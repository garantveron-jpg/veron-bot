import logging
import re
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# ============================================================
TELEGRAM_BOT_TOKEN = "8586034716:AAHBM0xOmcGt4K12_1c1dpDqfZOqBQIDzYc"
BRAWL_KANAL = "@NeytenYT"
PUBG_KANALLAR = ["@uzbekistancomminuty", "@player2748"]
ADMIN_USERNAME = "@Veron_Garant"
ADMIN_CHAT_ID = None  # /myid buyrug'i bilan oling
# ============================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler('bot.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# States
GAME_SELECT = 0
# Brawl Stars states
BS_NIK = 10
BS_KUBOK = 11
BS_TITUL = 12
BS_BRAWLER = 13
BS_SKIN = 14
BS_GEM = 15
BS_GIPER = 16
BS_BRAWLPASS = 17
BS_NARX = 18
BS_MUROJAAT = 19
BS_MEDIA = 20
# PUBG states
PG_TIER = 30
PG_UC = 31
PG_SKIN = 32
PG_NARX = 33
PG_MANZIL = 34
PG_MUROJAAT = 35
PG_MEDIA = 36

def main_menu():
    keyboard = [
        ["📝 E'lon berish", "🛍 Donat Narxlar"],
        ["👤 Profil", "📊 Statistika"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def back_button():
    return ReplyKeyboardMarkup([["🔙 Orqaga"]], resize_keyboard=True)

def game_select_keyboard():
    keyboard = [
        ["🟡 BRAWL STARS", "🎮 PUBG MOBILE"],
        ["🔙 Orqaga"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Salom, {user.first_name}! 👋\n\n"
        f"🎮 Veron Garant Bot ga xush kelibsiz!\n"
        f"Bu yerda o'yin akkauntlarini sotishingiz mumkin.\n\n"
        f"Quyidagi menyudan tanlang:",
        reply_markup=main_menu()
    )
    return ConversationHandler.END

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Sizning ID: `{update.effective_user.id}`", parse_mode='Markdown')

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📝 E'lon berish":
        await update.message.reply_text(
            "Qaysi o'yin uchun e'lon berasiz?",
            reply_markup=game_select_keyboard()
        )
        return GAME_SELECT

    elif text == "🛍 Donat Narxlar":
        await update.message.reply_text(
            "💎 Donat narxlari:\n\n"
            "🟡 Brawl Stars:\n"
            "• 80 Gem - 15,000 so'm\n"
            "• 170 Gem - 30,000 so'm\n"
            "• 360 Gem - 60,000 so'm\n\n"
            "🎮 PUBG Mobile:\n"
            "• 60 UC - 15,000 so'm\n"
            "• 325 UC - 60,000 so'm\n"
            "• 660 UC - 115,000 so'm\n\n"
            f"Murojaat: {ADMIN_USERNAME}",
            reply_markup=main_menu()
        )

    elif text == "👤 Profil":
        user = update.effective_user
        await update.message.reply_text(
            f"👤 Profil\n\n"
            f"Ism: {user.first_name}\n"
            f"Username: @{user.username if user.username else 'Yoq'}\n"
            f"ID: {user.id}",
            reply_markup=main_menu()
        )

    elif text == "📊 Statistika":
        await update.message.reply_text(
            "📊 Statistika\n\n"
            "Bot ishlayapti! ✅",
            reply_markup=main_menu()
        )

    return ConversationHandler.END

async def game_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔙 Orqaga":
        await update.message.reply_text("Asosiy menyu:", reply_markup=main_menu())
        return ConversationHandler.END

    elif text == "🟡 BRAWL STARS":
        context.user_data['game'] = 'brawl'
        await update.message.reply_text(
            "🟡 BRAWL STARS e'lon\n\nAkkaunt NIK ni kiriting:",
            reply_markup=back_button()
        )
        return BS_NIK

    elif text == "🎮 PUBG MOBILE":
        context.user_data['game'] = 'pubg'
        await update.message.reply_text(
            "🎮 PUBG MOBILE e'lon\n\nTier (rang) kiriting (masalan: Platinum, Diamond):",
            reply_markup=back_button()
        )
        return PG_TIER

    return GAME_SELECT

# ==================== BRAWL STARS ====================

async def bs_nik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("O'yin tanlang:", reply_markup=game_select_keyboard())
        return GAME_SELECT
    context.user_data['bs_nik'] = update.message.text
    await update.message.reply_text("Kuboklar sonini kiriting (faqat raqam):", reply_markup=back_button())
    return BS_KUBOK

async def bs_kubok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("NIK kiriting:", reply_markup=back_button())
        return BS_NIK
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam kiriting!")
        return BS_KUBOK
    context.user_data['bs_kubok'] = update.message.text
    await update.message.reply_text("Titul kiriting (masalan: Legend, Masters):", reply_markup=back_button())
    return BS_TITUL

async def bs_titul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Kuboklar sonini kiriting:", reply_markup=back_button())
        return BS_KUBOK
    context.user_data['bs_titul'] = update.message.text
    await update.message.reply_text("Brawler soni kiriting (faqat raqam):", reply_markup=back_button())
    return BS_BRAWLER

async def bs_brawler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Titul kiriting:", reply_markup=back_button())
        return BS_TITUL
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam kiriting!")
        return BS_BRAWLER
    context.user_data['bs_brawler'] = update.message.text
    await update.message.reply_text("Skin soni kiriting (faqat raqam):", reply_markup=back_button())
    return BS_SKIN

async def bs_skin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Brawler sonini kiriting:", reply_markup=back_button())
        return BS_BRAWLER
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam kiriting!")
        return BS_SKIN
    context.user_data['bs_skin'] = update.message.text
    await update.message.reply_text("Gem miqdori kiriting (faqat raqam):", reply_markup=back_button())
    return BS_GEM

async def bs_gem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Skin sonini kiriting:", reply_markup=back_button())
        return BS_SKIN
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam kiriting!")
        return BS_GEM
    context.user_data['bs_gem'] = update.message.text
    keyboard = ReplyKeyboardMarkup([["Ha", "Yoq"], ["🔙 Orqaga"]], resize_keyboard=True)
    await update.message.reply_text("Giperzaryad bor mi?", reply_markup=keyboard)
    return BS_GIPER

async def bs_giper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Gem miqdorini kiriting:", reply_markup=back_button())
        return BS_GEM
    context.user_data['bs_giper'] = update.message.text
    keyboard = ReplyKeyboardMarkup([["Ha", "Yoq"], ["🔙 Orqaga"]], resize_keyboard=True)
    await update.message.reply_text("Brawl Pass bor mi?", reply_markup=keyboard)
    return BS_BRAWLPASS

async def bs_brawlpass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Giperzaryad:", reply_markup=back_button())
        return BS_GIPER
    context.user_data['bs_brawlpass'] = update.message.text
    await update.message.reply_text("Narx kiriting (so'mda, faqat raqam):", reply_markup=back_button())
    return BS_NARX

async def bs_narx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Brawl Pass:", reply_markup=back_button())
        return BS_BRAWLPASS
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam kiriting!")
        return BS_NARX
    context.user_data['bs_narx'] = update.message.text
    await update.message.reply_text("Murojaat (Telegram username @... yoki telefon raqam):", reply_markup=back_button())
    return BS_MUROJAAT

async def bs_murojaat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Narx kiriting:", reply_markup=back_button())
        return BS_NARX
    contact = update.message.text
    if '@' not in contact and not contact.replace('+', '').replace(' ', '').isdigit():
        await update.message.reply_text("Iltimos @ username yoki telefon raqam kiriting!")
        return BS_MUROJAAT
    context.user_data['bs_murojaat'] = contact
    await update.message.reply_text(
        "Akkaunt rasmi/videosini yuboring (yoki 'Yoq' deb yozing):",
        reply_markup=back_button()
    )
    return BS_MEDIA

async def bs_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Murojaat kiriting:", reply_markup=back_button())
        return BS_MUROJAAT

    d = context.user_data
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    elon = (
        f"🟡 BRAWL STARS AKKOUNT SOTILADI\n"
        f"{'='*30}\n"
        f"NIK: {d.get('bs_nik')}\n"
        f"Kubok: {d.get('bs_kubok')}\n"
        f"Titul: {d.get('bs_titul')}\n"
        f"Brawlerlar: {d.get('bs_brawler')} ta\n"
        f"Skinlar: {d.get('bs_skin')} ta\n"
        f"Gemlar: {d.get('bs_gem')} ta\n"
        f"Giperzaryad: {d.get('bs_giper')}\n"
        f"Brawl Pass: {d.get('bs_brawlpass')}\n"
        f"{'='*30}\n"
        f"Narx: {d.get('bs_narx')} so'm\n"
        f"Murojaat: {d.get('bs_murojaat')}\n"
        f"Sana: {now}"
    )

    try:
        if update.message.photo:
            await context.bot.send_photo(chat_id=BRAWL_KANAL, photo=update.message.photo[-1].file_id, caption=elon)
        elif update.message.video:
            await context.bot.send_video(chat_id=BRAWL_KANAL, video=update.message.video.file_id, caption=elon)
        else:
            await context.bot.send_message(chat_id=BRAWL_KANAL, text=elon)

        if ADMIN_CHAT_ID:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Yangi e'lon!\n\n{elon}")

        await update.message.reply_text(
            "E'lon muvaffaqiyatli joylashtirildi! ✅",
            reply_markup=main_menu()
        )
    except Exception as e:
        logger.error(f"Xato: {e}")
        await update.message.reply_text(
            f"Xato yuz berdi: {e}\nAdmin: {ADMIN_USERNAME}",
            reply_markup=main_menu()
        )

    context.user_data.clear()
    return ConversationHandler.END

# ==================== PUBG MOBILE ====================

async def pg_tier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("O'yin tanlang:", reply_markup=game_select_keyboard())
        return GAME_SELECT
    context.user_data['pg_tier'] = update.message.text
    await update.message.reply_text("UC miqdori kiriting (faqat raqam):", reply_markup=back_button())
    return PG_UC

async def pg_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Tier kiriting:", reply_markup=back_button())
        return PG_TIER
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam kiriting!")
        return PG_UC
    context.user_data['pg_uc'] = update.message.text
    await update.message.reply_text("Skin soni kiriting (faqat raqam):", reply_markup=back_button())
    return PG_SKIN

async def pg_skin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("UC miqdori kiriting:", reply_markup=back_button())
        return PG_UC
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam kiriting!")
        return PG_SKIN
    context.user_data['pg_skin'] = update.message.text
    await update.message.reply_text("Narx kiriting (so'mda, faqat raqam):", reply_markup=back_button())
    return PG_NARX

async def pg_narx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Skin sonini kiriting:", reply_markup=back_button())
        return PG_SKIN
    if not update.message.text.isdigit():
        await update.message.reply_text("Faqat raqam kiriting!")
        return PG_NARX
    context.user_data['pg_narx'] = update.message.text
    await update.message.reply_text("Akkount manzili (server/mintaqa):", reply_markup=back_button())
    return PG_MANZIL

async def pg_manzil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Narx kiriting:", reply_markup=back_button())
        return PG_NARX
    context.user_data['pg_manzil'] = update.message.text
    await update.message.reply_text("Murojaat (Telegram username @... yoki telefon raqam):", reply_markup=back_button())
    return PG_MUROJAAT

async def pg_murojaat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Manzil kiriting:", reply_markup=back_button())
        return PG_MANZIL
    contact = update.message.text
    if '@' not in contact and not contact.replace('+', '').replace(' ', '').isdigit():
        await update.message.reply_text("Iltimos @ username yoki telefon raqam kiriting!")
        return PG_MUROJAAT
    context.user_data['pg_murojaat'] = contact
    await update.message.reply_text(
        "Akkaunt rasmi/videosini yuboring (yoki 'Yoq' deb yozing):",
        reply_markup=back_button()
    )
    return PG_MEDIA

async def pg_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("Murojaat kiriting:", reply_markup=back_button())
        return PG_MUROJAAT

    d = context.user_data
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    elon = (
        f"🎮 PUBG MOBILE AKKOUNT SOTILADI\n"
        f"{'='*30}\n"
        f"Tier: {d.get('pg_tier')}\n"
        f"UC: {d.get('pg_uc')} ta\n"
        f"Skinlar: {d.get('pg_skin')} ta\n"
        f"Manzil: {d.get('pg_manzil')}\n"
        f"{'='*30}\n"
        f"Narx: {d.get('pg_narx')} so'm\n"
        f"Murojaat: {d.get('pg_murojaat')}\n"
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

        if ADMIN_CHAT_ID:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Yangi e'lon!\n\n{elon}")

        await update.message.reply_text(
            "E'lon muvaffaqiyatli joylashtirildi! ✅",
            reply_markup=main_menu()
        )
    except Exception as e:
        logger.error(f"Xato: {e}")
        await update.message.reply_text(
            f"Xato yuz berdi: {e}\nAdmin: {ADMIN_USERNAME}",
            reply_markup=main_menu()
        )

    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Bekor qilindi.", reply_markup=main_menu())
    return ConversationHandler.END

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],
        states={
            GAME_SELECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, game_select)],
            BS_NIK: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs_nik)],
            BS_KUBOK: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs_kubok)],
            BS_TITUL: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs_titul)],
            BS_BRAWLER: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs_brawler)],
            BS_SKIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs_skin)],
            BS_GEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs_gem)],
            BS_GIPER: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs_giper)],
            BS_BRAWLPASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs_brawlpass)],
            BS_NARX: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs_narx)],
            BS_MUROJAAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, bs_murojaat)],
            BS_MEDIA: [MessageHandler(filters.ALL & ~filters.COMMAND, bs_media)],
            PG_TIER: [MessageHandler(filters.TEXT & ~filters.COMMAND, pg_tier)],
            PG_UC: [MessageHandler(filters.TEXT & ~filters.COMMAND, pg_uc)],
            PG_SKIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, pg_skin)],
            PG_NARX: [MessageHandler(filters.TEXT & ~filters.COMMAND, pg_narx)],
            PG_MANZIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, pg_manzil)],
            PG_MUROJAAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, pg_murojaat)],
            PG_MEDIA: [MessageHandler(filters.ALL & ~filters.COMMAND, pg_media)],
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
    
