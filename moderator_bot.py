import os
import random
import requests

# ======================
# 🧠 نظام الذاكرة الفولاذي ضد التكرار
# ======================

USED_QUOTES_FILE = "used_quotes.txt"
used = set()

if os.path.exists(USED_QUOTES_FILE):
    with open(USED_QUOTES_FILE, "r", encoding="utf-8") as f:
        used = set(line.strip() for line in f if line.strip())

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

def save_used_quote(text):
    used.add(text)
    try:
        with open(USED_QUOTES_FILE, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except:
        pass

def generate_thought():
    subjects = ["الصمت", "الخذلان", "الحنين", "الوحدة", "الألم", "الغياب", "النسيان", "الذكريات", "الحب"]
    templates = [
        "لم أعد أبحث عن {} بل عن نفسي التي فقدتها أثناء الطريق.",
        "كل ما تبقى من {} هو أثر لا يُرى.",
        "{} علّمني أن الصمت أحيانًا أبلغ من كل شيء.",
        "تغيّرت نظرتي إلى {} دون أن أشعر.",
        "لم يعد {} يعني لي ما كان يعنيه من قبل."
    ]
    # محاولة توليد خاطرة جديدة لم تُستخدم من قبل
    for _ in range(50):
        thought = random.choice(templates).format(random.choice(subjects))
        if thought not in used:
            return thought
    return random.choice(templates).format(random.choice(subjects))

def classify_content(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["نجاح", "هدف", "حلم", "فشل", "استمر", "قوة", "عزيمة", "طموح"]):
        return "تحفيز وتطوير ذات 🔥"
    elif any(w in text_lower for w in ["عمل", "مال", "تجارة", "بيزنس", "قائد", "وقت", "خطة", "استثمار"]):
        return "بيزنس وإدارة وعمل 💼"
    return "أقوال وحكم عميقة 🧠"

# ======================
# 🚀 دالة الاختيار الـ Max (ممنوع التكرار نهائياً)
# ======================
def pick_content():
    # بنجرب 30 مرة "نطير" على الإنترنت نجيب جملة جديدة تماماً ومش موجودة في الذاكرة
    random.shuffle(ARABIC_APIS)
    for _ in range(30):
        for api in ARABIC_APIS:
            try:
                res = requests.get(api, timeout=7)
                if res.status_code == 200:
                    data = res.json()
                    text = data.get("quote") or data.get("text") or data.get("content")
                    # شرط صارم: لازم النص ميكونش اتنشر قبل كده وطوله مناسب
                    if text and text.strip() not in used and len(text) > 10:
                        save_used_quote(text.strip())
                        return text, classify_content(text), "live_api"
            except:
                continue

    # لو الإنترنت علق أو ملقاش جديد، بنروح للذكاء الاصطناعي يولد حاجة جديدة
    text = generate_thought()
    if text not in used:
        save_used_quote(text)
        return text, "أقوال وحكم عميقة 🧠", "local_ai"

    # لو كل الخطوط قفلت، بينقي بوست من الفيرال بشرط ميكونش اتكرر
    available_viral = [p for p in VIRAL_POSTS if p not in used]
    if available_viral:
        text = random.choice(available_viral)
        save_used_quote(text)
        return text, "أقوال وحكم عميقة 🧠", "static_viral"
        
    # fallback أخير جداً إذا امتلأت الذاكرة تماماً
    return random.choice(VIRAL_POSTS), "أقوال وحكم عميقة 🧠", "fallback"

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
    
    # تحديث ملف الذاكرة في جيت هوب تلقائياً عشان يفتكر المنشورات اللي نزلت
    os.system("git config --local user.email 'action@github.com'")
    os.system("git config --local user.name 'GitHub Action'")
    os.system("git add used_quotes.txt")
    os.system("git commit -m '🔄 Update used quotes memory' --allow-empty")
    os.system("git push")

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": format_post(content, category), "parse_mode": "Markdown"}
    )
    print(f"✅ Sent ({ctype}) -> {category}")

if __name__ == "__main__":
    send()
