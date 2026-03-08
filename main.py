
import logging
import re
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

# =============================================
TELEGRAM_BOT_TOKEN = "8586034716:AAHBM0xOmcGt4K12_1c1dpDqfZOqBQIDzYc"
BRAWL_KANAL = "@NeytenYT"
PUBG_KANALLAR = ["@uzbekistancomminuty", "@player2748"]
ADMIN_USERNAME = "@Veron_Garant"
ADMIN_CHAT_ID = None  # /myid buyrug'i bilan bilib olasiz
# =============================================

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(name)

(OYUN,
 B_NIK, B_KUBOK, B_TITUL, B_BRAWLER, B_SKIN, B_GEM, B_GIPER, B_BPASS, B_NARX, B_MUROJAAT, B_MEDIA,
 P_TIER, P_UC, P_SKIN, P_NARX, P_MANZIL, P_MUROJAAT, P_MEDIA) = range(19)

user_data_store = {}
elon_count = {"brawl": 0, "pubg": 0}

# ─── KLAVIATURALAR ────────────────────────
def main_kb():
    return ReplyKeyboardMarkup([
        ["📝 E'lon berish", "🛍 Donat Narxlar"],
        ["👤 Profil", "📊 Statistika"]
    ], resize_keyboard=True)

def back_kb():
    return ReplyKeyboardMarkup([["🔙 Orqaga"]], resize_keyboard=True)

def oyun_kb():
    return ReplyKeyboardMarkup([
        ["🟡 BRAWL STARS", "🎮 PUBG MOBILE"],
        ["🔙 Orqaga"]
    ], resize_keyboard=True)

# ─── VALIDATSIYA ──────────────────────────
def is_number(text):
    return bool(re.match(r'^\d+([.,]\d+)?[kKmMbB]?$', text.strip()))

def is_valid_contact(text):
    return "@" in text or text.replace("+", "").replace(" ", "").isdigit()

# ─── START ────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Yangi foydalanuvchi: {user.username} ({user.id})")
    await update.message.reply_text(
        f"Salom, *{user.first_name}*! 👋\n\n"
        f"🎮 Men akkaunt e'lon botiman!\n\n"
        f"• 🟡 Brawl Stars akkaunt sotish\n"
        f"• 🎮 PUBG Mobile akkaunt sotish\n\n"
        f"Boshlash uchun *E'lon berish* tugmasini bosing!",
        parse_mode="Markdown",
        reply_markup=main_kb()
    )

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Sizning ID: {update.effective_user.id}", parse_mode="Markdown")

# ─── MENU ─────────────────────────────────
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    if text == "📝 E'lon berish":
        await update.message.reply_text(
            "🎮 Qaysi o'yin akkauntini sotmoqchisiz?",
            reply_markup=oyun_kb()
        )
        return OYUN

    elif text == "🛍 Donat Narxlar":
        kb = [[InlineKeyboardButton("💎 Donat Kanal", url="https://t.me/Veron_Up_danat")]]
        await update.message.reply_text(
            "🛍 *Donat Narxlar*\n\n"
            "💎 80 Gem — 15,000 so'm\n"
            "💎 170 Gem — 30,000 so'm\n"
            "💎 360 Gem — 60,000 so'm\n"
            "💎 950 Gem — 150,000 so'm\n\n"
            f"📞 Murojaat: {ADMIN_USERNAME}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb)
        )

    elif text == "👤 Profil":
        username = f"@{user.username}" if user.username else "Yo'q"
        await update.message.reply_text(
            f"👤 *Profil*\n\n"
            f"Ism: {user.first_name}\n"
            f"Username: {username}\n"
            f"ID: {user.id}\n\n"
            f"🟡 Brawl e'lonlar: {elon_count['brawl']}\n"
            f"🎮 PUBG e'lonlar: {elon_count['pubg']}",
            parse_mode="Markdown"
        )

