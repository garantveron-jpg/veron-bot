from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8586034716:AAHBM0xOmcGt4K12_1c1dpDqfZOqBQIDzYc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ishlayapti!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
