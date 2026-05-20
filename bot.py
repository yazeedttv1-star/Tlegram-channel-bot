import os
import time
import random
import requests
from collections import defaultdict

# ======================
# 🧠 Memory System
# ======================

USED_QUOTES_FILE = "used_quotes.txt"

used = set()

if os.path.exists(USED_QUOTES_FILE):
    with open(USED_QUOTES_FILE, "r", encoding="utf-8") as f:
        used = set(line.strip() for line in f if line.strip())

post_counter = 0

stats = {
    "viral": {"sent": 0, "score": 1.0},
    "ai": {"sent": 0, "score": 1.0},
    "api": {"sent": 0, "score": 1.0}
}

# ======================
# ✍️ المؤلفين
# ======================

AUTHORS = [
    "دوستويفسكي 📚",
    "إرنست همنغواي 📚",
    "فرجينيا وولف 📚",
    "أوسكار وايلد 📚",
    "نيتشه 📚",
    "جبران خليل جبران 📚"
]

# ======================
# 🌐 APIs كثيرة
# ======================

APIS = [
    "https://api.quotable.io/random",
    "https://api.quotable.io/random?tags=wisdom",
    "https://api.quotable.io/random?tags=life",
    "https://api.quotable.io/random?tags=inspirational",
    "https://api.quotable.io/random?tags=happiness",
    "https://api.quotable.io/random?tags=success",
]

# ======================
# 🔥 Viral Posts
# ======================

VIRAL_POSTS = [
    "أخطر ما في الحياة أنك تعتاد الألم وتظنه طبيعيًا.",
    "هناك نسخ منك ماتت بصمت ولم يلاحظها أحد.",
    "أسوأ شعور أن تتغير دون أن يشعر بك أحد.",
    "كل شيء واضح إلا ما يحدث داخلك.",
    "بعض النهايات تبدأ من الداخل دون أن نشعر.",
    "أحيانًا لا ينقصنا شيء سوى شخص يفهم صمتنا.",
    "الخذلان لا يأتي من الغرباء أبدًا.",
    "كل الذين نجوا كانوا يحملون شيئًا مكسورًا بداخلهم.",
]

# ======================
# 💾 حفظ الاقتباسات
# ======================

def save_used_quote(text):

    used.add(text)

    with open(USED_QUOTES_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


# ======================
# 🤖 توليد خواطر عربية
# ======================

def generate_thought():

    subjects = [
        "الصمت",
        "الخذلان",
        "الحنين",
        "الوحدة",
        "الألم",
        "الغياب",
        "النسيان",
        "الذكريات",
        "الحب"
    ]

    templates = [
        "لم أعد أبحث عن {} بل عن نفسي التي فقدتها أثناء الطريق.",
        "كل ما تبقى من {} هو أثر لا يُرى.",
        "{} علّمني أن الصمت أحيانًا أبلغ من كل شيء.",
        "تغيّرت نظرتي إلى {} دون أن أشعر.",
        "لم يعد {} يعني لي ما كان يعنيه من قبل.",
        "أحيانًا يكون {} أثقل من الكلام نفسه.",
        "ما زلت أحاول النجاة من {} حتى الآن."
    ]

    return random.choice(templates).format(random.choice(subjects))


# ======================
# 🌐 ترجمة
# ======================

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

        if r.status_code == 200:
            return r.json()[0][0][0]

    except:
        pass

    return None


# ======================
# 📥 استخراج API
# ======================

def extract(api, data):

    if "quotable.io" in api:
        return data.get("content")

    return None


# ======================
# 📊 تحليل الأداء
# ======================

def update_stats(content_type):

    fake_engagement = random.uniform(0.5, 1.5)

    stats[content_type]["sent"] += 1
    stats[content_type]["score"] += fake_engagement


def best_content_type():

    return max(stats.items(), key=lambda x: x[1]["score"])[0]


# ======================
# 🧠 اختيار المحتوى
# ======================

def pick_content():

    global post_counter

    post_counter += 1

    # 🔥 بوست قوي كل 7 مرات
    if post_counter % 7 == 0:

        text = random.choice(VIRAL_POSTS)

        update_stats("viral")

        return text, "viral"

    best = best_content_type()

    r = random.random()

    # 🔥 Viral
    if best == "viral" or r < 0.35:

        text = random.choice(VIRAL_POSTS)

        if text not in used:
            save_used_quote(text)

        update_stats("viral")

        return text, "viral"

    # 🤖 AI عربي
    if best == "ai" or r < 0.65:

        text = generate_thought()

        if text not in used:
            save_used_quote(text)

        update_stats("ai")

        return text, "ai"

    # 🌐 API
    for _ in range(20):

        api = random.choice(APIS)

        try:

            res = requests.get(api, timeout=10)

            if res.status_code != 200:
                continue

            data = res.json()

            text = extract(api, data)

            if not text:
                continue

            arabic = translate(text) or text

            if arabic in used:
                continue

            save_used_quote(arabic)

            update_stats("api")

            return arabic, "api"

        except:
            continue

    return "الصمت أبلغ من الكلام أحيانًا.", "fallback"


# ======================
# 🎨 تنسيق البوست
# ======================

def format_post(text):

    author = random.choice(AUTHORS)

    return f"""*|| ✨ لم تُقال بعد ✨ ||*

{text}

*⭐ {author} ⭐*"""


# ======================
# 📩 إرسال تيليجرام
# ======================

def send():

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("❌ Missing env vars")
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

    print(f"✅ Sent ({ctype})")


# ======================
# ⏰ توزيع ذكي
# ======================

def smart_sleep():

    hour = time.localtime().tm_hour

    # 🔥 وقت الذروة
    if 18 <= hour <= 23:
        return random.randint(170, 240)

    # 🌤️ وقت متوسط
    if 12 <= hour < 18:
        return random.randint(300, 480)

    # 🌙 وقت هادئ
    return random.randint(600, 900)


# ======================
# 🚀 تشغيل البوت
# ======================

if __name__ == "__main__":

    print("🚀 FINAL BOSS BOT STARTED")

    while True:

        try:
            send()

        except Exception as e:
            print("❌ ERROR:", e)

        time.sleep(smart_sleep())
