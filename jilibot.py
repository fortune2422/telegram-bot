from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    BotCommand
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import telegram

print("🔍 当前 python-telegram-bot 版本:", telegram.__version__)

# TOKEN
TOKEN = "8331605813:AAFHs5vaFopD72LZOD-c1YsD4Ug2E47mbwg"

# URLs
REGISTER_URL = "https://jili707.co/register"
OFFICIAL_URL = "https://jili707.co"
CUSTOMER_SERVICE_URL = "https://magweb.meinuoka.com/Web/im.aspx?_=t&accountid=133283"
IOS_DOWNLOAD_URL = "https://images.6929183.com/wsd-images-prod/jili707f2/merchant_resource/mobileconfig/jili707f2_2.4.3_20250725002905.mobileconfig"
ANDROID_DOWNLOAD_URL = "https://images.847830.com/wsd-images-prod/jili707f2/merchant_resource/android/jili707f2_2.4.68_20250725002907.apk"

# /start 指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🎮 Registre uma conta"), KeyboardButton("🟢 Link do site oficial")],
        [KeyboardButton("📱 ANDROID DOWNLOAD"), KeyboardButton("🍏 IOS DOWNLOAD")],
        [KeyboardButton("🧑‍💼 atendimento ao Cliente")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    welcome_text = (
        "Bem-vindo ao bot oficial do jili707.co, um produto de apostas baseado na plataforma jili707.\n"
        "Aqui, você pode experimentar toda a emoção das apostas e ainda participar de campanhas de promoção,\n"
        "para ganhar grandes prêmios em dinheiro.\n\n"
        "Seja bem-vindo ao bot oficial de apostas do Jili707!"
    )

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# 回复底部菜单按钮点击
async def handle_menu_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "Registre" in text:
        await update.message.reply_text(f"🔗 {REGISTER_URL}")
    elif "site oficial" in text:
        await update.message.reply_text(f"🌐 {OFFICIAL_URL}")
    elif "ANDROID" in text:
        await update.message.reply_text(f"📱 Android 下载链接：\n{ANDROID_DOWNLOAD_URL}")
    elif "IOS" in text:
        await update.message.reply_text(f"🍏 iOS 下载链接：\n{IOS_DOWNLOAD_URL}")
    elif "Cliente" in text:
        await update.message.reply_text(f"👨‍💼 客服地址：\n{CUSTOMER_SERVICE_URL}")
    else:
        await update.message.reply_text("❓ 无法识别的命令，请使用下方菜单按钮。")

# 设置菜单命令
async def set_bot_commands(application):
    commands = [
        BotCommand("register", "🎮 Registre uma conta"),
        BotCommand("site", "🟢 Link do site oficial"),
        BotCommand("cliente", "🧑‍💼 atendimento ao Cliente"),
        BotCommand("android", "📱 Android"),
        BotCommand("ios", "🍏 iOS")
    ]
    await application.bot.set_my_commands(commands)
    print("✅ 菜单命令已设置")

# 指令函数（可选保留）
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🔗 {REGISTER_URL}")

async def site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🌐 {OFFICIAL_URL}")

async def cliente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📞 {CUSTOMER_SERVICE_URL}")

async def android(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📱 {ANDROID_DOWNLOAD_URL}")

async def ios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🍏 {IOS_DOWNLOAD_URL}")

# 主程序入口
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # 命令处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("site", site))
    app.add_handler(CommandHandler("cliente", cliente))
    app.add_handler(CommandHandler("android", android))
    app.add_handler(CommandHandler("ios", ios))

    # 文本按钮点击
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_click))

    # 设置命令
    app.post_init = set_bot_commands

    app.run_polling()
