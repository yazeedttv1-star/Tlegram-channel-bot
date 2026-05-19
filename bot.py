import os
import time
import random
import requests
import json

# ===== ملف حفظ العبارات لمنع التكرار حتى بعد إعادة التشغيل =====
SEEN_FILE = "used_quotes.json"

def load_seen():
    try:
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(data):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(data), f, ensure_ascii=False)

used_quotes = load_seen()


# ===== مصادر كثيرة جدًا =====
APIS = [
    "https://api.quotable.io/random",
    "https://api.quotable.io/random?tags=life",
    "https://api.quotable.io/random?tags=wisdom",
    "https://api.quotable.io/random?tags=inspirational",
    "https://api.quotable.io/random?tags=love",
    "https://zenquotes.io/api/random",
    "https://zenquotes.io/api/random",
]


EMO = ["🖤", "🌙", "✨", "🤍"]


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


def get_from_api():

    for _ in range(20):  # محاولات كتير عشان يجيب حاجة جديدة

        api = random.choice(APIS)

        try:
            r = requests.get(api, timeout=10)
            if r.status_code != 200:
                continue

            data = r.json()

            # استخراج النص
            if "content" in str(data):
                text = data.get("content")
            elif isinstance(data, list):
                text = data[0].get("q")
            else:
                continue

            if not text:
                continue

            arabic = translate(text) or text

            # منع التكرار الحقيقي
            if arabic in used_quotes:
                continue

            used_quotes.add(arabic)
            save_seen(used_quotes)

            return f"{random.choice(EMO)} {arabic}"

        except:
            continue

    return None


def send_to_telegram():

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Missing env vars")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    text = get_from_api()

    if not text:
        text = "🖤 أحيانًا الصمت هو كل ما نحتاجه."

    try:
        requests.post(url, data={"chat_id": chat_id, "text": text}, timeout=10)
        print("Sent ✔")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":

    while True:
        send_to_telegram()
        time.sleep(random.randint(300, 600))  # 5–10 دقائق
