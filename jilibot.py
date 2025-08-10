# jilibot.py - cleaned (自动注册功能已移除)
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
    WebAppInfo,
    MenuButtonWebApp,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackContext,
)

import telegram
import os
import aiohttp
import asyncio

print("🔍 当前 python-telegram-bot 版本:", telegram.__version__)

GROUP_ID = -1002704459263 
WELCOME_TEXT = """Bem-vindo ao bot oficial do jilibot.jili707vip1.com, um produto de apostas baseado na plataforma jili707.
Aqui, você pode experimentar toda a emoção das apostas e ainda participar de campanhas de promoção,
para ganhar grandes prêmios em dinheiro.

Escolha uma opção abaixo 👇
"""
# Telegram Bot Token
TOKEN = "8331605813:AAFHs5vaFopD72LZOD-c1YsD4Ug2E47mbwg"

# Webhook domain
WEBHOOK_DOMAIN = "https://telegram-bot-45rt.onrender.com"

# URLs
REGISTER_URL = "https://jilibot.jili707vip1.com/register"
OFFICIAL_URL = "https://jilibot.jili707vip1.com/"
CUSTOMER_SERVICE_URL = "https://magweb.meinuoka.com/Web/im.aspx?_=t&accountid=133283"
IOS_DOWNLOAD_URL = "https://images.6929183.com/wsd-images-prod/jili707f2/merchant_resource/mobileconfig/jili707f2_2.4.3_20250725002905.mobileconfig"
ANDROID_DOWNLOAD_URL = "https://images.847830.com/wsd-images-prod/jili707f2/merchant_resource/android/jili707f2_2.4.68_20250725002907.apk"

def get_group_menu():
    keyboard = [
        [InlineKeyboardButton("🎮 Entrar no jogo", web_app=WebAppInfo(url=OFFICIAL_URL))],
        [InlineKeyboardButton("🟢 Link do site oficial", url=OFFICIAL_URL)],
        [InlineKeyboardButton("📝 Registre uma conta", url=REGISTER_URL)],
        [
            InlineKeyboardButton("🍏 iOS Download", url=IOS_DOWNLOAD_URL),
            InlineKeyboardButton("📱 Android Download", url=ANDROID_DOWNLOAD_URL)
        ],
        [InlineKeyboardButton("🧑‍💼 atendimento ao Cliente", url=CUSTOMER_SERVICE_URL)]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    inline_keyboard = [
        [InlineKeyboardButton("🎮 Entrar no jogo", web_app=WebAppInfo(url=OFFICIAL_URL))],
        [InlineKeyboardButton("🟢 Link do site oficial", url=OFFICIAL_URL)],
        [InlineKeyboardButton("📝 Registre uma conta", url=REGISTER_URL)],
        [
            InlineKeyboardButton("🍏 iOS Download", url=IOS_DOWNLOAD_URL),
            InlineKeyboardButton("📱 Android Download", url=ANDROID_DOWNLOAD_URL),
        ],
        [InlineKeyboardButton("🧑‍💼 atendimento ao Cliente", url=CUSTOMER_SERVICE_URL)],
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    reply_keyboard = [
        [KeyboardButton("🎮 Registre uma conta"), KeyboardButton("🟢 Link do site oficial")],
        [KeyboardButton("🧑‍💼 atendimento ao Cliente"), KeyboardButton("📱 ANDROID DOWNLOAD")],
        [KeyboardButton("🍏 IOS DOWNLOAD")],
    ]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Bem-vindo ao bot oficial do jilibot.jili707vip1.com, um produto de apostas baseado na plataforma jili707.\n"
        "Aqui, você pode experimentar toda a emoção das apostas e ainda participar de campanhas de promoção,\n"
        "para ganhar grandes prêmios em dinheiro.\n\n"
        "Escolha uma opção abaixo 👇",
        reply_markup=reply_markup
    )

    await update.message.reply_text("⬇️ Acesso rápido abaixo:", reply_markup=inline_markup)


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


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    # 如果用户点击或发送“注册”相关文字 — 显示注册链接
    if any(kw in text for kw in ["registe", "register", "registr", "注册", "conta"]):
        keyboard = [[InlineKeyboardButton("🎮 Clique aqui para registrar", url=REGISTER_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🎮 Clique abaixo para registrar manualmente 👇", reply_markup=reply_markup)
        return

    if "site" in text or text.startswith("/site"):
        keyboard = [[InlineKeyboardButton("🟢 Acessar site oficial", url=OFFICIAL_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🟢 Link do site oficial:\nClique abaixo para acessar 👇", reply_markup=reply_markup)
        return

    if "cliente" in text or text.startswith("/cliente"):
        keyboard = [[InlineKeyboardButton("🧑‍💼 Falar com o suporte", url=CUSTOMER_SERVICE_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🧑‍💼 Atendimento ao Cliente:\nClique abaixo para falar com o suporte 👇", reply_markup=reply_markup)
        return

    if "android" in text or text.startswith("/android"):
        keyboard = [[InlineKeyboardButton("📱 Baixar Android", url=ANDROID_DOWNLOAD_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("📱 Android Download:\nClique abaixo para baixar 👇", reply_markup=reply_markup)
        return

    if "ios" in text or text.startswith("/ios"):
        keyboard = [[InlineKeyboardButton("🍏 Baixar iOS", url=IOS_DOWNLOAD_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🍏 iOS Download:\nClique abaixo para baixar 👇", reply_markup=reply_markup)
        return

    # 其他未识别
    await update.message.reply_text("❓ Comando não reconhecido. Por favor, use os botões ou comandos disponíveis.")

async def send_group_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=WELCOME_TEXT,
        reply_markup=get_group_menu()
    )

async def keep_alive():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                await session.get("https://telegram-bot-45rt.onrender.com")
        except Exception as e:
            print(f"Keep-alive error: {e}")
        await asyncio.sleep(600)


async def post_init(application):
    print("⚙️ 正在设置 Bot 菜单按钮...")
    await set_bot_commands(application)
    await application.bot.set_chat_menu_button(
        chat_id=None,
        menu_button=MenuButtonWebApp(text="OPEN", web_app=WebAppInfo(url=OFFICIAL_URL)),
    )
    print("✅ OPEN 按钮已设置")
    asyncio.create_task(keep_alive())
    
    application.job_queue.run_repeating(send_group_message, interval=3600, first=5)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", handle_text))
    app.add_handler(CommandHandler("site", handle_text))
    app.add_handler(CommandHandler("cliente", handle_text))
    app.add_handler(CommandHandler("android", handle_text))
    app.add_handler(CommandHandler("ios", handle_text))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.post_init = post_init

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_DOMAIN}/{TOKEN}",
    )
