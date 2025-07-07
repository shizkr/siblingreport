import os
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

## Question to ChatGPT
system_question = "너는 가족들에게 메세지를 보내는 막내 동생이야. 이에 맞춰서 50살 남자 느낌으로 작성해줘."
user_question = '''당신은 한국에 사는 55~70세 가족들에게 매주 따뜻한 안부
메세지를 전하는 AI. 다음 항목에 맞춰
너무 기술적이지 않으면서도 따뜻하고 정감 있는 말투로 구성. 메시지는 한국어로 작성하며,
각 항목은 짧고 간결하고 여약해주세요 전체분량은 500자 이내.
1. 이번주를 시작하는 따뜻한 인삿말.
2. 삶에 도움이 되는 한줄 명언 또는 격려 메시지
3. 이번주 한국/세계 주요뉴스 2~3 요약 (쉽고 친근한 표현 사용)
4. 50-70대 여자에게 유익한 건강 팁 하나
아주 간단한 화이팅 마무리 메세지 넣어줘.'''

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_question},
        {"role": "user", "content": user_question}
    ],
    temperature=0.8
)
answer = response.choices[0].message.content
tg_msg(answer)
