import os
import time
import random
import requests

used_quotes = set()

# 5 مصادر مختلفة للعبارات
APIS = [
    "https://api.quotable.io/random",        # قوي
    "https://zenquotes.io/api/random",       # قوي
    "https://api.adviceslip.com/advice",     # نصائح قصيرة
    "https://api.quotable.io/random?tags=wisdom",
    "https://api.quotable.io/random?tags=inspirational"
]


def translate(text):
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": "ar",
            "dt": "t",
            "q": text
        }

        r = requests.get(url, params=params, timeout=10)

        if r.status_code == 200:
            return r.json()[0][0][0]

    except:
        pass

    return None


def extract_quote(api, data):

    # API 1 + 4 + 5 (quotable)
    if "quotable.io" in api:
        return data.get("content")

    # zenquotes
    if "zenquotes" in api:
        return data[0].get("q")

    # adviceslip
    if "adviceslip" in api:
        return data["slip"]["advice"]

    return None


def get_quote():

    for _ in range(10):  # يحاول يجيب حاجة جديدة

        api = random.choice(APIS)

        try:
            r = requests.get(api, timeout=10)

            if r.status_code != 200:
                continue

            data = r.json()
            text = extract_quote(api, data)

            if not text:
                continue

            # ترجمة للعربي
            arabic = translate(text)

            if not arabic:
                arabic = text

            # منع التكرار
            if arabic in used_quotes:
                continue

            used_quotes.add(arabic)

            return f"✨ {arabic}"

        except:
            continue

    return "✨ استمر.. النجاح محتاج صبر أكبر مما تتخيل."


def send_to_telegram():

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Missing env vars")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": get_quote()
    }

    try:
        requests.post(url, data=payload, timeout=10)
        print("✔ Sent")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":

    while True:
        send_to_telegram()
        time.sleep(300)  # كل 5 دقائق
