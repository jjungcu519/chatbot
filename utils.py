import random
import requests
from openai import OpenAI
from langchain import hub
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def random_number():
    return str(sorted(random.sample(range(1, 46), 6)))

def kospi():
    KOSPI_URL = 'https://finance.naver.com/sise/'

    res = requests.get(KOSPI_URL)

    res_text = res.text

    selector = '#KOSPI_now'

    soup = BeautifulSoup(res_text, 'html.parser')
    kospi = soup.select_one(selector).text
    return kospi

def openai(api_key, user_input):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role': 'system', 'content': '사용자와 즐겁게 이야기하는 챗봇이 되렴. 단, 출력 결과에서 #은 빼줘.'},
        {'role': 'user', 'content':user_input},
        ]
    )

    return completion.choices[0].message.content

def langchain(api_key, user_input):
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

#1. load document    
    loader = WebBaseLoader(
        web_paths=(
            'https://www.donga.com/news/Inter/article/all/20240722/126057224/1',
            ),
    )

    docs = loader.load()

#2. split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

#3. store
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

#4. retriever
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")


    rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser() 
    )

    return rag_chain.invoke(user_input)