import os
import time
import random
import requests

# ======================
# 🧠 نظام الذاكرة الفولاذي ضد التكرار
# ======================

USED_QUOTES_FILE = "used_quotes.txt"
used = set()

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
# ✍️ قائمة الكتاب والمؤلفين
# ======================

AUTHORS = [
    "دوستويفسكي 📚", "إرنست همنغواي 📚", "فرجينيا وولف 📚",
    "أوسكار وايلد 📚", "فريدريك نيتشه 📚", "جبران خليل جبران 📚",
    "نجيب محفوظ 📚", "محمود درويش 📚", "جلال الدين الرومي 📚",
    "ألبير كامو 📚", "فرانز كافكا 📚", "إميل سيوران 📚",
    "علي الوردي 📚", "أحمد خالد توفيق 📚", "غسان كنفاني 📚"
]

# ======================
# 🌐 مصادر الإنترنت المفتوحة والموسعة (APIs المتعددة)
# ======================

ARABIC_APIS = [
    "https://api.single-developers.software/arabicquotes", 
    "https://api.ahmedhesham.com/quotes/random",
    "https://raw.githubusercontent.com/HeshamHaroon/arabic-quotes/main/quotes.json", # مستودع خارجي ضخم للاقتباسات
    "https://api.aladhan.com/v1/gToH" # مستخدم أحياناً كبوابة طوارئ لقيم متغيرة
]

# ======================
# 🔥 قائمة ضخمة ومحدثة من العبارات العميقة والشهيرة (Viral & Fallback)
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
    "العزلة ليست كراهية للبشر، بل هي حماية لآخر ما تبقى منا من نقاء.",
    "الأشياء التي نتمنى لو أننا ننساها، هي تحديداً الأشياء التي تصر على البقاء.",
    "الاعتذار المتأخر كالدواء بعد الوفاة، لا قيمة له وإن كان صادقاً.",
    "نصف التعب الذي نشعر به ناتج عن تمسكنا بأشياء كان يفترض بنا التخلي عنها منذ زمن.",
    "الذكريات لا تموت، بل تختبئ في زوايا قلوبنا وتنتظر لحظة ضعف لتلتهمنا.",
    "أكثر الأشياء إرهاقاً للمرء هو التظاهر بعكس ما يشعر به تماماً.",
    "أحياناً تبكي ليس لأنك ضعيف، بل لأنك مارست القوة والتحمل لفترة طويلة جداً.",
    "الصمت هو النص الأكثر صخباً في قاموس المتعبين.",
    "لا تجبر أحداً على البقاء بجانبك، فالأشياء الجميلة تأتي دون طلب."
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
# 🤖 مولد الخواطر الذكي المتعدد اللغات والتركيبات (تأليف تلقائي)
# ======================

