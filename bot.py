import os
import time
import random
import requests

used_quotes = set()

# ====== 5 APIs اقتباسات ======
QUOTE_APIS = [
    "https://api.quotable.io/random",
    "https://zenquotes.io/api/random",
    "https://api.adviceslip.com/advice",
    "https://api.quotable.io/random?tags=wisdom",
    "https://api.quotable.io/random?tags=inspirational"
]

# ====== عبارات واتساب ستايل ======
WHATSAPP_STYLE = [
    "✨ الهدوء اللي وصلتله بعد كل اللي عديت بيه يستحق الاحترام.",
    "🖤 مش كل حاجة تستاهل رد.",
    "⚡ الراحة النفسية أهم من أي حاجة.",
    "🌙 اتعلمت أمشي لوحدي من غير ما أندم.",
    "🔥 في ناس وجودهم درس مش راحة.",
    "🤍 اختار نفسك حتى لو الكل عكسك.",
    "✨ السكوت أحيانًا أذكى قرار.",
    "🖤 مش لازم تشرح نفسك دايمًا.",
    "⚡ كل واحد شايل اللي محدش شايفه.",
    "🌙 الوجع بيعلمك تبقى أقوى."
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

    if "quotable.io" in api:
        return data.get("content")

    if "zenquotes" in api:
        return data[0].get("q")

    if "adviceslip" in api:
        return data["slip"]["advice"]

    return None


def get_api_quote():

    for _ in range(10):

        api = random.choice(QUOTE_APIS)

        try:
            r = requests.get(api, timeout=10)

            if r.status_code != 200:
                continue

            data = r.json()
            text = extract_quote(api, data)

            if not text:
                continue

            arabic = translate(text) or text

            if arabic in used_quotes:
                continue

            used_quotes.add(arabic)

            return f"✨ {arabic}"

        except:
            continue

    return None


def get_whatsapp_quote():

    remaining = list(set(WHATSAPP_STYLE) - used_quotes)

    if not remaining:
        used_quotes.clear()
        remaining = WHATSAPP_STYLE.copy()

    quote = random.choice(remaining)

    used_quotes.add(quote)

    return quote


def get_post():

    # توزيع ذكي:
    # 60% واتساب ستايل
    # 40% اقتباسات من API

    if random.random() < 0.6:
        return get_whatsapp_quote()

    api_quote = get_api_quote()

    if api_quote:
        return api_quote

    return get_whatsapp_quote()


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


# ====== تشغيل كل دقيقة ======
if __name__ == "__main__":

    while True:
        send_to_telegram()
        time.sleep(60)  # كل دقيقة
