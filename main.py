import os
import requests
import google.generativeai as genai

# 1. 환경변수 확인
telegram_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
gemini_key = os.getenv("GEMINI_API_KEY")

print("--- [환경변수 점검] ---")
print(f"TELEGRAM_TOKEN 존재 여부: {bool(telegram_token)}")
print(f"TELEGRAM_CHAT_ID 존재 여부: {bool(chat_id)}")
print(f"GEMINI_API_KEY 존재 여부: {bool(gemini_key)}")

try:
    # 2. Gemini AI 설정 및 실행
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

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

    print("\n--- [Gemini AI 응답 생성 중...] ---")
    response = model.generate_content(prompt)
    print("AI 응답 생성 성공!")

    # 3. 텔레그램 전송
    print("\n--- [텔레그램 메시지 발송 중...] ---")
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    data = {"chat_id": chat_id, "text": response.text, "parse_mode": "Markdown"}
    res = requests.post(url, data=data)
    
    if res.status_code == 200:
        print("🎉 텔레그램 알림 발송 최종 성공!")
    else:
        print(f"❌ 텔레그램 전송 실패 (상태코드 {res.status_code}): {res.text}")

except Exception as e:
    print(f"\n❌ 실행 중 오류 발생: {e}")
    raise e
response = model.generate_content(prompt)
send_telegram_msg(response.text)
print("텔레그램 알림 발송 완료!")
