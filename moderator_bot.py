import os
import telebot

# جلب توكن البوت من إعدادات جيت هوب السرية
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# قاموس لتخزين آخر رسالة أرسلها كل عضو لمنع التكرار
# الهيكل: { user_id: "نص آخر رسالة" }
last_messages = {}

print("🤖 بوت الحماية والتفاعل يعمل الآن بنجاح...")

# ==========================================
# 1. نظام منع التكرار وحماية الجروب (Anti-Spam)
# ==========================================
@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'])
def handle_group_messages(message):
    user_id = message.from_user.id
    current_text = message.text.strip() if message.text else None

    if current_text:
        # التحقق إذا كانت الرسالة مطابقة تماماً لآخر رسالة أرسلها نفس الشخص
        if user_id in last_messages and last_messages[user_id] == current_text:
            try:
                # حذف الرسالة المكررة فوراً
                bot.delete_message(message.chat.id, message.message_id)
                
                # إرسال تحذير مؤقت للعضو
                warning = bot.send_message(
                    message.chat.id, 
                    f"⚠️ عذراً يا [{message.from_user.first_name}](tg://user?id={user_id})، ممنوع تكرار نفس الرسالة لحماية الجروب من الإزعاج!",
                    parse_mode="Markdown"
                )
                return # التوقف هنا وعدم إكمال الكود للرسالة المكررة
            except Exception as e:
                print(f"❌ لم أتمكن من حذف الرسالة المكررة: {e}")

        # تحديث ذاكرة البوت بآخر رسالة أرسلها هذا العضو
        last_messages[user_id] = current_text

    # ==========================================
    # 2. نظام التفاعل التلقائي الذكي (Reactions)
    # ==========================================
    if current_text:
        text_lower = current_text.lower()
        
        # التفاعل مع التحية والترحيب
        if any(word in text_lower for word in ["سلام", "مرحبا", "أهلاً", "منور", "صباح", "مساء"]):
            try:
                bot.set_message_reaction(message.chat.id, message.message_id, [telebot.types.ReactionTypeEmoji("👋")], is_big=True)
            except:
                pass
                
        # التفاعل مع كلمات الإعجاب أو الشكر
        elif any(word in text_lower for word in ["شكرا", "تسلم", "جميل", "مبدع", "كفو", "عاش"]):
            try:
                bot.set_message_reaction(message.chat.id, message.message_id, [telebot.types.ReactionTypeEmoji("🔥")], is_big=True)
            except:
                pass

        # التفاعل مع الضحك
        elif any(word in text_lower for word in ["هههه", "ههه", "😂", "🤣"]):
            try:
                bot.set_message_reaction(message.chat.id, message.message_id, [telebot.types.ReactionTypeEmoji("😂")])
            except:
                pass

# تشغيل البوت بشكل مستمر لا ينقطع
bot.infinity_polling()
