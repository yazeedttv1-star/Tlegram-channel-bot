import os
import random
import requests

# ======================
# ✍️ المؤلفون
# ======================
AUTHORS = [
    "دوستويفسكي 📚", "إرنست همنغواي 📚", "فرجينيا وولف 📚",
    "أوسكار وايلد 📚", "نيتشه 📚", "جبران خليل جبران 📚"
]

# ======================
# 🌐 مصادر الإنترنت المباشرة (اقتباسات عربية متجددة)
# ======================
ARABIC_APIS = [
    "https://api.single-developers.software/arabicquotes", 
    "https://api.ahmedhesham.com/quotes/random"
]

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

def generate_thought():
    subjects = ["الصمت", "الخذلان", "الحنين", "الوحدة", "الألم", "الغياب", "النسيان", "الذكريات", "الحب"]
    templates = [
        "لم أعد أبحث عن {} بل عن نفسي التي فقدتها أثناء الطريق.",
        "كل ما تبقى من {} هو أثر لا يُرى.",
        "{} علّمني أن الصمت أحيانًا أبلغ من كل شيء.",
        "تغيّرت نظرتي إلى {} دون أن أشعر.",
        "لم يعد {} يعني لي ما كان يعنيه من قبل."
    ]
    return random.choice(templates).format(random.choice(subjects))

def classify_content(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["نجاح", "هدف", "حلم", "فشل", "استمر", "قوة", "عزيمة", "طموح"]):
        return "تحفيز وتطوير ذات 🔥"
    elif any(w in text_lower for w in ["عمل", "مال", "تجارة", "بيزنس", "قائد", "وقت", "خطة", "استثمار"]):
        return "بيزنس وإدارة وعمل 💼"
    return "أقوال وحكم عميقة 🧠"

# ======================
# 🚀 دالة الاختيار الفولاذية (بدون الحاجة لحفظ ملفات)
# ======================
def pick_content():
    r = random.random()

    # 50% يسحب لايف من الإنترنت لتجديد المحتوى بالكامل
    if r < 0.50:
        random.shuffle(ARABIC_APIS)
        for api in ARABIC_APIS:
            try:
                res = requests.get(api, timeout=7)
                if res.status_code == 200:
                    data = res.json()
                    text = data.get("quote") or data.get("text") or data.get("content")
                    if text and len(text) > 10:
                        return text, classify_content(text), "live_api"
            except:
                continue

    # 30% يولد خواطر بالذكاء الاصطناعي
    if r < 0.80:
        return generate_thought(), "أقوال وحكم عميقة 🧠", "local_ai"

    # المتبقي يسحب من الفيرال المخزن
    return random.choice(VIRAL_POSTS), "أقوال وحكم عميقة 🧠", "static_viral"

def format_post(text, category):
    author = random.choice(AUTHORS)
    return f"""🌟 *منشور جديد* 🌟\n\n“ {text.strip()} ”\n\n📌 *التصنيف:* {category}\n⭐ *المؤلف:* {author} ⭐"""

def send():
    token = os.getenv("NEW_TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("NEW_TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("❌ Missing env vars")
        return

    content, category, ctype = pick_content()
    
    # تم إلغاء كل أسطر الـ git push والـ الالتزامات المالية والبرمجية نهائياً 🧼

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": format_post(content, category), "parse_mode": "Markdown"}
    )
    print(f"✅ Sent ({ctype}) -> {category}")

if __name__ == "__main__":
    send()
