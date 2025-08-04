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
)
# 顶部统一 import 区
from playwright.async_api import async_playwright

import telegram
import os
import random
import string
import aiohttp

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

def random_username():
    return "jili_" + ''.join(random.choices(string.digits, k=6))

def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


async def auto_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = random_username()
    password = random_password()

    form = {
        "username": username,
        "password": password,
        "confirm_password": password
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(REGISTER_URL, data=form) as resp:
                text = await resp.text()
                if "login" in text.lower() or "success" in text.lower():
                    await update.message.reply_text(
                        f"✅ Conta criada com sucesso!\n👤 Usuário: `{username}`\n🔐 Senha: `{password}`",
                        parse_mode="Markdown"
                    )
                else:
                    await update.message.reply_text("❌ Falha ao registrar. Tente manualmente em: https://jili707.co/register")
    except Exception as e:
        await update.message.reply_text("❌ Erro ao registrar. Tente novamente mais tarde.")


async def auto_register_with_browser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = random_username()
    password = random_password()
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context_ = await browser.new_context()
            page = await context_.new_page()

            await page.goto(REGISTER_URL)
            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)
            await page.fill('input[name="confirm_password"]', password)
            await page.click('button[type="submit"]')  # 你也可以试试别的选择器，比如 .register-button

            await page.wait_for_timeout(2000)  # 可根据网站响应速度调整

            # 📸 截图页面
            screenshot_path = "/tmp/register_page.png"
            await page.screenshot(path=screenshot_path, full_page=True)

            content = await page.content()
            await browser.close()

            if "login" in content.lower() or "success" in content.lower():
                await update.message.reply_text(
                    f"✅ Conta criada com sucesso!\n👤 Usuário: `{username}`\n🔐 Senha: `{password}`",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text("❌ Falha ao registrar. Tente manualmente em: https://jili707.co/register")

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao registrar com navegador: {str(e)}")

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_keyboard = [
        [InlineKeyboardButton("🎮 Entrar no jogo", web_app=WebAppInfo(url="https://www.jili707.co"))],
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

    if any(kw in text for kw in ["register", "registar", "account", "注册", "conta", "criar conta"]):
        await auto_register(update, context)

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
        
# 👇 定义 post_init 函数（执行初始化动作，比如设置菜单命令和 OPEN 按钮）
async def post_init(application):
    print("⚙️ 正在设置 Bot 菜单按钮...")  # 调试用，部署时可删

    # 设置菜单命令
    await set_bot_commands(application)

    # 设置全局 OPEN 按钮
    await application.bot.set_chat_menu_button(
        chat_id=None,  # 💡 全局用户都看到
        menu_button=MenuButtonWebApp(
            text="OPEN",
            web_app=WebAppInfo(url=OFFICIAL_URL)
        )
    )
    print("✅ OPEN 按钮已设置")  # 可选调试日志


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
    app.add_handler(CommandHandler("autoreg", auto_register))
    app.add_handler(CommandHandler("autoreg_browser", auto_register_with_browser))

    # 文本按钮 handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # 设置菜单命令
    app.post_init = post_init

    # 启动 webhook（Render 部署）
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_DOMAIN}/{TOKEN}"
    )
