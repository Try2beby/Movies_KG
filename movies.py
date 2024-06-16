import requests
from py2neo import Graph, Node, Relationship
import tqdm
import json
import time

import dotenv

dotenv.load_dotenv()

from loguru import logger
import sys
import os

LOG_DIR = "./log"
# 获取脚本的文件名（不包括扩展名）
script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

# 使用脚本的文件名作为日志文件的文件名
log_filename = script_name + ".log"

# 设置日志级别
logger.remove()
logger.add(sys.stderr, level="INFO")

# 创建一个处理器，将日志输出到文件
logger.add(os.path.join(LOG_DIR, log_filename), level="INFO")


class MoviesKG:
    def __init__(
        self,
        download=False,
        num_pages=100,
    ) -> None:
        self.api_key = os.getenv("TMDB_API_KEY")  # 替换为你的 TMDB API 密钥
        self.url = {
            "search": "https://api.themoviedb.org/3/movie/popular?api_key={api_key}&page={page}",
            "details": "https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits",
        }

        self.config_spec_name = "./data/movies_{num_pages}.json".format(
            num_pages=num_pages
        )

        self.graph = Graph(
            "bolt://localhost:7687", auth=("neo4j", os.getenv("NEO4J_PASSWORD"))
        )

        if download:
            self.movies = self.get_movies(num_pages)
            self.movies_detailed = self.get_details()
        else:
            with open(self.config_spec_name, "r") as f:
                self.movies_detailed = json.load(f)

    def get_movies(self, num_pages):
        all_movies = []
        for page in tqdm.tqdm(range(1, num_pages + 1), desc="Getting movies"):
            url = self.url["search"].format(api_key=self.api_key, page=page)
            # logger.info(f"Retrieving data for page {page}")
            success = False
            attempts = 0
            while not success and attempts < 5:
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        all_movies.extend(data["results"])
                        success = True
                    else:
                        print(
                            f"Failed to retrieve data for page {page}, status code: {response.status_code}"
                        )
                        attempts += 1
                        time.sleep(5)  # 等待5秒后重试
                except requests.RequestException as e:
                    print(f"Request exception for page {page}: {e}")
                    attempts += 1
                    time.sleep(5)  # 等待5秒后重试
        return all_movies

    def get_details(self):
        detailed_movies = []
        for movie in tqdm.tqdm(self.movies, desc="Getting movie details"):
            url = self.url["details"].format(movie_id=movie["id"], api_key=self.api_key)
            # logger.info(f"Retrieving details for movie ID {movie['id']}")
            success = False
            attempts = 0
            while not success and attempts < 5:
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        detailed_movies.append(data)
                        success = True
                    else:
                        print(
                            f"Failed to retrieve details for movie ID {movie['id']}, status code: {response.status_code}"
                        )
                        attempts += 1
                        time.sleep(5)  # 等待5秒后重试
                except requests.RequestException as e:
                    print(f"Request exception for movie ID {movie['id']}: {e}")
                    attempts += 1
                    time.sleep(5)  # 等待5秒后重试
        return detailed_movies

    def filter_data(self):
        filtered_data = []
        for movie in self.movies_detailed:
            filtered_data.append(self.filter_one_data(movie))
        # save filtered data to json
        with open("./data/movies_filtered.json", "w") as f:
            json.dump(filtered_data, f, indent=4)

        self.filtered_data = filtered_data

    def filter_one_data(self, movie_details_item):
        movie_keys = [
            "belongs_to_collection",
            # "genres",
            "budget",
            # "origin_country",
            "id",
            # "imdb_id",
            "overview",
            # "production_companies",
            "release_date",
            "revenue",
            "runtime",
            "tagline",
        ]
        # belongs_to_collection_keys = ["id", "name"]
        production_companies_keys = ["id", "name", "origin_country"]

        crew_keep_jobs = ["Director", "Producer", "Executive Producer"]
        crew_keys = ["id", "name", "job"]

        cast_top = 10
        cast_keys = ["id", "name", "character", "gender"]

        movie = {key: movie_details_item[key] for key in movie_keys}
        if movie["belongs_to_collection"]:
            movie["belongs_to_collection"] = movie["belongs_to_collection"]["name"]

        origin_country = movie_details_item["origin_country"]

        production_companies = [
            {key: company[key] for key in production_companies_keys}
            for company in movie_details_item["production_companies"]
        ]

        genres = [genre["name"] for genre in movie_details_item["genres"]]

        crew = [
            {key: person[key] for key in crew_keys}
            for person in movie_details_item["credits"]["crew"]
            if person["job"] in crew_keep_jobs
        ]
        cast = [
            {key: person[key] for key in cast_keys}
            for person in movie_details_item["credits"]["cast"][:cast_top]
        ]

        return dict(
            movie=movie,
            genres=genres,
            production_companies=production_companies,
            crew=crew,
            cast=cast,
            origin_country=origin_country,
        )

    def build_graph(self):
        self.load_filtered_data()
        for movie in tqdm.tqdm(self.filtered_data, desc="Building graph"):
            self.insert_one_movie(movie)

    def insert_one_movie(self, movie_data):
        tx = self.graph.begin()

        # 插入电影节点
        movie_node = Node("Movie", **movie_data["movie"])
        tx.merge(movie_node, "Movie", "id")

        # 插入 genre 节点并建立关系
        for genre_name in movie_data["genres"]:
            genre_node = Node("Genre", name=genre_name)
            tx.merge(genre_node, "Genre", "name")
            relationship = Relationship(movie_node, "BELONGS_TO_GENRE", genre_node)
            tx.create(relationship)

        # 插入 production company 节点并建立关系
        for company in movie_data["production_companies"]:
            company_node = Node(
                "ProductionCompany",
                id=company["id"],
                name=company["name"],
                origin_country=company["origin_country"],
            )
            tx.merge(company_node, "ProductionCompany", "id")
            relationship = Relationship(movie_node, "PRODUCED_BY", company_node)
            tx.create(relationship)

        # 插入 origin country 节点并建立关系
        for country in movie_data["origin_country"]:
            country_node = Node("Country", name=country)
            tx.merge(country_node, "Country", "name")
            relationship = Relationship(movie_node, "ORIGIN_COUNTRY", country_node)
            tx.create(relationship)

        # 插入 crew 节点并建立关系
        for crew_member in movie_data["crew"]:
            crew_node = Node("Person", id=crew_member["id"], name=crew_member["name"])
            tx.merge(crew_node, "Person", "id")
            relationship = Relationship(
                crew_node, crew_member["job"].replace(" ", "_").upper(), movie_node
            )
            tx.create(relationship)

        # 插入 cast 节点并建立关系
        for cast_member in movie_data["cast"]:
            cast_node = Node(
                "Person",
                id=cast_member["id"],
                name=cast_member["name"],
                gender=cast_member["gender"],
            )
            tx.merge(cast_node, "Person", "id")
            relationship = Relationship(
                cast_node, "ACTED_IN", movie_node, character=cast_member["character"]
            )
            tx.create(relationship)

        tx.commit()

    def clear_database(self):
        self.graph.run("MATCH (n) DETACH DELETE n")
        print("Database cleared.")

    def get_node_count(self):
        return self.graph.run("MATCH (n) RETURN count(n) AS count").evaluate()

    def save_to_json(self):
        with open(self.config_spec_name, "w") as f:
            json.dump(self.movies_detailed, f, indent=4)

    def load_from_json(self):
        with open(self.config_spec_name, "r") as f:
            self.movies_detailed = json.load(f)

    def load_filtered_data(self):
        with open("./data/movies_filtered.json", "r") as f:
            self.filtered_data = json.load(f)
