from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import telegram
import os

print("🔍 当前 python-telegram-bot 版本:", telegram.__version__)

# Telegram Bot Token
TOKEN = "8331605813:AAFHs5vaFopD72LZOD-c1YsD4Ug2E47mbwg"

# Webhook domain
WEBHOOK_DOMAIN = "https://telegram-bot-45rt.onrender.com"

# URLs
REGISTER_URL = "https://jili707.co/register"
OFFICIAL_URL = "https://jili707.co"
CUSTOMER_SERVICE_URL = "https://magweb.meinuoka.com/Web/im.aspx?_=t&accountid=133283"
IOS_DOWNLOAD_URL = "https://images.6929183.com/wsd-images-prod/jili707f2/merchant_resource/mobileconfig/jili707f2_2.4.3_20250725002905.mobileconfig"
ANDROID_DOWNLOAD_URL = "https://images.847830.com/wsd-images-prod/jili707f2/merchant_resource/android/jili707f2_2.4.68_20250725002907.apk"

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            KeyboardButton("🎮 Registre uma conta", url=REGISTER_URL),
            KeyboardButton("🟢 Link do site oficial", url=OFFICIAL_URL)
        ],
        [
            KeyboardButton("📱 ANDROID DOWNLOAD", url=ANDROID_DOWNLOAD_URL),
            KeyboardButton("📱🍏 IOS DOWNLOAD", url=IOS_DOWNLOAD_URL)
        ],
        [
            KeyboardButton("🧑‍💼 atendimento ao Cliente", url=CUSTOMER_SERVICE_URL)
        ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    text = (
        "Bem-vindo ao bot oficial do jili707.co, um produto de apostas baseado na plataforma jili707.\n"
        "Aqui, você pode experimentar toda a emoção das apostas e ainda participar de campanhas de promoção,\n"
        "para ganhar grandes prêmios em dinheiro.\n\n"
        "Seja bem-vindo ao bot oficial de apostas do Jili707!"
    )
    await update.message.reply_text(text, reply_markup=reply_markup)

# 设置 Bot 菜单命令
async def set_bot_commands(application):
    commands = [
        BotCommand("register", "🎮 Registre uma conta"),
        BotCommand("site", "🟢 Link do site oficial"),
        BotCommand("cliente", "🧑‍💼 atendimento ao Cliente"),
        BotCommand("android", "📱 Android"),
        BotCommand("ios", "🍏 iOS"),
    ]
    await application.bot.set_my_commands(commands)
    print("✅ 菜单命令已设置")

# 各个指令处理
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🔗 {REGISTER_URL}")

async def site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🔗 {OFFICIAL_URL}")

async def cliente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📞 {CUSTOMER_SERVICE_URL}")

async def android(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📱 {ANDROID_DOWNLOAD_URL}")

async def ios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🍏 {IOS_DOWNLOAD_URL}")

# 启动程序
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # 添加指令处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("site", site))
    app.add_handler(CommandHandler("cliente", cliente))
    app.add_handler(CommandHandler("android", android))
    app.add_handler(CommandHandler("ios", ios))

    # 设置菜单命令
    app.post_init = set_bot_commands

    # 启动 webhook 模式（适配 Render）
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_DOMAIN}/{TOKEN}"
    )
