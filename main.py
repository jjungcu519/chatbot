#요청을 자동으로 처리
import os
import requests
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from utils import random_number, kospi, openai

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = FastAPI()

@app.post('/')
async def read_root(request: Request):

    body = await request.json()

    user_id = body['message']['from']['id']
    user_input = body['message']['text']

    if user_input[0] == '/' :
        #우리가 만든 기능 추가
        if user_input == '/lotto':
            text = random_number() #함수 실행한 것을 변수에 저장
        elif user_input == '/kospi':
            text = kospi()
        else:
            text = '지원하지 않는 기능입니다.'
       
    else:
        #openAI API 활용
        #text = openai(OPENAI_API_KEY, user_input)
        #text = '지원하는 기능은 /lotto, /kospi입니다.'
        text = langchain(OPENAI_API_KEY, user_input)

    req_url = f'{URL}/sendMessage?chat_id={user_id}&text={text}'
    res = requests.get(req_url)
    return {'hello': 'world'}