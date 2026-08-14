import os
import requests

# 1. 환경변수 가져오기
telegram_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
gemini_key = os.getenv("GEMINI_API_KEY")

print("--- [1. 환경변수 점검] ---")
print(f"TELEGRAM_TOKEN: {bool(telegram_token)}")
print(f"TELEGRAM_CHAT_ID: {bool(chat_id)}")
print(f"GEMINI_API_KEY: {bool(gemini_key)}")

try:
    # 2. Gemini 최신 REST API 호출 (SDK 파편화 영향 없음)
    print("\n--- [2. Gemini AI 응답 요청 중...] ---")
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"
    
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

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    ai_res = requests.post(gemini_url, json=payload)
    ai_json = ai_res.json()

    if ai_res.status_code != 200:
        raise Exception(f"Gemini API 오류 ({ai_res.status_code}): {ai_json}")

    # AI가 생성한 텍스트 추출
    ai_message = ai_json['candidates'][0]['content']['parts'][0]['text']
    print("AI 응답 생성 완료!")

    # 3. 텔레그램 메시지 발송
    print("\n--- [3. 텔레그램 알림 발송 중...] ---")
    telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    tele_payload = {
        "chat_id": chat_id,
        "text": ai_message
    }

    tele_res = requests.post(telegram_url, json=tele_payload)
    if tele_res.status_code == 200:
        print("🎉 텔레그램 알림 발송 성공!")
    else:
        print(f"❌ 텔레그램 발송 실패 ({tele_res.status_code}): {tele_res.text}")

except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    raise e
