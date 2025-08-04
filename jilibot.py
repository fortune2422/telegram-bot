from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
    WebAppInfo,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
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
    # 💬 聊天框中绿色按钮
    inline_keyboard = [
        [InlineKeyboardButton("🎮 Entrar no jogo", web_app=WebAppInfo(url=OFFICIAL_URL))],
        [InlineKeyboardButton("🟢 Link do site oficial", url=OFFICIAL_URL),
         InlineKeyboardButton("🎮 Registre uma conta", url=REGISTER_URL)
        ],
        [
            InlineKeyboardButton("🍏 iOS Download", url=IOS_DOWNLOAD_URL),
            InlineKeyboardButton("📱 Android Download", url=ANDROID_DOWNLOAD_URL)
        ],
        [
         InlineKeyboardButton("🧑‍💼 atendimento ao Cliente", url=CUSTOMER_SERVICE_URL)
        ]    
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    # ⌨️ 底部菜单按钮
    reply_keyboard = [
        [KeyboardButton("🎮 Registre uma conta"), KeyboardButton("🟢 Link do site oficial")],
        [KeyboardButton("📱 ANDROID DOWNLOAD"), KeyboardButton("🍏 IOS DOWNLOAD")],
        [KeyboardButton("🧑‍💼 atendimento ao Cliente")],
    ]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    # 发送欢迎文字 + 底部菜单
    await update.message.reply_text(
        "Bem-vindo ao bot oficial do jili707.co, um produto de apostas baseado na plataforma jili707.\n"
        "Aqui, você pode experimentar toda a emoção das apostas e ainda participar de campanhas de promoção,\n"
        "para ganhar grandes prêmios em dinheiro.\n\n"
        "Escolha uma opção abaixo 👇",
        reply_markup=reply_markup
    )

    # 发送绿色 inline 按钮
    await update.message.reply_text("⬇️ Acesso rápido abaixo:", reply_markup=inline_markup)
    
    # ✅✅✅ 新增部分：自动发送“OPEN”按钮（无文字）
    open_button = [[InlineKeyboardButton("OPEN", web_app=WebAppInfo(url=OFFICIAL_URL))]]
    open_markup = InlineKeyboardMarkup(open_button)
    await update.message.reply_text("Clique no botão abaixo para abrir o jogo 👉", reply_markup=open_markup)  # 空格用于撑起按钮
    # ✅✅✅ 新增部分结束

# 菜单命令
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

## 文本按钮命令
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    if "registre" in text or text.startswith("/register"):
        keyboard = [[InlineKeyboardButton("🎮 Registrar agora", url=REGISTER_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🎮 Registre uma conta:\nClique abaixo para criar sua conta 👇", reply_markup=reply_markup)

    elif "site" in text or text.startswith("/site"):
        keyboard = [[InlineKeyboardButton("🟢 Acessar site oficial", url=OFFICIAL_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🟢 Link do site oficial:\nClique abaixo para acessar 👇", reply_markup=reply_markup)

    elif "cliente" in text or text.startswith("/cliente"):
        keyboard = [[InlineKeyboardButton("🧑‍💼 Falar com o suporte", url=CUSTOMER_SERVICE_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🧑‍💼 Atendimento ao Cliente:\nClique abaixo para falar com o suporte 👇", reply_markup=reply_markup)

    elif "android" in text or text.startswith("/android"):
        keyboard = [[InlineKeyboardButton("📱 Baixar Android", url=ANDROID_DOWNLOAD_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("📱 Android Download:\nClique abaixo para baixar 👇", reply_markup=reply_markup)

    elif "ios" in text or text.startswith("/ios"):
        keyboard = [[InlineKeyboardButton("🍏 Baixar iOS", url=IOS_DOWNLOAD_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🍏 iOS Download:\nClique abaixo para baixar 👇", reply_markup=reply_markup)

    else:
        await update.message.reply_text("❓ Comando não reconhecido. Por favor, use os botões ou comandos disponíveis.")


# 主程序
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # 指令 handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", handle_text))
    app.add_handler(CommandHandler("site", handle_text))
    app.add_handler(CommandHandler("cliente", handle_text))
    app.add_handler(CommandHandler("android", handle_text))
    app.add_handler(CommandHandler("ios", handle_text))

    # 文本按钮 handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # 设置菜单命令
    app.post_init = set_bot_commands

    # 启动 webhook（Render 部署）
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_DOMAIN}/{TOKEN}"
    )
