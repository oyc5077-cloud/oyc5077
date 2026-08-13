import os
import requests
from google import genai

# 환경변수에서 키 가져오기
telegram_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
gemini_key = os.getenv("GEMINI_API_KEY")

# 최신 SDK 방식으로 client 생성
client = genai.Client(api_key=gemini_key)

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=data)

# AI 비서 동작 로직
prompt = """
너는 초특가 항공권과 호텔을 동시에 감지하는 최고의 AI 여행 비서야.
사용자를 위해 항공권과 5성급 호텔이 같은 날짜에 동시 초특가로 나온 가상의 리포트를 작성해줘.
예시:
[🚨 항공+호텔 동시 초특가 감지!]
- 목적지: 후쿠오카 3박 4일
- 항공권: 110,000원 (왕복)
- 호텔: 5성급 1박 120,000원 (60% 할인)
- 특징: 같은 날짜 동시 특가 매칭 완료
"""

# 최신 2.5 모델 및 호환 호출 방식 사용
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
)

send_telegram_msg(response.text)
print("텔레그램 알림 발송 완료!")
