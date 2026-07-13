import os
import time
import random
import requests

# ======================
# 🧠 نظام الذاكرة الفولاذي ضد التكرار
# ======================

USED_QUOTES_FILE = "used_quotes.txt"
used = set()

# التأكد من وجود الملف أو إنشائه تلقائياً لمنع الأخطاء
if not os.path.exists(USED_QUOTES_FILE):
    try:
        with open(USED_QUOTES_FILE, "w", encoding="utf-8") as f:
            f.write("")
    except Exception as e:
        print(f"⚠️ Warning: Could not create memory file: {e}")

if os.path.exists(USED_QUOTES_FILE):
    try:
        with open(USED_QUOTES_FILE, "r", encoding="utf-8") as f:
            used = set(line.strip() for line in f if line.strip())
    except Exception as e:
        print(f"⚠️ Warning: Could not read memory file: {e}")

# ======================
# ✍️ قائمة واسعة من المؤلفين والفلاسفة
# ======================

AUTHORS = [
    "دوستويفسكي 📚", "إرنست همنغواي 📚", "فرجينيا وولف 📚",
    "أوسكار وايلد 📚", "فريدريك نيتشه 📚", "جبران خليل جبران 📚",
    "نجيب محفوظ 📚", "محمود درويش 📚", "جلال الدين الرومي 📚",
    "ألبير كامو 📚", "فرانز كافكا 📚", "إميل سيوران 📚",
    "علي الوردي 📚", "أحمد خالد توفيق 📚", "غسان كنفاني 📚"
]

# ======================
# 🌐 مصادر الإنترنت المباشرة (اقتباسات عربية متجددة)
# ======================

ARABIC_APIS = [
    "https://api.single-developers.software/arabicquotes", 
    "https://api.ahmedhesham.com/quotes/random"
]

# ======================
# 🔥 قائمة ضخمة ومحدثة من العبارات العميقة (Viral & Fallback)
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
    "الهدوء صاخب جداً لمن يملك عقلاً مزدحماً.",
    "نحن لا نربت على كتف أحد، نحن نضم قلوبنا ونصمت.",
    "لا أحد يعلم كم من الصراعات خضتها لتظهر بهذا السلام.",
    "المأساة ليست في رحيل من تحب، بل في رحيلك أنت من نفسك.",
    "قد يواسيك شخص لا يجد من يواسيه، ويداويك شخص جرحه أعمق من جرحك.",
    "نكتب لأننا نعجز عن الصراخ، ولأن الصمت ثقيل جداً.",
    "أشد أنواع المغتربين هو من يغترب داخل وطنه وبيته وجسده.",
    "في نهاية المطاف، لن يتذكر الناس ما قلته، بل سيتذكرون كيف جعلتهم يشعرون.",
    "العزلة ليست كراهية للبشر، بل هي حماية لآخر ما تبقى منا من نقاء.",
    "الأشياء التي نتمنى لو أننا ننساها، هي تحديداً الأشياء التي تصر على البقاء.",
    "الاعتذار المتأخر كالدواء بعد الوفاة، لا قيمة له وإن كان صادقاً.",
    "نصف التعب الذي نشعر به ناتج عن تمسكنا بأشياء كان يفترض بنا التخلي عنها منذ زمن.",
    "الذكريات لا تموت، بل تختبئ في زوايا قلوبنا وتنتظر لحظة ضعف لتلتهمنا."
]

def save_used_quote(text):
    text_clean = text.strip()
    if not text_clean:
        return
    used.add(text_clean)
    try:
        with open(USED_QUOTES_FILE, "a", encoding="utf-8") as f:
            f.write(text_clean + "\n")
    except Exception as e:
        print(f"⚠️ Warning: Could not save quote to file: {e}")

# ======================
# 🤖 توليد متطور للخواطر الفلسفية محلياً
# ======================

def generate_thought():
    subjects = [
        "الصمت", "الخذلان", "الحنين", "الوحدة", "الألم", 
        "الغياب", "النسيان", "الذكريات", "الحب", "الانتظار", 
        "العزلة", "المرآة", "الخوف", "الطريق"
    ]
    templates = [
        "لم أعد أبحث عن {} بل عن نفسي التي فقدتها أثناء الطريق.",
        "كل ما تبقى من {} هو أثر لا يُرى، لكنه يوجع بعمق.",
        "{} علّمني أن الصمت أحيانًا أبلغ من كل كلام يُقال.",
        "تغيّرت نظرتي إلى {} دون أن أشعر، وكأنني أصبحت شخصاً آخر.",
        "لم يعد {} يعني لي ما كان يعنيه من قبل، لقد نضجت بشكل مؤلم.",
        "الهروب من {} هو بداية المواجهة الحقيقية مع الذات.",
        "نعتقد أننا نتجاوز {}، لكننا في الحقيقة نعتاد العيش معه فقط.",
        "أحياناً تكون رغبتنا في الهروب من {} أشد من رغبتنا في البقاء والقتال.",
        "تحت غطاء {}، يختبئ طفل صغير يبحث عن طمأنينة مفقودة.",
        "لا شيء أقسى من أن تجلس بمفردك لتواجه {} دون سلاح."
    ]
    # محاولة توليد خاطرة جديدة لم تُستخدم من قبل
    for _ in range(100):
        thought = random.choice(templates).format(random.choice(subjects))
        if thought not in used:
            return thought
    return random.choice(templates).format(random.choice(subjects))

