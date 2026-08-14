import os
import requests

# 1. 환경변수 확인
telegram_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
gemini_key = os.getenv("GEMINI_API_KEY")

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

# 시도해볼 안전한 모델 목록
candidate_models = ["gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-pro"]
ai_message = None

print("--- [Gemini AI 응답 요청 시작] ---")
for model in candidate_models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    res = requests.post(url, json=payload)
    if res.status_code == 200:
        ai_json = res.json()
        ai_message = ai_json['candidates'][0]['content']['parts'][0]['text']
        print(f"🎉 성공한 모델: {model}")
        break
    else:
        print(f"⚠️ {model} 호출 실패 ({res.status_code}): {res.json().get('error', {}).get('message')}")

if not ai_message:
    raise Exception("모든 Gemini 모델 호출에 실패했습니다. API Key를 확인해 주세요.")

# 텔레그램 메시지 발송
telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
tele_payload = {"chat_id": chat_id, "text": ai_message}
tele_res = requests.post(telegram_url, json=tele_payload)

if tele_res.status_code == 200:
    print("🎉 텔레그램 알림 발송 최종 성공!")
else:
    print(f"❌ 텔레그램 발송 실패: {tele_res.text}")
