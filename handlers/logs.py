from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import OWNER_ID
from database import async_session, AuditLog
from sqlalchemy import select, func, desc

PAGE_SIZE = 5

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    async with async_session() as session:
        total = await session.scalar(select(func.count(AuditLog.id)))
        text = f"📊 <b>AUDIT STATISTICS</b>\n\nTotal Logged Events: {total or 0}"
    await update.message.reply_text(text, parse_mode="HTML")

async def logs_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    await send_logs_page(update, context, page=0)

async def send_logs_page(update, context, page=0):
    async with async_session() as session:
        result = await session.execute(
            select(AuditLog).order_by(desc(AuditLog.timestamp)).offset(page * PAGE_SIZE).limit(PAGE_SIZE)
        )
        logs = result.scalars().all()

    if not logs:
        text = "No logs found."
    else:
        text = "📋 <b>Recent Logs</b>\n\n"
        for log in logs:
            text += f"• <b>{log.event_type}</b> in group <code>{log.group_id}</code>\n"

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("◀️ Previous", callback_data=f"logs_page_{page-1}"),
         InlineKeyboardButton("▶️ Next", callback_data=f"logs_page_{page+1}")],
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"logs_page_{page}")],
    ])

    if update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=kb)
    else:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb)

async def logs_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != OWNER_ID:
        return
    page = int(query.data.split("_")[-1])
    if page < 0:
        page = 0
    await send_logs_page(update, context, page)
