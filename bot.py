import os
import time
import random
import requests

used_quotes = set()

APIS = [
    "https://api.quotable.io/random",
    "https://api.quotable.io/random?tags=life",
    "https://api.quotable.io/random?tags=wisdom",
    "https://api.quotable.io/random?tags=inspirational",
    "https://zenquotes.io/api/random"
]

EMO = ["🖤", "🌙", "✨", "🤍"]

FOOTER = [
    "\n\n🖤 لو الكلام لمسّك، شاركه.",
    "\n\n✨ يمكن غيرك محتاجه.",
    "\n\n🌙 بعض الكلام مش بيتقال مرتين.",
    "\n\n🤍 لو فهمت، أنت مش لوحدك."
]

BLOCKED = ["doctor", "medical", "health", "مرض", "طبيب", "علاج"]


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


def get_quote():

    for _ in range(10):

        api = random.choice(APIS)

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

            # منع التكرار
            if arabic in used_quotes:
                continue

            used_quotes.add(arabic)

            return arabic

        except:
            continue

    # fallback ستايل مشاعر
    fallback = [
        "فيه حاجات بنحسها ومش بنعرف نقولها.",
        "الهدوء اللي جواك مش دايمًا راحة… أحيانًا تعب.",
        "مش كل اللي ساكت قوي، أحيانًا هو بس مستسلم.",
        "بعض المشاعر مش بتخف… بس بنتعود عليها."
    ]

    return random.choice(fallback)


def build_post():

    emoji = random.choice(EMO)
    quote = get_quote()

    return f"{emoji} {quote}" + random.choice(FOOTER)


def send_to_telegram():

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Missing env vars")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": build_post()
    }

    try:
        requests.post(url, data=payload, timeout=10)
        print("Sent ✔")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":

    while True:

        send_to_telegram()

        # ⏱️ من 5 إلى 10 دقائق عشوائي
        time.sleep(random.randint(300, 600))
