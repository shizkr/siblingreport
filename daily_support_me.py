import os
import time
import requests
import openai
from dotenv import load_dotenv
from openai import OpenAI

import telegram
import textutil

if os.getenv("GITHUB_ACTIONS") != "true":
    load_dotenv()  # 로컬 환경일 경우에만 .env 파일을 불러옵니다

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# 환경 변수 로드 (GitHub Actions에서는 Secrets로 자동 주입됨)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# OpenAI 클라이언트 생성
client = OpenAI(api_key=OPENAI_API_KEY)

def tg_msg(msg):
    telegram.send_message_to_telegram(BOT_TOKEN, CHAT_ID, msg)

system_question = "AI  내 개인 비서처럼 작성해줘."
def send_message(ask):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_question},
            {"role": "user", "content": ask}
        ],
        temperature=0.8
    )
    answer = response.choices[0].message.content
    tg_msg(answer)
    time.sleep(1)

def send_message_mp3(ask):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_question},
            {"role": "user", "content": ask}
        ],
        temperature=0.9
    )
    answer = response.choices[0].message.content

    textutil.text_to_mp3(answer, "output.mp3")
    tg_msg(answer)
    telegram.send_mp3_to_telegram(BOT_TOKEN, CHAT_ID, "output.mp3", answer[:20])
    time.sleep(1)

send_message('''
인생에 힘이 되는 따뜻하고 철학적이며 투자에 도움이 되는 명언 한마디 알려줘!
영어, 한글, 중국어, 일본어 순서로 같이 적어주고. 중국어의 경우에는 병음을 같이 알려줘.
일본어의 경우는 히라가나로 적어줘.
저자는 맨 아래에 한글과 영어로 이름만 포함해줘 -한글/영어-
''')
send_message('''엔지니어링 메니저를 위한 조언 한마디 써줘. 50자 이내''')
send_message('''오늘의 습관/루틴 챌린지 하나 알려줘. 50자 이내''')
send_message_mp3('''아침에 듣기 좋은 명상 메세지로 300자 이내로 읅어줄래. 바로 알려줘 물론입니다 이런거 앞에 붙이지 말고.''')
