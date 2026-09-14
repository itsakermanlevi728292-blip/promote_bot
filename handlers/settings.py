from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import OWNER_ID

NOTIF_SETTINGS = {
    "promotion": True,
    "ban": True,
    "restrict": True,
    "member": False,
    "settings": True,
    "vc": False,
}

async def settings_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    await send_settings(update)

async def send_settings(update):
    kb_rows = []
    for key, label in [
        ("promotion", "👑 Admin Changes"),
        ("ban", "🔨 Ban/Unban"),
        ("restrict", "🔇 Restrict/Unrestrict"),
        ("member", "👤 Join/Leave"),
        ("settings", "⚙️ Group Changes"),
        ("vc", "🎙️ VC Events"),
    ]:
        state = "ON" if NOTIF_SETTINGS[key] else "OFF"
        kb_rows.append([InlineKeyboardButton(f"{label}: {state}", callback_data=f"set_toggle_{key}")])
    kb = InlineKeyboardMarkup(kb_rows)
    text = "🔔 <b>NOTIFICATION SETTINGS</b>"
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=kb, parse_mode="HTML")
    else:
        await update.message.reply_text(text, reply_markup=kb, parse_mode="HTML")

async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != OWNER_ID:
        return
    if query.data.startswith("set_toggle_"):
        key = query.data.replace("set_toggle_", "")
        NOTIF_SETTINGS[key] = not NOTIF_SETTINGS[key]
        await send_settings(update)
