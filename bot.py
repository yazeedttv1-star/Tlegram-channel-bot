import os
import time
import random
import requests
from collections import deque, defaultdict

# ======================
# 🧠 Memory System
# ======================

used = deque(maxlen=400)
post_counter = 0

# 📊 محاكاة التفاعل الحقيقي
stats = {
    "viral": {"sent": 0, "score": 1.0},
    "ai": {"sent": 0, "score": 1.0},
    "api": {"sent": 0, "score": 1.0}
}

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
    "https://api.quotable.io/random?tags=inspirational"
]

VIRAL_POSTS = [
    "أخطر ما في الحياة أنك تعتاد الألم وتظنه طبيعيًا.",
    "هناك نسخ منك ماتت بصمت ولم يلاحظها أحد.",
    "أسوأ شعور أن تتغير دون أن يشعر بك أحد.",
    "كل شيء واضح إلا ما يحدث داخلك.",
    "بعض النهايات تبدأ من الداخل دون أن نشعر."
]


# ======================
# 🤖 توليد عربي احترافي
# ======================

def generate_thought():

    subjects = ["الصمت", "الخذلان", "الحنين", "الوحدة", "الألم", "الغياب"]

    templates = [
        "لم أعد أبحث عن {} بل عن نفسي التي فقدتها أثناء الطريق.",
        "كل ما تبقى من {} هو أثر لا يُرى.",
        "{} علّمني أن الصمت أحيانًا أبلغ من كل شيء.",
        "تغيّرت نظرتي إلى {} دون أن أشعر.",
        "لم يعد {} يعني لي ما كان يعنيه من قبل."
    ]

    return random.choice(templates).format(random.choice(subjects))


# ======================
# 🌐 API
# ======================

def extract(api, data):
    if "quotable.io" in api:
        return data.get("content")
    return None


def translate(text):
    try:
        r = requests.get(
            "https://translate.googleapis.com/translate_a/single",
            params={
                "client": "gtx",
                "sl": "en",
                "tl": "ar",
                "dt": "t",
                "q": text
            },
            timeout=10
        )
        return r.json()[0][0][0]
    except:
        return None


# ======================
# 📊 تقييم الأداء (Fake Engagement Engine)
# ======================

def update_stats(content_type):

    # نحاكي التفاعل (زي مشاهدات/حفظ/مشاركة)
    fake_engagement = random.uniform(0.5, 1.5)

    stats[content_type]["sent"] += 1
    stats[content_type]["score"] += fake_engagement


def best_content_type():

    return max(stats.items(), key=lambda x: x[1]["score"])[0]


# ======================
# 🔥 اختيار ذكي نهائي
# ======================

def pick_content():

    global post_counter
    post_counter += 1

    # 🔥 بوست فيروسي إجباري
    if post_counter % 7 == 0:
        update_stats("viral")
        return random.choice(VIRAL_POSTS), "viral"

    best = best_content_type()

    r = random.random()

    # 🎯 يعتمد على الأداء الفعلي
    if best == "viral" or r < 0.35:
        update_stats("viral")
        return random.choice(VIRAL_POSTS), "viral"

    if best == "ai" or r < 0.65:
        update_stats("ai")
        return generate_thought(), "ai"

    # 🌐 API
    for _ in range(10):

        api = random.choice(APIS)

        try:
            res = requests.get(api, timeout=10)

            if res.status_code != 200:
                continue

            data = res.json()
            text = extract(api, data)

            if not text:
                continue

            ar = translate(text) or text

            if ar in used:
                continue

            used.append(ar)
            update_stats("api")

            return ar, "api"

        except:
            continue

    return "الصمت أبلغ من الكلام أحيانًا.", "api"


# ======================
# 🎨 تنسيق احترافي ثابت
# ======================

def format_post(text):

    author = random.choice(AUTHORS)

    return f"""|| ✨ لم تُقال بعد ✨ ||

{text}

⭐ {author} ⭐"""


# ======================
# 📩 إرسال تيليجرام
# ======================

def send():

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Missing env vars")
        return

    content, ctype = pick_content()

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": format_post(content),
            "parse_mode": "Markdown"
        }
    )

    print(f"Sent ✔ ({ctype})")


# ======================
# ⏰ توزيع احترافي نهائي
# ======================

def smart_sleep():

    hour = time.localtime().tm_hour

    # 🔥 peak
    if 18 <= hour <= 23:
        return random.randint(170, 240)

    # 🌤️ normal
    if 12 <= hour < 18:
        return random.randint(300, 480)

    # 🌙 low
    return random.randint(600, 900)


# ======================
# 🚀 تشغيل النظام
# ======================

if __name__ == "__main__":

    print("🚀 FINAL BOSS BOT STARTED")

    while True:
        send()
        time.sleep(smart_sleep())