def generate_thought():
    subjects = [
        "الصمت", "الخذلان", "الحنين", "الوحدة", "الألم", 
        "الغياب", "النسيان", "الذكريات", "الحب", "الانتظار", 
        "العزلة", "المرآة", "الخوف", "الطريق", "الوقت", "الندم"
    ]
    
    feelings = [
        "يوجع بعمق", "يرسم في دواخلنا طريقاً مجهولاً", "يأتي على هيئة غصة صامتة",
        "يسرق منا أجمل سنوات العمر", "يجعلنا غرباء في تفاصيلنا اليومية",
        "يعيد صياغة انكساراتنا القديمة بكل دقة"
    ]
    
    templates = [
        "لم أعد أبحث عن {} بل عن نفسي التي فقدتها أثناء الطريق.",
        "كل ما تبقى من {} هو أثر لا يُرى، لكنه {}.",
        "{} علّمني أن الصمت أحيانًا أبلغ من كل كلام يُقال.",
        "تغيّرت نظرتي إلى {} دون أن أشعر، وكأنني أصبحت شخصاً آخر.",
        "لم يعد {} يعني لي ما كان يعنيه من قبل، لقد نضجت بشكل مؤلم.",
        "الهروب من {} هو بداية المواجهة الحقيقية مع الذات والماضي.",
        "نعتقد أننا نتجاوز {}، لكننا في الحقيقة نعتاد العيش معه فقط.",
        "أحياناً تكون رغبتنا في الهروب من {} أشد من رغبتنا في البقاء والقتال.",
        "تحت غطاء {}، يختبئ طفل صغير يبحث عن طمأنينة مفقودة.",
        "لا شيء أقسى من أن تجلس بمفردك لتواجه {} دون سلاح.",
        "كان {} معبراً وحيداً إلى زاوية الطمأنينة التي لم نصل إليها قط.",
        "حين يتسلل {} إلى تفاصيلنا، ندرك مدى هشاشة الوعود التي صدقناها."
    ]
    
    # محاولة توليد تركيبات نادرة ومميزة لم تنشر من قبل
    for _ in range(150):
        tmpl = random.choice(templates)
        subj = random.choice(subjects)
        feel = random.choice(feelings)
        
        # دمج الكلمات حسب القالب المختار
        if "{}" in tmpl:
            if tmpl.count("{}") == 2:
                thought = tmpl.format(subj, feel)
            else:
                thought = tmpl.format(subj)
        else:
            thought = tmpl
            
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
# 🚀 دالة الاختيار الفائقة (مقاومة للتكرار والأعطال)
# ======================

def pick_content():
    # المسار الأول: جلب وتصفية الاقتباسات من مصادر الويب عشوائياً
    random.shuffle(ARABIC_APIS)
    for api in ARABIC_APIS:
        try:
            res = requests.get(api, timeout=6)
            if res.status_code == 200:
                data = res.json()
                text = None
                
                # التعامل مع هياكل البيانات المختلفة للـ APIs
                if isinstance(data, list):
                    # إذا كانت الاستجابة عبارة عن قائمة كبيرة من الملفات الجاهزة
                    item = random.choice(data)
                    text = item.get("quote") or item.get("text") or item.get("content")
                elif isinstance(data, dict):
                    text = data.get("quote") or data.get("text") or data.get("content")
                
                if text:
                    text_clean = text.strip()
                    if text_clean not in used and len(text_clean) > 10:
                        save_used_quote(text_clean)
                        return text_clean, classify_content(text_clean), "live_api"
        except:
            continue

    # المسار الثاني: تأليف الذكاء الاصطناعي المحلي الفريد
    for _ in range(50):
        text = generate_thought()
        if text not in used:
            save_used_quote(text)
            return text, "أقوال وحكم عميقة 🧠", "local_ai"

    # المسار الثالث: البحث في بنك العبارات المخزنة داخلياً
    available_viral = [p for p in VIRAL_POSTS if p not in used]
    if available_viral:
        text = random.choice(available_viral)
        save_used_quote(text)
        return text, "أقوال وحكم عميقة 🧠", "static_viral"
        
    return random.choice(VIRAL_POSTS), "أقوال وحكم عميقة 🧠", "fallback"

# ======================
# 🎨 التنسيق المطلوب بدقة (اسم القناة ➜ المقولة ➜ الكاتب فقط)
# ======================

def format_post(text, category):
    author = random.choice(AUTHORS)
    clean_text = text.replace("<", "&lt;").replace(">", "&gt;").strip()
    
    return f"""🗓️ <b>لم تقال</b> | @lamtoqal

“ <i>{clean_text}</i> ”

📍👑— {author}"""

# ======================
# 📩 دالة الإرسال مع آليات الحماية والتكرار
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
        time.sleep(2)
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
    
    # 1️⃣ النشر المباشر في تليجرام
    success, log_msg = send_message_with_retry(token, chat_id, payload)
    
    if success:
        print(f"✅ Success: Posted ({ctype}) successfully to channel!")
    else:
        print(f"❌ Failed: Could not send message. Telegram response: {log_msg}")
        return

    # 2️⃣ تحديث قائمة المقولات المستخدمة على GitHub لضمان عدم التكرار مستقبلاً
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