elif text == "📊 Statistika":
        jami = elon_count['brawl'] + elon_count['pubg']
        await update.message.reply_text(
            f"📊 *Bot Statistikasi*\n\n"
            f"🟡 Brawl Stars e'lonlar: {elon_count['brawl']}\n"
            f"🎮 PUBG Mobile e'lonlar: {elon_count['pubg']}\n"
            f"📋 Jami e'lonlar: {jami}",
            parse_mode="Markdown"
        )

# ─── OYUN TANLASH ─────────────────────────
async def oyun_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_user.id

    if text == "🔙 Orqaga":
        await update.message.reply_text("🏠 Asosiy menyu:", reply_markup=main_kb())
        return ConversationHandler.END

    user_data_store[uid] = {"oyun": text}

    if "BRAWL" in text:
        await update.message.reply_text(
            "📋 *1/10* — Akkaunt nikini yozing:",
            parse_mode="Markdown",
            reply_markup=back_kb()
        )
        return B_NIK
    elif "PUBG" in text:
        await update.message.reply_text(
            "🏆 *1/7* — Tier/Rangingizni yozing:\n_(Masalan: Bronze, Silver, Gold, Platinum, Diamond, Crown, Ace, Conqueror)_",
            parse_mode="Markdown",
            reply_markup=back_kb()
        )
        return P_TIER
    else:
        await update.message.reply_text("❌ Iltimos, o'yinni tanlang!", reply_markup=oyun_kb())
        return OYUN

# ─── BRAWL STARS ──────────────────────────
async def b_nik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("🎮 O'yinni tanlang:", reply_markup=oyun_kb())
        return OYUN
    user_data_store[update.effective_user.id]["nik"] = update.message.text
    await update.message.reply_text("🏆 *2/10* — Kuboklar sonini yozing _(faqat raqam)_:", parse_mode="Markdown", reply_markup=back_kb())
    return B_KUBOK

