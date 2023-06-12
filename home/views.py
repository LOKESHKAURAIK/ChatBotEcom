from django.shortcuts import render
# from langchain.agents import create_sql_agent
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.chains import SQLDatabaseSequentialChain
# from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
# from langchain.agents import AgentExecutor
from langchain.chat_models import ChatOpenAI
from django.views.decorators.csrf import csrf_exempt
# from langchain.agents import AgentType
# from langchain.agents import initialize_agent, Tool
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from .models import Chatbot
import os
import openai

# os.environ["OPENAI_API_KEY"] = "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"
# from dotenv import load_dotenv
# load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


db_user = "admin"
db_password = "loku12345"
db_host = "myfirstdb.cyxgntsmiing.eu-north-1.rds.amazonaws.com"
db_name = "my_first_db"
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
# llm = OpenAI(temperature=0, verbose=True)

# tools = [Tool(name = "Jester", func=lambda x: "foo", description="useful for answer the question")]

# toolkit = SQLDatabaseToolkit(db=db, llm=llm)
# def generate_response(user_input):
#     agent_executor = create_sql_agent(
#     llm=OpenAI(temperature=0),
#     toolkit=toolkit,
#         max_execution_time=1, 
#         early_stopping_method="generate",
#         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True),
#     )
#     return agent_executor.run(user_input)


# <--- here is the Customize Prompt --->
_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}

If request is about the products, then always give answer as product name and only give Answer after Finished chain.

Question: {input}"""
PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
)



# <--- Function that generate_response --->
def generate_response(user_input):
    db_chain = SQLDatabaseSequentialChain.from_llm(llm, 
                                         db, 
                                        # use_query_checker=True,
                                        # prompt=PROMPT,
                                        verbose=True)
    return db_chain.run(user_input)
                                         


# <--- Function for storing a response --->
# def storing_response(user_input):
#     conversation = ConversationChain(llm=llm, 
#                                     verbose=True, 
#                                     memory=ConversationBufferMemory())

#     return conversation.predict(input=user_input)



# <--- Function that taking text_input --->
@csrf_exempt
def text_input(request):
    if request.method == "POST":
        user_input = request.POST["message"]
        response = generate_response(user_input)
        bot = Chatbot.objects.create(user_input=user_input, bot_response=response)
        bot.save()
        data = Chatbot.objects.all()
        print(data)
        # response1 = storing_response(user_input)
        # if response1:
        # print(response)
    return render(request, "index.html",{"data" : data})

def index(request):
    data = Chatbot.objects.all()
    print(data)
        # response1 = storing_response(user_input)
        # if response1:
        # print(response)
    return render(request, "index.html",{"data" : data})