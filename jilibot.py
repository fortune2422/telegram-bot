from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Bot
from telegram.error import TelegramError

# 把这行换成你自己的 Bot Token
TOKEN = "8331605813:AAFHs5vaFopD72LZOD-c1YsD4Ug2E47mbwg"
bot = Bot(token=TOKEN)

try:
    # 清除之前的 webhook 或 polling 实例
    bot.delete_webhook(drop_pending_updates=True)
    print("✅ 已清除之前的会话，避免冲突")
except TelegramError as e:
    print(f"⚠️ 清除失败：{e}")


# 替换成你们网站的地址
REGISTER_URL = "https://jili707.co/register"
OFFICIAL_URL = "https://jili707.co"
CUSTOMER_SERVICE_URL = "https://magweb.meinuoka.com/Web/im.aspx?_=t&accountid=133283"
IOS_DOWNLOAD_URL = "https://images.6929183.com/wsd-images-prod/jili707f2/merchant_resource/mobileconfig/jili707f2_2.4.3_20250725002905.mobileconfig"
ANDROID_DOWNLOAD_URL = "https://images.847830.com/wsd-images-prod/jili707f2/merchant_resource/android/jili707f2_2.4.68_20250725002907.apk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🎮 Registre uma conta", url=REGISTER_URL),
            InlineKeyboardButton("🟢 Link do site oficial", url=OFFICIAL_URL),
        ],
        [
            InlineKeyboardButton("📱 ANDROID DOWNLOAD", url=ANDROID_DOWNLOAD_URL),
            InlineKeyboardButton("📱🍏 IOS DOWNLOAD", url=IOS_DOWNLOAD_URL),
        ],
        [
            InlineKeyboardButton("🧑‍💼 atendimento ao Cliente", url=CUSTOMER_SERVICE_URL),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = (
        "Bem-vindo ao bot oficial do jili707.co, um produto de apostas baseado na plataforma jili707.\n"
        "Aqui, você pode experimentar toda a emoção das apostas e ainda participar de campanhas de promoção，\n"
        "para ganhar grandes prêmios em dinheiro.。\n\n"
        "Seja bem-vindo ao bot oficial de apostas do Jili707!。"
    )

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

if __name__ == '__main__':
    # 替换为你的 BotFather 提供的 token
    app = ApplicationBuilder().token("8331605813:AAFHs5vaFopD72LZOD-c1YsD4Ug2E47mbwg").build()
    
    app.add_handler(CommandHandler("start", start))

    print("🤖 Bot is running...")
    app.run_polling()
