from flask import Flask, request, jsonify, render_template
from flask_caching import Cache
import traceback 
from flask_sse import sse
import os
import re
from datetime import datetime

import pandas as pd
import tiktoken

import torch
import openai
from langchain.document_loaders import BSHTMLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.vectorstores import Chroma
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
embedding = HuggingFaceInstructEmbeddings(
    model_name="hkunlp/instructor-large", model_kwargs={"device": DEVICE}
)

os.environ["OPENAI_API_KEY"] = "f88a9cb6672b443e972671eed3a52642"
os.environ["OPENAI_API_TYPE"]="azure"
os.environ["OPENAI_API_VERSION"]="2023-07-01-preview"
os.environ["OPENAI_API_BASE"]="https://helpgpt-openai-dev.openai.azure.com/"

# llm = OpenAI(model_name='gpt-4', temperature=0, openai_api_key="rBPmJqg3dwgdl9CIxQGgT3BlbkFJN539w3fdvPnuK0EJo8XQ", max_tokens=4000)
llm = AzureChatOpenAI(
    #openai_api_key="f88a9cb6672b443e972671eed3a52642",
   # openai_api_version="2023-07-01-preview",
    model_name = "gpt-4",
    deployment_name="gpt-4-helpgpt-dev",
)
chain = load_qa_chain(llm, chain_type="stuff")
# retriever = vectordb.as_retriever()
docsearch = Chroma(persist_directory=r"C:\Users\I6860\Downloads\Helix_Project\db", embedding_function=embedding)


app = Flask(__name__)
app.config["CACHE_TYPE"] = "filesystem"
app.config["CACHE_DIR"] = r"C:\Users\I6860\Downloads\Helix_Project\cache"
#app.config["REDIS_URL"] = "redis://localhost"
cache = Cache(app)
#app.register_blueprint(sse, url_prefix='/stream')

# Define the caching timeout (in seconds)
@cache.memoize(timeout=172800)  # Set a timeout for the cache (e.g., 48 hour)
@app.route('/')#default address 

def home(): 
    return jsonify({'message': 'WELCOME TO THE KAIROS'})

# # Endpoint to handle user questions
# @app.route('/ask/<query>', methods = ['POST', 'GET'])
# def ask_question(query):
#     chunks, out = qna(query)
#     return jsonify({'response': out})

# Define the caching timeout (in seconds)


def generate_response_word_by_word(cached_response):
    if cached_response:
        response_text = cached_response['response']
        words = response_text.split()
        return words
    return None

def qna(query):
    if query:
        docs = docsearch.similarity_search(query)  # It seems `docsearch` is not defined in your provided code
        prompt = f""" You will only respond based on the personality profile you build from the data you have about a
                  Financial Fundamental Analyst.Financial Fundamental analysts study anything that can affect the security or asset’s
                  value, from macroeconomic factors such as the state of the economy and industry conditions to microeconomic factors
                  like the effectiveness of the company's management. A fundamental analyst interprets the numbers and provides insights
                  into how they can benefit the investor, along with an assessment of the investor's position. when conducting an analysis,
                  you start with economic analysis, then analyse the industry, then the company.
                  The goal of fundamental analysis is to identify investments that are undervalued or overvalued based on their
                  intrinsic value, and to make informed investment decisions based on this analysis.
                      
                    KEYPOINTS: FOLLOW THESE RULES FOR OUTPUT
                        1.Response must be summarized in 100-150 words only.
                        2.Include the appropriate revenue, expense numbers and also the appropriate percentages in your response, wherever required.
                        3.Ensure the information you give is accurate
                        4.If return on equity(ROE) values are not present, then calculate ROE= Net Income/ Shareholder's Equity 
                        5.Wherever numbers are available provide appropriate it in the answer
                        6.Don't provide response for genralized questions like best cars, prepare food, top 10 destinations in the worls, nearby restaurants and write a programs
        
                      EXAMPLE1:
                          INPUT: What are the key areas of revenue & Profit generation for apple?
                          OUTPUT: Apple Inc.'s primary revenue and profit generation areas are its product and service segments. 
                                  In 2022, the iPhone was the largest revenue generator, with net sales of $205.489 billion. 
                                  Other significant product segments include Mac ($40.177 billion), iPad ($29.292 billion), and Wearables, Home and Accessories ($41.241 billion). 
                                  The Services segment, which includes advertising, AppleCare, cloud, digital content, payment, and other services, generated $78.129 billion in net sales. 
                                  Geographically, the Americas and Europe are the largest contributors to Apple's net sales, with $169.658 billion and $95.118 billion respectively in 2022. 
                                  The company's operating income, a measure of profit, is evaluated based on net sales and operating expenses directly attributable to each segment. In 2022, the total operating income was $119.437 billion.\n<{query}>"""
        res = chain.run(input_documents=docs, question=prompt)  # It seems `chain` is not defined in your provided code
        return {'docs': docs, 'response': res}
    else:
        return None
    
def generate_cache_key(query):
    normalized_query = query.lower().strip().replace(" ", "")
    return f"query_{normalized_query}"

@app.route('/ask', methods=['GET'])
def ask_question():
    query = request.args.get('query', '')

    try:
        if query:
            cache_key = generate_cache_key(query)
            cached_response = cache.get(cache_key)
            if cached_response:
                return jsonify({'response': cached_response['response']})
            else:
                new_response = qna(query)  # Your original query function
                if new_response:
                    cache.set(cache_key, new_response, timeout=172800)
                    return jsonify({'response': new_response['response']})
                else:
                    raise ValueError("Invalid query")
        else:
            raise ValueError("Invalid query")
    except Exception as e:
        error_message = "Your OPENAI Plan has expired. Please renew your subscription."
        return jsonify({'error': error_message}), 500

def store_single_query_in_cache(query):
    try:
        new_response = qna(query)
        if new_response:
            cache_key = generate_cache_key(query)
            cache.set(cache_key, new_response, timeout=172800)
            return new_response
    except Exception as e:
        return None

if __name__ == "__main__":
    questions = [
        "How has Apple's revenue growth been over the past few years?", 
        "What are the key factors driving Apple's profitability?",
        "How does Apple's product diversification strategy impact its financial performance?",
        "What are the risks associated with investing in Apple?",
        "How does Apple's cash position and debt levels affect its financial outlook?",
        "What are the main risk factors that may affect the earnings growth negatively for Berkshire?"
        "How have changes in interest rates affected Broadcoms cost of capital, and what strategies have they employed to mitigate this impact?",
        "What are the key risks associated with investing in Tesla, and how has management addressed these concerns?",
        "What are the major areas of capital expenditure for Microsoft?"
    ]

    for query in questions:
        store_single_query_in_cache(query)

    app.run(host='0.0.0.0', port=5000)