def classify_content(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["نجاح", "هدف", "حلم", "فشل", "استمر", "قوة", "عزيمة", "طموح", "الأمل"]):
        return "تحفيز وتطوير ذات 🔥"
    elif any(w in text_lower for w in ["عمل", "مال", "تجارة", "بيزنس", "قائد", "وقت", "خطة", "استثمار"]):
        return "بيزنس وإدارة وعمل 💼"
    return "أقوال وحكم عميقة 🧠"

# ======================
# 🚀 دالة الاختيار الفائقة (ممنوع التكرار نهائياً)
# ======================

def pick_content():
    # محاولة جلب اقتباس من الويب أولاً
    random.shuffle(ARABIC_APIS)
    for _ in range(15):
        for api in ARABIC_APIS:
            try:
                res = requests.get(api, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    text = data.get("quote") or data.get("text") or data.get("content")
                    if text:
                        text_clean = text.strip()
                        # فحص شرط التكرار والطول المناسب
                        if text_clean not in used and len(text_clean) > 10:
                            save_used_quote(text_clean)
                            return text_clean, classify_content(text_clean), "live_api"
            except:
                continue

    # الخيار الثاني: توليد خاطرة فلسفية محلياً
    for _ in range(30):
        text = generate_thought()
        if text not in used:
            save_used_quote(text)
            return text, "أقوال وحكم عميقة 🧠", "local_ai"

    # الخيار الثالث: اختيار بوست فيرال مميز غير مكرر
    available_viral = [p for p in VIRAL_POSTS if p not in used]
    if available_viral:
        text = random.choice(available_viral)
        save_used_quote(text)
        return text, "أقوال وحكم عميقة 🧠", "static_viral"
        
    # ملجأ الطوارئ الأخير جداً
    return random.choice(VIRAL_POSTS), "أقوال وحكم عميقة 🧠", "fallback"

# ======================
# 🎨 تنسيق البوست المحدث (اسم القناة ➜ المقولة ➜ الكاتب فقط)
# ======================

def format_post(text, category):
    author = random.choice(AUTHORS)
    # تنظيف النصوص بالكامل من أي وسوم لعدم تخريب كود الـ HTML الخاص بتليجرام
    clean_text = text.replace("<", "&lt;").replace(">", "&gt;").strip()
    
    return f"""📢 <b>لم تقال</b> | @lamtoqal

“ <i>{clean_text}</i> ”

👤— {author}"""

# ======================
# 📩 دالة الإرسال والتحديث (بمحاولات تكرار ذكية)
# ======================

def send_message_with_retry(token, chat_id, payload, max_retries=3):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, data=payload, timeout=15)
            if response.status_code == 200:
                return True, response.text
            print(f"⚠️ Attempt {attempt} failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"⚠️ Attempt {attempt} error: {e}")
        time.sleep(2)  # انتظار بسيط قبل إعادة المحاولة
    return False, "All attempts failed"

def send():
    token = os.getenv("NEW_TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("NEW_TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("❌ Error: NEW_TELEGRAM_BOT_TOKEN and NEW_TELEGRAM_CHAT_ID must be set in Environment Variables.")
        return

    content, category, ctype = pick_content()
    
    payload = {
        "chat_id": chat_id,
        "text": format_post(content, category),
        "parse_mode": "HTML"
    }
    
    # 1️⃣ البدء بإرسال الرسالة إلى تليجرام أولاً
    success, log_msg = send_message_with_retry(token, chat_id, payload)
    
    if success:
        print(f"✅ Success: Posted ({ctype}) successfully to channel!")
    else:
        print(f"❌ Failed: Could not send message. Telegram response: {log_msg}")
        return # إلغاء تحديث الذاكرة إذا لم ينشر البوت شيئاً

    # 2️⃣ تحديث الذاكرة في جيت هوب بأمان بعد نجاح الإرسال
    try:
        os.system("git config --local user.email 'action@github.com'")
        os.system("git config --local user.name 'GitHub Action'")
        os.system("git add used_quotes.txt")
        os.system("git commit -m '🔄 Update used quotes memory' --allow-empty")
        os.system("git push")
        print("💾 Memory successfully synchronized with GitHub Repository.")
    except Exception as git_err:
        print(f"⚠️ Git Sync Warning: Could not push changes to repository: {git_err}")

if __name__ == "__main__":
    send()
