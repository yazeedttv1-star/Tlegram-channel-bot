import os
import time
import random
import requests

used_quotes = set()

# ====== 5 APIs اقتباسات حب ======
LOVE_APIS = [
    "https://api.quotable.io/random?tags=love",
    "https://api.quotable.io/random?tags=romance",
    "https://api.quotable.io/random",
    "https://zenquotes.io/api/random",
    "https://api.quotable.io/random?tags=life"
]

# ====== 5 APIs عبارات قوية ======
STRONG_APIS = [
    "https://api.quotable.io/random?tags=wisdom",
    "https://api.quotable.io/random?tags=inspirational",
    "https://api.quotable.io/random?tags=famous-quotes",
    "https://api.quotable.io/random?tags=success",
    "https://api.quotable.io/random"
]

# ====== واتساب ستايل ======
WHATSAPP_STYLE = [
    "✨ في ناس وجودهم راحة مش تفسير.",
    "🖤 الحب الحقيقي مبيقلش مهما بعدنا.",
    "⚡ القوة إنك تكمل حتى لو لوحدك.",
    "🤍 اللي بيحبك بجد بيفضل ثابت.",
    "🌙 بعض القلوب مش بتتنسى.",
    "🔥 الكرامة أهم من أي شعور.",
    "✨ مش كل حب بيكمل، بس كل حب بيعلم.",
    "🖤 أحيانًا البعد بيكون إنقاذ.",
    "⚡ القوة مش في الكلام.. القوة في الصمت.",
    "🤍 بعض الناس وجودهم أمان مش صدفة."
]

# ====== فلترة ======
BLOCKED = ["doctor", "medical", "health", "disease", "مرض", "طبيب", "علاج"]


def is_valid(text):
    t = text.lower()
    return not any(w in t for w in BLOCKED)


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


def extract(api, data):
    if "quotable.io" in api:
        return data.get("content")
    if "zenquotes" in api:
        return data[0].get("q")
    return None


def get_api_quote(api_list):

    for _ in range(10):

        api = random.choice(api_list)

        try:
            r = requests.get(api, timeout=10)

            if r.status_code != 200:
                continue

            data = r.json()
            text = extract(api, data)

            if not text:
                continue

            if not is_valid(text):
                continue

            arabic = translate(text) or text

            if not is_valid(arabic):
                continue

            if arabic in used_quotes:
                continue

            used_quotes.add(arabic)

            return f"✨ {arabic}"

        except:
            continue

    return None


def get_post():

    mode = random.random()

    # 40% حب
    if mode < 0.4:
        quote = get_api_quote(LOVE_APIS)
        if quote:
            return quote

    # 40% قوة
    elif mode < 0.8:
        quote = get_api_quote(STRONG_APIS)
        if quote:
            return quote

    # 20% واتساب ستايل
    quote = random.choice(WHATSAPP_STYLE)

    if quote in used_quotes:
        return random.choice(WHATSAPP_STYLE)

    used_quotes.add(quote)

    return quote


def send_to_telegram():

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Missing env vars")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": get_post()
    }

    try:
        requests.post(url, data=payload, timeout=10)
        print("✔ Sent")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":

    while True:
        send_to_telegram()
        time.sleep(60)
