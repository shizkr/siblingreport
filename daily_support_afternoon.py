import os
import time
import requests
import openai
from dotenv import load_dotenv
from openai import OpenAI

import telegram

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

send_message('''투자 전문가용 경제 지식 및 투자 관련 200자
이내로 하나 알려줘.''')
