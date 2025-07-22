import sys
import os
import telegram
from dotenv import load_dotenv
from openai import OpenAI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import textutil

textutil.text_to_mp3("hello", "output.mp3")

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
def send_mp3_message(ask):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_question},
            {"role": "user", "content": ask}
        ],
        temperature=0.8
    )
    answer = response.choices[0].message.content
    print(answer)
    textutil.text_to_mp3(answer, "output.mp3")
    tg_msg(answer)
    telegram.send_mp3_to_telegram(BOT_TOKEN, CHAT_ID, "output.mp3", answer)

send_mp3_message('''
인생에 힘이 되는 따뜻하고 철학적이며 투자에 도움이 되는 명언 한마디 알려줘!
한글로만 적어줘.
저자는 맨 아래에 한글로 알려줘. - 저자 - 이런식으로
''')

