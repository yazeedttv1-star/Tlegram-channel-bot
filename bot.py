import os
import random
import requests

# قاعدة بيانات العبارات الثابتة
QUOTES = {
    "تحفيز وتطوير": [
        "🔥 الاستمرار في السعي هو ما يصنع الفارق، النجاح ليس ضربة حظ بل رحلة التزام يومية.",
        "🚀 لا تنتظر الظروف المثالية لتبرز، اصنع أنت واقعك وابدأ بالمتوفر لديك الآن.",
        "💪 العظمة لا تأتي من عدم السقوط أبدًا، بل من النهوض في كل مرة نسقط فيها."
    ],
    "بيزنس وإدارة": [
        "💼 التجارة والبيزنس لا يعتمدان على الأفكار فقط، بل على جودة وفن التنفيذ في أرض الواقع.",
        "📊 المستثمر الذكي لا يضع البيض كله في سلة واحدة، التنويع هو درع الأمان المالي.",
        "🎯 إذا لم تكن لديك خطة واضحة لعملك، فأنت للأسف تخطط للفشل دون أن تشعر."
    ],
    "أقوال وحكم عميقة": [
        "🧠 حكمة اليوم: 'الصمت في بعض المواقف ليس ضعفاً، بل هو قمة الذكاء والترفع.'",
        "⏳ الوقت هو العملة الوحيدة التي تنفقها ولا يمكن استردادها، أحسن إدارة عملتك.",
        "🌱 الشيء الوحيد الثابت في الحياة هو التغيير المستمر، تكيّف تنجح."
    ]
}

def get_random_quote():
    category = random.choice(list(QUOTES.keys()))
    quote = random.choice(QUOTES[category])
    return f"🌟 *منشور جديد* 🌟\n\n{quote}\n\n📌 *التصنيف:* {category}"

def send_to_telegram():
    # جلب التوكن ومعرف القناة من إعدادات جيت هوب بأمان
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") # معرف القناة (مثال: @my_channel)

    if not bot_token or not chat_id:
        print("❌ خطأ: لم يتم ضبط المتغيرات السرية في جيت هوب.")
        return

    # رابط الـ API الخاص بتليجرام لإرسال الرسائل
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    data = {
        "chat_id": chat_id,
        "text": get_random_quote(),
        "parse_mode": "Markdown" # عشان يقبل التنسيق العريض والإيموجي
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("✅ تم نشر العبارة بنجاح في قناة التليجرام!")
    else:
        print(f"❌ فشل النشر: {response.text}")

if __name__ == "__main__":
    send_to_telegram()
