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
        [KeyboardButton("🎮 Registre uma conta"), KeyboardButton("🟢 Link do site oficial")],
        [KeyboardButton("📱 ANDROID DOWNLOAD"), KeyboardButton("🍏 IOS DOWNLOAD")],
        [KeyboardButton("🧑‍💼 atendimento ao Cliente")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    text = (
        "Bem-vindo ao bot oficial do jili707.co, um produto de apostas baseado na plataforma jili707.\n"
        "Aqui, você pode experimentar toda a emoção das apostas e ainda participar de campanhas de promoção,\n"
        "para ganhar grandes prêmios em dinheiro.\n\n"
        "Escolha uma opção abaixo 👇"
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

# 手动命令处理函数（命令或点击按钮时调用）
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    if "registre" in text or text.startswith("/register"):
        await update.message.reply_text(f"🎮 Registre uma conta: {REGISTER_URL}")
    elif "site" in text or text.startswith("/site"):
        await update.message.reply_text(f"🟢 Link do site oficial: {OFFICIAL_URL}")
    elif "cliente" in text or text.startswith("/cliente"):
        await update.message.reply_text(f"🧑‍💼 Atendimento ao Cliente: {CUSTOMER_SERVICE_URL}")
    elif "android" in text or text.startswith("/android"):
        await update.message.reply_text(f"📱 Android Download: {ANDROID_DOWNLOAD_URL}")
    elif "ios" in text or text.startswith("/ios"):
        await update.message.reply_text(f"🍏 iOS Download: {IOS_DOWNLOAD_URL}")
    else:
        await update.message.reply_text("❓ Comando não reconhecido. Por favor, use os botões ou comandos disponíveis.")

# 主程序
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # 添加指令
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", handle_text))
    app.add_handler(CommandHandler("site", handle_text))
    app.add_handler(CommandHandler("cliente", handle_text))
    app.add_handler(CommandHandler("android", handle_text))
    app.add_handler(CommandHandler("ios", handle_text))

    # 添加按钮点击（文本匹配）处理
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # 设置菜单
    app.post_init = set_bot_commands

    # 启动 Webhook（Render 部署）
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_DOMAIN}/{TOKEN}"
    )
