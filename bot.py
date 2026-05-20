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
# ✍️ المؤلفون
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
# 🌐 مصادر الإنترنت المباشرة (اقتباسات عربية متجددة)
# ======================

ARABIC_APIS = [
    "https://api.single-developers.software/arabicquotes", 
    "https://api.ahmedhesham.com/quotes/random"
]

# ======================
# 🔥 العبارات الافتراضية الطارئة (Fallback)
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
    try:
        with open(USED_QUOTES_FILE, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except:
        pass

# ======================
# 🤖 توليد خواطر عربية (AI المدمج)
# ======================

def generate_thought():
    subjects = ["الصمت", "الخذلان", "الحنين", "الوحدة", "الألم", "الغياب", "النسيان", "الذكريات", "الحب"]
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
# 🧠 المصنف الذكي للعبارات الخارجية
# ======================

def classify_content(text):
    text_lower = text.lower()
    
    # تصنيف تحفيز وتطوير ذات
    if any(w in text_lower for w in ["نجاح", "هدف", "حلم", "فشل", "استمر", "قوة", "عزيمة", "طموح"]):
        return "تحفيز وتطوير ذات 🔥"
    
    # تصنيف بيزنس وإدارة
    elif any(w in text_lower for w in ["عمل", "مال", "تجارة", "بيزنس", "قائد", "وقت", "خطة", "استثمار"]):
        return "بيزنس وإدارة وعمل 💼"
    
    # تصنيف افتراضي في حال كانت الخواطر عامة أو فلسفية
    return "أقوال وحكم عميقة 🧠"

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
# 📥 سحب واختيار المحتوى ديناميكيًا من الإنترنت
# ======================

def pick_content():
    global post_counter
    post_counter += 1

    # بوست فيرال مخزن كل 7 مرات لضمان ثبات الجودة
    if post_counter % 7 == 0:
        text = random.choice(VIRAL_POSTS)
        update_stats("viral")
        return text, "تحفيز وتطوير ذات 🔥", "static_viral"

    best = best_content_type()
    r = random.random()

    # المسار الأول: العبارات القوية المخزنة (Viral)
    if best == "viral" or r < 0.30:
        text = random.choice(VIRAL_POSTS)
        if text not in used:
            save_used_quote(text)
        update_stats("viral")
        return text, "أقوال وحكم عميقة 🧠", "static_viral"

    # المسار الثاني: خواطر الذكاء الاصطناعي المبنية محليًا
    if best == "ai" or r < 0.55:
        text = generate_thought()
        if text not in used:
            save_used_quote(text)
        update_stats("ai")
        return text, "أقوال وحكم عميقة 🧠", "local_ai"

    # المسار الثالث: الطيران للإنترنت لجلب محتوى جديد تمامًا وتصنيفه تلقائيًا
    random.shuffle(ARABIC_APIS)
    for api in ARABIC_APIS:
        try:
            res = requests.get(api, timeout=7)
            if res.status_code == 200:
                data = res.json()
                text = data.get("quote") or data.get("text") or data.get("content")
                
                if text and text not in used and len(text) > 10:
                    save_used_quote(text)
                    category = classify_content(text)
                    update_stats("api")
                    return text, category, "live_api"
        except:
            continue

    # في حال فشل الاتصال بالإنترنت تمامًا
    fallback_text = random.choice(VIRAL_POSTS)
    return fallback_text, "أقوال وحكم عميقة 🧠", "fallback"

# ======================
# 🎨 تنسيق البوست بالهيكل الذي تفضله
# ======================

def format_post(text, category):
    author = random.choice(AUTHORS)
    return f"""🌟 *منشور جديد* 🌟

“ {text.strip()} ”

📌 *التصنيف:* {category}
⭐ *المؤلف:* {author} ⭐"""

# ======================
# 📩 إرسال تيليجرام
# ======================

def send():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("❌ Missing env vars")
        return

    content, category, ctype = pick_content()

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": format_post(content, category),
            "parse_mode": "Markdown"
        }
    )

    print(f"✅ Sent ({ctype}) -> Category: {category}")

# ======================
# ⏰ توزيع ذكي للوقت
# ======================

def smart_sleep():
    hour = time.localtime().tm_hour
    if 18 <= hour <= 23:
        return random.randint(170, 240)
    if 12 <= hour < 18:
        return random.randint(300, 480)
    return random.randint(600, 900)

# ======================
# 🚀 تشغيل البوت المستمر
# ======================

if __name__ == "__main__":
    print("🚀 FINAL BOSS BOT WITH LIVE WEB EXTENSION STARTED")
    while True:
        try:
            send()
        except Exception as e:
            print("❌ ERROR:", e)
        time.sleep(smart_sleep())
