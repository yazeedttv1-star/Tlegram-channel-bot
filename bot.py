import os
import time
import random
import requests

used = set()

AUTHORS = [
    "دوستويفسكي 📚",
    "إرنست همنغواي 📚",
    "فرجينيا وولف 📚",
    "أوسكار وايلد 📚",
    "نيتشه 📚",
    "جبران خليل جبران 📚"
]

APIS = [
    "https://api.quotable.io/random",
    "https://api.quotable.io/random?tags=wisdom",
    "https://api.quotable.io/random?tags=life",
    "https://api.quotable.io/random?tags=inspirational",
    "https://zenquotes.io/api/random"
]

# 🔥 بوستات فيروسيه جاهزة (تشد الانتباه وتنتشر)
VIRAL_POSTS = [
    "أخطر شيء في الحياة أن تتعود على الألم وتظنه طبيعيًا.",
    "لا أحد يخبرك أن بعض النهايات تبدأ من الداخل أولًا.",
    "تظن أنك قوي… حتى تواجه نفسك وحدك.",
    "هناك نسخ منك ماتت بصمت ولم يلاحظها أحد.",
    "أسوأ شعور أن تتغير دون أن يشعر بك أحد.",
    "كل شيء واضح… إلا ما يحدث داخلك."
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


def extract(api, data):
    if "quotable.io" in api:
        return data.get("content")
    if "zenquotes" in api:
        return data[0].get("q")
    return None


def get_quote():

    # 🔥 30% بوستات فيروسيه
    if random.random() < 0.3:
        return random.choice(VIRAL_POSTS)

    # 🌐 باقي الوقت من API
    for _ in range(15):

        api = random.choice(APIS)

        try:
            r = requests.get(api, timeout=10)

            if r.status_code != 200:
                continue

            data = r.json()
            text = extract(api, data)

            if not text:
                continue

            arabic = translate(text) or text

            if arabic in used:
                continue

            used.add(arabic)

            return arabic

        except:
            continue

    return "الصمت أبلغ من الكلام أحيانًا."


# 🎨 فريمات احترافية (تجذب الانتباه)
def format_post(text):

    author = random.choice(AUTHORS)

    frames = [

f"""━━━━━━━━━━━━━━
✨ لم تُقال بعد ✨
━━━━━━━━━━━━━━

{text}

━━━━━━━━━━━━━━
{author}
━━━━━━━━━━━━━━""",

f"""❖━━━━━━ لم تُقال بعد ━━━━━━❖

{text}

❖━━━━━━━━━━━━━━❖
{author}"""
    ]

    return random.choice(frames)


def send():

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    post = format_post(get_quote())

    requests.post(url, data={
        "chat_id": chat_id,
        "text": post
    })

    print("Sent ✔")


if __name__ == "__main__":

    while True:
        send()
        time.sleep(240)  # كل 4 دقائق
