import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TELEGRAM_BOT_TOKEN = "8586034716:AAHBM0xOmcGt4K12_1c1dpDqfZOqBQIDzYc"
BRAWL_KANAL = "@NeytenYT"
PUBG_KANALLAR = ["@uzbekistancomminuty", "@player2748"]
ADMIN_USERNAME = "@Veron_Garant"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GAME, BS1, BS2, BS3, BS4, BS5, BS6, BS7, BS8, BS9, BS10, BS11 = range(12)
PG1, PG2, PG3, PG4, PG5, PG6, PG7 = range(20, 27)

def menu():
    return ReplyKeyboardMarkup([["Elon berish", "Donat Narxlar"], ["Profil"]], resize_keyboard=True)

def back():
    return ReplyKeyboardMarkup([["Orqaga"]], resize_keyboard=True)

def game_kb():
    return ReplyKeyboardMarkup([["BRAWL STARS", "PUBG MOBILE"], ["Orqaga"]], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Veron Garant Bot ga xush kelibsiz!\nMenyudan tanlang:",
        reply_markup=menu()
    )
    return ConversationHandler.END

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Sizning ID: {update.effective_user.id}")

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Elon berish":
        await update.message.reply_text("Qaysi oyinda?", reply_markup=game_kb())
        return GAME
    elif text == "Donat Narxlar":
        await update.message.reply_text(
            "Donat narxlari:\n\nBRAWL STARS:\n80 Gem - 15,000\n170 Gem - 30,000\n\nPUBG:\n60 UC - 15,000\n325 UC - 60,000\n\nMurojaat: " + ADMIN_USERNAME,
            reply_markup=menu()
        )
    elif text == "Profil":
        u = update.effective_user
        await update.message.reply_text(f"Ism: {u.first_name}\nID: {u.id}", reply_markup=menu())
    return ConversationHandler.END

async def game_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Orqaga":
        await update.message.reply_text("Menyu:", reply_markup=menu())
        return ConversationHandler.END
    elif text == "BRAWL STARS":
        context.user_data['game'] = 'brawl'
        await update.message.reply_text("Akkount NIK kiriting:", reply_markup=back())
        return BS1
    elif text == "PUBG MOBILE":
        context.user_data['game'] = 'pubg'
        await update.message.reply_text("Tier kiriting (masalan: Platinum):", reply_markup=back())
        return PG1
    return GAME

# BRAWL STARS
async def bs1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Oyinni tanlang:", reply_markup=game_kb())
        return GAME
    context.user_data['nik'] = update.message.text
    await update.message.reply_text("Kubok soni (raqam):", reply_markup=back())
    return BS2

async def bs2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("NIK kiriting:", reply_markup=back())
        return BS1
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam!")
        return BS2
    context.user_data['kubok'] = update.message.text
    await update.message.reply_text("Titul (masalan: Legend):", reply_markup=back())
    return BS3

async def bs3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Kubok:", reply_markup=back())
        return BS2
    context.user_data['titul'] = update.message.text
    await update.message.reply_text("Brawler soni (raqam):", reply_markup=back())
    return BS4

async def bs4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Titul:", reply_markup=back())
        return BS3
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam!")
        return BS4
    context.user_data['brawler'] = update.message.text
    await update.message.reply_text("Skin soni (raqam):", reply_markup=back())
    return BS5

async def bs5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Brawler:", reply_markup=back())
        return BS4
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam!")
        return BS5
    context.user_data['skin'] = update.message.text
    await update.message.reply_text("Gem miqdori (raqam):", reply_markup=back())
    return BS6

async def bs6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Skin:", reply_markup=back())
        return BS5
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam!")
        return BS6
    context.user_data['gem'] = update.message.text
    kb = ReplyKeyboardMarkup([["Ha", "Yoq"], ["Orqaga"]], resize_keyboard=True)
    await update.message.reply_text("Giperzaryad bormi?", reply_markup=kb)
    return BS7

async def bs7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Gem:", reply_markup=back())
        return BS6
    context.user_data['giper'] = update.message.text
    kb = ReplyKeyboardMarkup([["Ha", "Yoq"], ["Orqaga"]], resize_keyboard=True)
    await update.message.reply_text("Brawl Pass bormi?", reply_markup=kb)
    return BS8

async def bs8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Giperzaryad:", reply_markup=back())
        return BS7
    context.user_data['brawlpass'] = update.message.text
    await update.message.reply_text("Narx (so'm, raqam):", reply_markup=back())
    return BS9

async def bs9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Brawl Pass:", reply_markup=back())
        return BS8
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam!")
        return BS9
    context.user_data['narx'] = update.message.text
    await update.message.reply_text("Murojaat (@username yoki telefon):", reply_markup=back())
    return BS10

async def bs10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Narx:", reply_markup=back())
        return BS9
    context.user_data['murojaat'] = update.message.text
    await update.message.reply_text("Rasm/video yuboring yoki 'Yoq' yozing:", reply_markup=back())
    return BS11

