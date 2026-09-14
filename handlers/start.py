from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import OWNER_ID

MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("📊 Statistics", callback_data="menu_stats")],
    [InlineKeyboardButton("📋 Recent Logs", callback_data="menu_logs")],
    [InlineKeyboardButton("🔔 Notifications", callback_data="menu_notifs")],
    [InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings")],
    [InlineKeyboardButton("📚 Help", callback_data="menu_help")],
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    text = (
        "┌─────────────────────┐\n"
        "   <b>PROMOTE</b>\n"
        "   <i>Admin Audit System</i>\n"
        "└─────────────────────┘\n\n"
        "Select an option below:"
    )
    await update.message.reply_text(text, reply_markup=MAIN_MENU, parse_mode="HTML")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    text = (
        "<b>PROMOTE — Help</b>\n\n"
        "This bot monitors your groups and sends audit logs to your DM.\n\n"
        "<b>Commands:</b>\n"
        "/start — Main menu\n"
        "/stats — Audit statistics\n"
        "/logs — Browse recent logs\n"
        "/settings — Notification settings\n"
        "/help — This message\n\n"
        "<b>Note:</b> Telegram Bot API limitations mean some events "
        "(e.g., message deletion, VC participant join/leave) cannot be "
        "reliably logged and are not implemented."
    )
    await update.message.reply_text(text, parse_mode="HTML")
