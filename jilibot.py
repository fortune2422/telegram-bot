from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import TelegramError
import asyncio

# Bot Token
TOKEN = "8331605813:AAFHs5vaFopD72LZOD-c1YsD4Ug2E47mbwg"
bot = Bot(token=TOKEN)

# 清除旧 webhook（避免冲突）
try:
    bot.delete_webhook(drop_pending_updates=True)
    print("✅ 已清除之前的会话")
except TelegramError as e:
    print(f"⚠️ 清除失败：{e}")

# 链接
REGISTER_URL = "https://jili707.co/register"
OFFICIAL_URL = "https://jili707.co"
CUSTOMER_SERVICE_URL = "https://magweb.meinuoka.com/Web/im.aspx?_=t&accountid=133283"
IOS_DOWNLOAD_URL = "https://images.6929183.com/wsd-images-prod/jili707f2/merchant_resource/mobileconfig/jili707f2_2.4.3_20250725002905.mobileconfig"
ANDROID_DOWNLOAD_URL = "https://images.847830.com/wsd-images-prod/jili707f2/merchant_resource/android/jili707f2_2.4.68_20250725002907.apk"

# 设置输入框下的命令菜单
async def set_bot_commands(bot):
    commands = [
        BotCommand("register", "🎮 Registre uma conta"),
        BotCommand("site", "🟢 Link do site oficial"),
        BotCommand("cliente", "🧑‍💼 atendimento ao Cliente"),
        BotCommand("android", "📱 Android"),
        BotCommand("ios", "🍏 iOS"),
    ]
    await bot.set_my_commands(commands)

# /start 命令
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
        "Aqui, você pode experimentar toda a emoção das apostas e ainda participar de campanhas de promoção,\n"
        "para ganhar grandes prêmios em dinheiro.\n\n"
        "Seja bem-vindo ao bot oficial de apostas do Jili707!"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# 空指令响应（可选）
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

# 主程序入口
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # 设置命令菜单
    await set_bot_commands(app.bot)

    # 添加处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("site", site))
    app.add_handler(CommandHandler("cliente", cliente))
    app.add_handler(CommandHandler("android", android))
    app.add_handler(CommandHandler("ios", ios))

    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
