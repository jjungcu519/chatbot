import os
import requests
from dotenv import load_dotenv #-> 읽어서 환경 변수에 저장

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') #-> 가져오는 친구

URL = f'https://api.telegram.org/bot{TOKEN}'

method = 'getUpdates'

res = requests.get(f'{URL}/{method}') #리스폰스 값 200

res_dict = res.json() #json형태로 변환

#딕셔너리 인덱스 접근
user_input = res_dict['result'][-1]['message']['text']
user_id = res_dict['result'][-1]['message']['from']['id']

print(user_id, user_input)


SEND_MSG_URL = f'{URL}/sendMessage?chat_id={user_id}&text={user_input}' #?뒤는 파라미터, 변수 라는 뜻

for i in range(5)
requests.get(SEND_MSG_URL)