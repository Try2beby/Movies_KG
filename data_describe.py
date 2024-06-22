from collections import Counter
import matplotlib.pyplot as plt
from matplotlib_inline import backend_inline

backend_inline.set_matplotlib_formats("svg")


class DataDescribe:
    def __init__(self, movies_detailed):
        self.movies_detailed = movies_detailed
        self.save_path = "./fig/"

    def get_all(self, key, remove_none=True):
        return (
            [movie[key] for movie in self.movies_detailed if movie[key] is not None]
            if remove_none
            else [movie[key] for movie in self.movies_detailed]
        )

    def plot_belongs_to_collection(self):
        # belongs_to_collection
        data_belong = self.get_all("belongs_to_collection")
        # count unique values
        data_belong_count = Counter([item["name"] for item in data_belong])
        # sort
        data_belong_count = dict(
            sorted(data_belong_count.items(), key=lambda x: x[1], reverse=True)
        )
        data_belong_count_plot = dict(list(data_belong_count.items())[:30])
        # visualize use horizontal bar, with x axis on the top
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(
            [
                item.rstrip(" Collection")
                for item in list(data_belong_count_plot.keys())
            ],
            list(data_belong_count_plot.values()),
            color="#1db9d8",
        )
        plt.gca().invert_yaxis()
        plt.xlabel("Count")
        plt.ylabel("Collection")
        plt.title("Top 30 Belongs to Collection")

        # 移除坐标轴线
        for side in ["bottom", "left", "right"]:
            ax.spines[side].set_visible(False)

        ax.xaxis.tick_top()
        ax.xaxis.set_label_position("top")

        plt.subplots_adjust(left=0.3, right=0.9, top=0.85, bottom=0.02)
        # save
        plt.savefig(self.save_path + "belongs_to_collection.svg")

        plt.show()

    def plot_genres(self):
        # genres
        data_genres = self.get_all("genres")
        data_genres_count = Counter(
            [item["name"] for sublist in data_genres for item in sublist]
        )
        data_genres_count = dict(
            sorted(data_genres_count.items(), key=lambda x: x[1], reverse=True)
        )
        data_genres_count_plot = dict(list(data_genres_count.items())[:30])
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(
            list(data_genres_count_plot.keys()),
            list(data_genres_count_plot.values()),
            color="#1db9d8",
        )
        plt.gca().invert_yaxis()
        plt.xlabel("Count")
        plt.ylabel("Genres")
        plt.title("Top 30 Genres")
        for side in ["bottom", "left", "right"]:
            ax.spines[side].set_visible(False)
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position("top")

        plt.subplots_adjust(left=0.3, right=0.9, top=0.85, bottom=0.02)
        # save
        plt.savefig(self.save_path + "genres.svg")

        plt.show()

    def plot_original_country(self):
        # original_country
        data_country = self.get_all("production_countries")
        data_country_count = Counter(
            [item["name"] for sublist in data_country for item in sublist]
        )
        data_country_count = dict(
            sorted(data_country_count.items(), key=lambda x: x[1], reverse=True)
        )
        data_country_count_plot = dict(list(data_country_count.items())[:30])
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(
            list(data_country_count_plot.keys()),
            list(data_country_count_plot.values()),
            color="#1db9d8",
        )
        plt.gca().invert_yaxis()
        plt.xlabel("Count")
        plt.ylabel("Country")
        plt.title("Top 30 Production Countries")
        for side in ["bottom", "left", "right"]:
            ax.spines[side].set_visible(False)
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position("top")

        plt.subplots_adjust(left=0.3, right=0.9, top=0.85, bottom=0.02)
        # save
        plt.savefig(self.save_path + "original_country.svg")

        plt.show()

    def plot_production_companies(self):
        # production_companies
        data_companies = self.get_all("production_companies")
        data_companies_count = Counter(
            [item["name"] for sublist in data_companies for item in sublist]
        )
        data_companies_count = dict(
            sorted(data_companies_count.items(), key=lambda x: x[1], reverse=True)
        )
        data_companies_count_plot = dict(list(data_companies_count.items())[:30])
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(
            list(data_companies_count_plot.keys()),
            list(data_companies_count_plot.values()),
            color="#1db9d8",
        )
        plt.gca().invert_yaxis()
        plt.xlabel("Count")
        plt.ylabel("Company")
        plt.title("Top 30 Production Companies")
        for side in ["bottom", "left", "right"]:
            ax.spines[side].set_visible(False)
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position("top")

        plt.subplots_adjust(left=0.3, right=0.9, top=0.85, bottom=0.02)
        # save
        plt.savefig(self.save_path + "production_companies.svg")

        plt.show()

    def plot_crew(self):
        # crew
        data_credits = self.get_all("credits")
        data_crew = [item["crew"] for item in data_credits]
        data_crew_count = Counter(
            [item["job"] for sublist in data_crew for item in sublist]
        )
        data_crew_count = dict(
            sorted(data_crew_count.items(), key=lambda x: x[1], reverse=True)
        )
        data_crew_count_plot = dict(list(data_crew_count.items())[:30])
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(
            list(data_crew_count_plot.keys()),
            list(data_crew_count_plot.values()),
            color="#1db9d8",
        )
        plt.gca().invert_yaxis()
        plt.xlabel("Count")
        plt.ylabel("Job")
        plt.title("Top 30 Crew Jobs")
        for side in ["bottom", "left", "right"]:
            ax.spines[side].set_visible(False)
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position("top")

        plt.subplots_adjust(left=0.3, right=0.9, top=0.85, bottom=0.02)
        # save
        plt.savefig(self.save_path + "crew.svg")

        plt.show()

    # # plot net revenue: revenue - budget
    # def plot_net_revenue(self):
    #     data_revenue = self.get_all("revenue")
    #     data_budget = self.get_all("budget")
    #     data_net_revenue = [
    #         revenue - budget for revenue, budget in zip(data_revenue, data_budget)
    #     ]
    #     fig, ax = plt.subplots(figsize=(8, 6))
    #     ax.hist(data_net_revenue, bins=100, color="#1db9d8")
    #     plt.xlabel("Net Revenue")
    #     plt.ylabel("Count")
    #     plt.title("Net Revenue Distribution")
    #     for side in ["top", "right"]:
    #         ax.spines[side].set_visible(False)

    #     plt.subplots_adjust(left=0.15, right=0.9, top=0.85, bottom=0.15)
    #     # save
    #     plt.savefig(self.save_path + "net_revenue.svg")

    #     plt.show()

    # plot budget & revenue scatter
    def plot_budget_revenue(self):
        data_budget = self.get_all("budget")
        data_revenue = self.get_all("revenue")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(data_budget, data_revenue, color="#1db9d8", alpha=0.5, s=5)
        plt.xlabel("Budget")
        plt.ylabel("Revenue")
        plt.title("Budget vs Revenue")
        for side in ["top", "right"]:
            ax.spines[side].set_visible(False)

        plt.subplots_adjust(left=0.15, right=0.9, top=0.85, bottom=0.15)
        # save
        plt.savefig(self.save_path + "budget_revenue.svg")

        plt.show()

    # plot vote count & vote average scatter
    def plot_vote_count_vote_average(self):
        data_vote_count = self.get_all("vote_count")
        data_vote_average = self.get_all("vote_average")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(data_vote_count, data_vote_average, color="#1db9d8", alpha=0.5, s=5)
        plt.xlabel("Vote Count")
        plt.ylabel("Vote Average")
        plt.title("Vote Count vs Vote Average")
        for side in ["top", "right"]:
            ax.spines[side].set_visible(False)

        plt.subplots_adjust(left=0.15, right=0.9, top=0.85, bottom=0.15)
        # save
        plt.savefig(self.save_path + "vote_count_vote_average.svg")

        plt.show()
