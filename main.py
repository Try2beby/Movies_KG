import importlib
import movies
import data_describe
import os

importlib.reload(movies)

MoviesKG = movies.MoviesKG
DataDescribe = data_describe.DataDescribe


import matplotlib.pyplot as plt

# %matplotlib inline
from matplotlib_inline import backend_inline

backend_inline.set_matplotlib_formats("svg")

movies_kg = MoviesKG()


from langchain_community.chat_models import ChatZhipuAI
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph

llm = ChatZhipuAI(
    temperature=0,
    zhipuai_api_key=os.getenv("ZHIPUAI_API_KEY"),
    model_name="GLM-4-0520",
    # model_name="GLM-4-Flash",
)
graph = Neo4jGraph(
    url="bolt://localhost:7687", username="neo4j", password=os.getenv("NEO4J_PASSWORD")
)
chain = GraphCypherQAChain.from_llm(llm, graph=graph, verbose=True)


def get_answer(question, choice=""):
    if choice:
        return chain.invoke(choice)["result"]
    return chain.invoke(question)["result"]


from enum import Enum


class QUESTION(str, Enum):
    # 简单单跳问题
    Q11 = "Who starred in 'The Dark Knight'?"
    Q12 = "Who directed 'The Dark Knight'?"
    Q13 = "Which movies did Christopher Nolan direct?"

    # 添加筛选条件
    Q21 = (
        "Besides 'The Dark Knight', which other movies has Christopher Nolan directed?"
    )
    Q22 = "In which movies have Michael Caine and Maggie Gyllenhaal co-starred?"
    # Q5 = "What other films has the director of 'The Dark Knight' directed?"


default_questions = [question.value for question in QUESTION]

print(get_answer(QUESTION.Q22.value))


import gradio as gr

# Corrected Gradio interface setup
iface = gr.Interface(
    fn=get_answer,
    inputs=[
        gr.Dropdown(
            choices=default_questions,
            label="Select a question",
            value=default_questions[0],
        ),  # 默认选择第一个问题
        gr.Textbox(lines=2, label="Or enter your question here..."),
    ],
    outputs=gr.Textbox(lines=10, label="Output"),  # 增加输出行数
    title="GraphCypher QA System",
    description="Ask any question related to the movie database.",
)


# Launch the Gradio app
iface.launch(share=True)
