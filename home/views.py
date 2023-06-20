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
# from dotenv import load_dotenv


os.environ["OPENAI_API_KEY"] = "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"


#<---  environment variable --->
# openai.api_key = os.getenv("OPENAI_API_KEY")
# print(os.getenv("db_password"))


# load_dotenv()
# print(os.getenv("OPENAI_API_KEY"))
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


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
_DEFAULT_TEMPLATE = """ I am a chatbot for ecommerce website. I can help you find products, 
answer your questions, and provide customer support.

Here are some of the things I can do:
Show you product details, such as price, description, and reviews.
Help you find products that match your criteria.
Answer your questions about products.
Provide customer support, such as troubleshooting problems and processing returns.


I can also have normal conversations with you. I can talk about your interests, listen to your problems, and offer advice.

So, if you have any questions about our products or need help with anything, please don't hesitate to ask. I'm here to help!

This prompt is designed to be informative and helpful. It explains what the chatbot can do and how it can be used. 
It also sets a friendly and approachable tone.

Here are some specific examples of how the chatbot could be used to show product details and have normal conversations with customers:

A customer could ask the chatbot for the price of a product. The chatbot would then provide the price and any other relevant information, such as the product description and reviews.
A customer could ask the chatbot about the features of a product. The chatbot would then provide a detailed description of the product's features.
A customer could ask the chatbot for recommendations for products. The chatbot would then recommend products based on the customer's interests and preferences.
A customer could ask the chatbot for help with a problem. The chatbot would then try to troubleshoot the problem and offer advice.
A customer could simply chat with the chatbot about their day. The chatbot would then listen to the customer and offer support and encouragement.


ConversationHistory: {table_info}

MemoryContext: {dialect} 

Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"  
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"



 <expert ecommerce advisor> :


Human: {input}

"""

PROMPT = PromptTemplate(
    input_variables=["dialect", "table_info", "input",], template=_DEFAULT_TEMPLATE
)



# <--- Function that generate_response --->

def generate_response(user_input):

    db_chain = SQLDatabaseChain.from_llm(llm, 
                                        db, 
                                        # use_query_checker=True,
                                        prompt=PROMPT,
                                        verbose=True)

    return db_chain.run(user_input)
                                         


# <--- Function for storing a response --->
# def storing_response(user_input):
#     conversation = ConversationChain(llm=llm, 
#                                     verbose=True, 
#                                     memory=ConversationBufferMemory())

#     return conversation.predict(input=user_input)



def OpenAIFunction(crust):

    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=crust,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return completions["choices"][0]["text"]


# <--- Function that taking text_input --->
@csrf_exempt
def text_input(request):
    if request.method == "POST":
        user_input = request.POST["message"]
        try:    
            response = generate_response(user_input)
            bot = Chatbot.objects.create(user_input=user_input, bot_response=response)
            bot.save()
            data = Chatbot.objects.all()
            return render(request, "index.html",{"data" : data})
        except:
            prompt = f"You are  <expert Ecommerce Shoppoing advisor>,<having ability to suggest product according to customer interest> <inteligent> human current question:{user_input}\n  Now if human current question: {user_input} for something then ask human for that otherwise give best answer as a shopping advisor "
            response = OpenAIFunction(prompt)
            bot = Chatbot.objects.create(user_input=user_input, bot_response=response)
            bot.save()
            data = Chatbot.objects.all()
            return render(request, "index.html",{"data" : data})
    else:
        return render(request, "index.html")

def index(request):
    data = Chatbot.objects.all()
    # print(data)
        # response1 = storing_response(user_input)
        # if response1:
        # print(response)
    return render(request, "index.html",{"data" : data})