async def bs11(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Murojaat:", reply_markup=back())
        return BS10
    d = context.user_data
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    elon = (
        "BRAWL STARS AKKOUNT SOTILADI\n"
        "==============================\n"
        f"NIK: {d.get('nik')}\n"
        f"Kubok: {d.get('kubok')}\n"
        f"Titul: {d.get('titul')}\n"
        f"Brawlerlar: {d.get('brawler')} ta\n"
        f"Skinlar: {d.get('skin')} ta\n"
        f"Gemlar: {d.get('gem')} ta\n"
        f"Giperzaryad: {d.get('giper')}\n"
        f"Brawl Pass: {d.get('brawlpass')}\n"
        "==============================\n"
        f"Narx: {d.get('narx')} som\n"
        f"Murojaat: {d.get('murojaat')}\n"
        f"Sana: {now}"
    )
    try:
        if update.message.photo:
            await context.bot.send_photo(chat_id=BRAWL_KANAL, photo=update.message.photo[-1].file_id, caption=elon)
        elif update.message.video:
            await context.bot.send_video(chat_id=BRAWL_KANAL, video=update.message.video.file_id, caption=elon)
        else:
            await context.bot.send_message(chat_id=BRAWL_KANAL, text=elon)
        await update.message.reply_text("Elon joylashtirildi!", reply_markup=menu())
    except Exception as e:
        await update.message.reply_text(f"Xato: {e}", reply_markup=menu())
    context.user_data.clear()
    return ConversationHandler.END

# PUBG
async def pg1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Oyinni tanlang:", reply_markup=game_kb())
        return GAME
    context.user_data['tier'] = update.message.text
    await update.message.reply_text("UC miqdori (raqam):", reply_markup=back())
    return PG2

async def pg2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Tier:", reply_markup=back())
        return PG1
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam!")
        return PG2
    context.user_data['uc'] = update.message.text
    await update.message.reply_text("Skin soni (raqam):", reply_markup=back())
    return PG3

async def pg3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("UC:", reply_markup=back())
        return PG2
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam!")
        return PG3
    context.user_data['skin'] = update.message.text
    await update.message.reply_text("Narx (so'm, raqam):", reply_markup=back())
    return PG4

async def pg4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Skin:", reply_markup=back())
        return PG3
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam!")
        return PG4
    context.user_data['narx'] = update.message.text
    await update.message.reply_text("Server/mintaqa:", reply_markup=back())
    return PG5

async def pg5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Narx:", reply_markup=back())
        return PG4
    context.user_data['manzil'] = update.message.text
    await update.message.reply_text("Murojaat (@username yoki telefon):", reply_markup=back())
    return PG6

async def pg6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Manzil:", reply_markup=back())
        return PG5
    context.user_data['murojaat'] = update.message.text
    await update.message.reply_text("Rasm/video yuboring yoki 'Yoq' yozing:", reply_markup=back())
    return PG7

async def pg7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Orqaga":
        await update.message.reply_text("Murojaat:", reply_markup=back())
        return PG6
    d = context.user_data
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    elon = (
        "PUBG MOBILE AKKOUNT SOTILADI\n"
        "==============================\n"
        f"Tier: {d.get('tier')}\n"
        f"UC: {d.get('uc')} ta\n"
        f"Skinlar: {d.get('skin')} ta\n"
        f"Manzil: {d.get('manzil')}\n"
        "==============================\n"
        f"Narx: {d.get('narx')} som\n"
        f"Murojaat: {d.get('murojaat')}\n"
        f"Sana: {now}"
    )
    try:
        for kanal in PUBG_KANALLAR:
            if update.message.photo:
                await context.bot.send_photo(chat_id=kanal, photo=update.message.photo[-1].file_id, caption=elon)
            elif update.message.video:
                await context.bot.send_video(chat_id=kanal, video=update.message.video.file_id, caption=elon)
            else:
                await context.bot.send_message(chat_id=kanal, text=elon)
        await update.message.reply_text("Elon joylashtirildi!", reply_markup=menu())
    except Exception as e:
        await update.message.reply_text(f"Xato: {e}", reply_markup=menu())
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Bekor qilindi.", reply_markup=menu())
    return ConversationHandler.END

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],
        states={
            GAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, game_select)],
            BS1: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs1)],
            BS2: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs2)],
            BS3: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs3)],
            BS4: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs4)],
            BS5: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs5)],
            BS6: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs6)],
            BS7: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs7)],
            BS8: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs8)],
            BS9: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs9)],
            BS10: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs10)],
            BS11: [MessageHandler(filters.ALL & ~filters.COMMAND, bs11)],
            PG1: [MessageHandler(filters.TEXT & ~filters.COMMAND, pg1)],
            PG2: [MessageHandler(filters.TEXT & ~filters.COMMAND, pg2)],
            PG3: [MessageHandler(filters.TEXT & ~filters.COMMAND, pg3)],
            PG4: [MessageHandler(filters.TEXT & ~filters.COMMAND, pg4)],
            PG5: [MessageHandler(filters.TEXT & ~filters.COMMAND, pg5)],
            PG6: [MessageHandler(filters.TEXT & ~filters.COMMAND, pg6)],
            PG7: [MessageHandler(filters.ALL & ~filters.COMMAND, pg7)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(conv)
    logger.info("Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
   
    