async def b_kubok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("📋 *1/10* — Nikni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return B_NIK
    if not is_number(update.message.text):
        await update.message.reply_text("❌ Faqat raqam kiriting!\n_(Masalan: 45000)_", parse_mode="Markdown")
        return B_KUBOK
    user_data_store[update.effective_user.id]["kubok"] = update.message.text
    await update.message.reply_text("⭐ *3/10* — Titullar sonini yozing _(faqat raqam)_:", parse_mode="Markdown", reply_markup=back_kb())
    return B_TITUL

async def b_titul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("🏆 *2/10* — Kubokni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return B_KUBOK
    if not is_number(update.message.text):
        await update.message.reply_text("❌ Faqat raqam kiriting!\n_(Masalan: 5)_", parse_mode="Markdown")
        return B_TITUL
    user_data_store[update.effective_user.id]["titul"] = update.message.text
    await update.message.reply_text("🥷 *4/10* — Brawlerlar sonini yozing _(faqat raqam)_:", parse_mode="Markdown", reply_markup=back_kb())
    return B_BRAWLER

async def b_brawler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("⭐ *3/10* — Titulni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return B_TITUL
    if not is_number(update.message.text):
        await update.message.reply_text("❌ Faqat raqam kiriting!", parse_mode="Markdown")
        return B_BRAWLER
    user_data_store[update.effective_user.id]["brawler"] = update.message.text
    await update.message.reply_text("🧝 *5/10* — Skinlar sonini yozing _(faqat raqam)_:", parse_mode="Markdown", reply_markup=back_kb())
    return B_SKIN

async def b_skin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("🥷 *4/10* — Brawlerni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return B_BRAWLER
    if not is_number(update.message.text):
        await update.message.reply_text("❌ Faqat raqam kiriting!", parse_mode="Markdown")
        return B_SKIN
    user_data_store[update.effective_user.id]["skin"] = update.message.text
    await update.message.reply_text("💎 *6/10* — Gemlar sonini yozing _(faqat raqam)_:", parse_mode="Markdown", reply_markup=back_kb())
    return B_GEM

async def b_gem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("🧝 *5/10* — Skinni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return B_SKIN
    if not is_number(update.message.text):
        await update.message.reply_text("❌ Faqat raqam kiriting!", parse_mode="Markdown")
        return B_GEM
    user_data_store[update.effective_user.id]["gem"] = update.message.text
    await update.message.reply_text("⚡ *7/10* — Giperzaryad sonini yozing _(faqat raqam)_:", parse_mode="Markdown", reply_markup=back_kb())
    return B_GIPER

async def b_giper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("💎 *6/10* — Gemni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return B_GEM
    if not is_number(update.message.text):
        await update.message.reply_text("❌ Faqat raqam kiriting!", parse_mode="Markdown")
        return B_GIPER
    user_data_store[update.effective_user.id]["giper"] = update.message.text
    await update.message.reply_text("🎟 *8/10* — Brawl Pass sonini yozing _(faqat raqam)_:", parse_mode="Markdown", reply_markup=back_kb())
    return B_BPASS

async def b_bpass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("⚡ *7/10* — Giperzaryadni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return B_GIPER
    if not is_number(update.message.text):
        await update.message.reply_text("❌ Faqat raqam kiriting!", parse_mode="Markdown")
        return B_BPASS
    user_data_store[update.effective_user.id]["bpass"] = update.message.text
    await update.message.reply_text("🤑 *9/10* — Narxini yozing _(so'mda, faqat raqam)_:", parse_mode="Markdown", reply_markup=back_kb())
    return B_NARX

async def b_narx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("🎟 *8/10* — Brawl Passni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return B_BPASS
    if not is_number(update.message.text):
        await update.message.reply_text("❌ Faqat raqam kiriting!\n_(Masalan: 500000)_", parse_mode="Markdown")
        return B_NARX
    user_data_store[update.effective_user.id]["narx"] = update.message.text
    await update.message.reply_text("📱 *10/10* — Murojaat uchun username yoki tel raqam:", parse_mode="Markdown", reply_markup=back_kb())
    return B_MUROJAAT

async def b_murojaat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("🤑 *9/10* — Narxni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return B_NARX
    if not is_valid_contact(update.message.text):
        await update.message.reply_text("❌ To'g'ri username (@username) yoki tel raqam kiriting!", parse_mode="Markdown")
        return B_MUROJAAT
    user_data_store[update.effective_user.id]["murojaat"] = update.message.text
    await update.message.reply_text(
        "📸 Akkaunt skrinshotini yuboring!\n_(Rasm yoki video)_",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    return B_MEDIA

async def b_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    d = user_data_store.get(uid, {})
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    elon = (
        f"•••••| D I Q Q A T | E L O N |•••••\n\n"
        f"🟡 BRAWL STARS AKKAUNT SOTILADI\n\n"
        f"📋 Nik: {d.get('nik', '-')}\n"
        f"🏆 Kubok: {d.get('kubok', '-')}\n"
        f"⭐ Titul: {d.get('titul', '-')}\n"
        f"🥷 Brawler: {d.get('brawler', '-')}\n"
        f"🧝 Skinlar: {d.get('skin', '-')}\n"
        f"💎 Gem: {d.get('gem', '-')}\n"
        f"⚡ Giperzaryad: {d.get('giper', '-')}\n"
        f"🎟 Brawl Pass: {d.get('bpass', '-')}\n\n"
        f"🤑 Narxi: {d.get('narx', '-')} so'm\n"
        f"📲 Murojaat: {d.get('murojaat', '-')}\n\n"
        f"Savdo {ADMIN_USERNAME} orqali yoki ko'rishib sotiladi ✅\n"
        f"Obmen yo'q ❌\n\n"
        f"❗️ Adminsiz savdo qilmang!\n"
        f"🤝 Garant: {ADMIN_USERNAME}\n\n"
        f"📌 Kanal: https://t.me/NeytenYT\n"
        f"🕐 {now}"
    )

    kb = [[
        InlineKeyboardButton("✅ Kanalga yuborish", callback_data="b_confirm"),
        InlineKeyboardButton("❌ Bekor", callback_data="cancel")
    ]]

    if update.message.photo:
        await update.message.reply_photo(
            photo=update.message.photo[-1].file_id,
            caption=elon,
            reply_markup=InlineKeyboardMarkup(kb)
        )
        user_data_store[uid]["photo"] = update.message.photo[-1].file_id
        user_data_store[uid]["media_type"] = "photo"
    elif update.message.video:
        await update.message.reply_video(
            video=update.message.video.file_id,
            caption=elon,
            reply_markup=InlineKeyboardMarkup(kb)
        )
        user_data_store[uid]["video"] = update.message.video.file_id
        user_data_store[uid]["media_type"] = "video"
    else:
        await update.message.reply_text("❌ Faqat rasm yoki video yuboring!")
        return B_MEDIA

    user_data_store[uid]["elon_text"] = elon
    user_data_store[uid]["type"] = "brawl"
    return ConversationHandler.END

# ─── PUBG MOBILE ──────────────────────────
async def p_tier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("🎮 O'yinni tanlang:", reply_markup=oyun_kb())
        return OYUN
    user_data_store[update.effective_user.id]["tier"] = update.message.text
    await update.message.reply_text("💰 *2/7* — UC miqdorini yozing _(faqat raqam)_:", parse_mode="Markdown", reply_markup=back_kb())
    return P_UC

async def p_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("🏆 *1/7* — Tierni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return P_TIER
    if not is_number(update.message.text):
        await update.message.reply_text("❌ Faqat raqam kiriting!\n_(Masalan: 5000)_", parse_mode="Markdown")
        return P_UC
    user_data_store[update.effective_user.id]["uc"] = update.message.text
    await update.message.reply_text("👗 *3/7* — Skinlar sonini yozing _(faqat raqam)_:", parse_mode="Markdown", reply_markup=back_kb())
    return P_SKIN

async def p_skin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("💰 *2/7* — UCni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return P_UC
    if not is_number(update.message.text):
        await update.message.reply_text("❌ Faqat raqam kiriting!", parse_mode="Markdown")
        return P_SKIN
    user_data_store[update.effective_user.id]["p_skin"] = update.message.text
    await update.message.reply_text("🤑 *4/7* — Narxini yozing _(so'mda, faqat raqam)_:", parse_mode="Markdown", reply_markup=back_kb())
    return P_NARX

async def p_narx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("👗 *3/7* — Skinni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return P_SKIN
    if not is_number(update.message.text):
        await update.message.reply_text("❌ Faqat raqam kiriting!\n_(Masalan: 300000)_", parse_mode="Markdown")
        return P_NARX
    user_data_store[update.effective_user.id]["narx"] = update.message.text
    await update.message.reply_text("🏠 *5/7* — Manzilingizni yozing _(shahar)_:", parse_mode="Markdown", reply_markup=back_kb())
    return P_MANZIL

async def p_manzil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("🤑 *4/7* — Narxni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return P_NARX
    user_data_store[update.effective_user.id]["manzil"] = update.message.text
    await update.message.reply_text("📱 *6/7* — Murojaat uchun username yoki tel raqam:", parse_mode="Markdown", reply_markup=back_kb())
    return P_MUROJAAT

async def p_murojaat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text("🏠 *5/7* — Manzilni qayta yozing:", parse_mode="Markdown", reply_markup=back_kb())
        return P_MANZIL
    if not is_valid_contact(update.message.text):
        await update.message.reply_text("❌ To'g'ri username (@username) yoki tel raqam kiriting!")
        return P_MUROJAAT
    user_data_store[update.effective_user.id]["murojaat"] = update.message.text
    await update.message.reply_text(
        "📸 *7/7* — Akkaunt skrinshotini yuboring!\n_(Rasm yoki video)_",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    return P_MEDIA

async def p_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    d = user_data_store.get(uid, {})
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    elon = (
        f"Account Sotiladi Global 👌\n\n"
        f"🎮 PUBG MOBILE AKKAUNT\n\n"
        f"📈🔥 Tier/Rang: {d.get('tier', '-')}\n"
        f"💰 UC: {d.get('uc', '-')}\n"
        f"👗 Skinlar: {d.get('p_skin', '-')}\n\n"
        f"🤑 Narxi: {d.get('narx', '-')} so'm\n"
        f"🏠 Manzil: {d.get('manzil', '-')}\n\n"
        f"📲 Tg murojaat: {d.get('murojaat', '-')}\n\n"
        f"Savdo {ADMIN_USERNAME} orqali yoki ko'rishib sotiladi ✅\n"
        f"Obmen yo'q ❌\n\n"
        f"✅ Adminsiz bo'lgan savdoga kanal admini javobgar emas ❗️\n"
        f"❗️ Adminsiz savdo qilmang!\n"
        f"🤝 O'rtada Garant bo'lib beramiz: {ADMIN_USERNAME}\n\n"
        f"📌 Asosiy kanal: https://t.me/player2748\n"
        f"2️⃣ Kanal: https://t.me/uzbekistancomminuty\n"
        f"🕐 {now}"
    )

    kb = [[
        InlineKeyboardButton("✅ Kanalga yuborish", callback_data="p_confirm"),
        InlineKeyboardButton("❌ Bekor", callback_data="cancel")
    ]]

    if update.message.photo:
        await update.message.reply_photo(
            photo=update.message.photo[-1].file_id,
            caption=elon,
            reply_markup=InlineKeyboardMarkup(kb)
        )
        user_data_store[uid]["photo"] = update.message.photo[-1].file_id
        user_data_store[uid]["media_type"] = "photo"
    elif update.message.video:
        await update.message.reply_video(
            video=update.message.video.file_id,
            caption=elon,
            reply_markup=InlineKeyboardMarkup(kb)
        )
        user_data_store[uid]["video"] = update.message.video.file_id
        user_data_store[uid]["media_type"] = "video"
    else:
        await update.message.reply_text("❌ Faqat rasm yoki video yuboring!")
        return P_MEDIA

    user_data_store[uid]["elon_text"] = elon
    user_data_store[uid]["type"] = "pubg"
    return ConversationHandler.END

# ─── ADMIN XABARNOMA ──────────────────────
async def notify_admin(context, user, elon_type, d):
    if not ADMIN_CHAT_ID:
        return
    try:
        username = f"@{user.username}" if user.username else f"ID: {user.id}"
        if elon_type == "brawl":
            msg = (
                f"🔔 *YANGI BRAWL E'LON!*\n\n"
                f"👤 Foydalanuvchi: {username}\n"
                f"📋 Nik: {d.get('nik', '-')}\n"
                f"🏆 Kubok: {d.get('kubok', '-')}\n"
                f"🤑 Narxi: {d.get('narx', '-')} so'm\n"
                f"📣 Kanal: @NeytenYT\n\n"
                f"✅ E'lon yuborildi!"
            )
        else:
            msg = (
                f"🔔 *YANGI PUBG E'LON!*\n\n"
                f"👤 Foydalanuvchi: {username}\n"
                f"🏆 Tier: {d.get('tier', '-')}\n"
                f"💰 UC: {d.get('uc', '-')}\n"
                f"🤑 Narxi: {d.get('narx', '-')} so'm\n"
                f"🏠 Manzil: {d.get('manzil', '-')}\n"
                f"📣 Kanallar: @player2748 va @uzbekistancomminuty\n\n"
                f"✅ E'lon yuborildi!"
            )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Admin xabarnoma xatosi: {e}")

# ─── CALLBACK ─────────────────────────────
async def button_callback(update, context):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    user = query.from_user
    d = user_data_store.get(uid, {})

    if query.data == "b_confirm":
        try:
            if d.get("media_type") == "photo":
                await context.bot.send_photo(chat_id=BRAWL_KANAL, photo=d["photo"], caption=d["elon_text"])
            elif d.get("media_type") == "video":
                await context.bot.send_video(chat_id=BRAWL_KANAL, video=d["video"], caption=d["elon_text"])
            elon_count["brawl"] += 1
            logger.info(f"Brawl e'lon yuborildi: {user.username} ({uid})")
            await notify_admin(context, user, "brawl", d)
            await query.edit_message_caption(
                caption=f"✅ E'loningiz @NeytenYT kanaliga yuborildi!\n\n🤝 Garant: {ADMIN_USERNAME}"
            )
        except Exception as e:
            logger.error(f"Brawl e'lon xatosi: {e}")
            await query.edit_message_caption(caption=f"❌ Xatolik yuz berdi: {e}\n\nAdmin bilan bog'laning: {ADMIN_USERNAME}")

    elif query.data == "p_confirm":
        try:
            success = []
            errors = []
            for kanal in PUBG_KANALLAR:
                try:
                    if d.get("media_type") == "photo":
                        await context.bot.send_photo(chat_id=kanal, photo=d["photo"], caption=d["elon_text"])
                    elif d.get("media_type") == "video":
                        await context.bot.send_video(chat_id=kanal, video=d["video"], caption=d["elon_text"])
                    success.append(kanal)
                except Exception as e:
                    logger.error(f"{kanal} ga yuborishda xato: {e}")
                    errors.append(kanal)

            if success:
                elon_count["pubg"] += 1
                await notify_admin(context, user, "pubg", d)
                success_text = "\n".join([f"✅ {k}" for k in success])
                error_text = "\n".join([f"❌ {k}" for k in errors]) if errors else ""
                msg = f"E'loningiz yuborildi!\n\n{success_text}"
                if error_text:
                    msg += f"\n\nXato:\n{error_text}"
                await query.edit_message_caption(caption=msg)
            else:
                await query.edit_message_caption(caption=f"❌ Yuborishda xato!\nAdmin: {ADMIN_USERNAME}")

            logger.info(f"PUBG e'lon: {user.username} — {success}")
        except Exception as e:
            logger.error(f"PUBG umumiy xato: {e}")
            await query.edit_message_caption(caption=f"❌ Xatolik: {e}")

    elif query.data == "cancel":
        await query.edit_message_caption(caption="❌ E'lon bekor qilindi.\n\n/start — qayta boshlash")

# ─── CANCEL ───────────────────────────────
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.", reply_markup=main_kb())
    return ConversationHandler.END

# ─── MAIN ─────────────────────────────────
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📝 E'lon berish$"), menu_handler)],
        states={
            OYUN: [MessageHandler(filters.TEXT & ~filters.COMMAND, oyun_handler)],
            B_NIK: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_nik)],
            B_KUBOK: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_kubok)],
            B_TITUL: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_titul)],
            B_BRAWLER: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_brawler)],
            B_SKIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_skin)],
            B_GEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_gem)],
            B_GIPER: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_giper)],
            B_BPASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_bpass)],
            B_NARX: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_narx)],
            B_MUROJAAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_murojaat)],
            B_MEDIA: [MessageHandler(filters.PHOTO | filters.VIDEO, b_media)],
            P_TIER: [MessageHandler(filters.TEXT & ~filters.COMMAND, p_tier)],
            P_UC: [MessageHandler(filters.TEXT & ~filters.COMMAND, p_uc)],
            P_SKIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, p_skin)],
            P_NARX: [MessageHandler(filters.TEXT & ~filters.COMMAND, p_narx)],
            P_MANZIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, p_manzil)],
            P_MUROJAAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, p_murojaat)],
            P_MEDIA: [MessageHandler(filters.PHOTO | filters.VIDEO, p_media)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("✅ Veron Bot ishga tushdi!")
    print("📌 Brawl kanal: @NeytenYT")
    print("📌 PUBG kanallar: @uzbekistancomminuty, @player2748")
    print("👮 Admin: @Veron_Garant")
    app.run_polling()

if name == "main":
    main()
