import asyncio
from telegram.ext import ApplicationBuilder, ChatMemberHandler, CommandHandler, CallbackQueryHandler
from telegram import Update
from config import BOT_TOKEN, OWNER_ID
from database import init_db
from handlers.start import start, help_cmd
from handlers.logs import logs_cmd, stats_cmd, logs_callback
from handlers.settings import settings_cmd, settings_callback
from services.audit import handle_chat_member_update

async def on_chat_member(update: Update, context):
    result = await handle_chat_member_update(update.chat_member, context)
    if not result:
        return
    try:
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=result["text"],
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Audit delivery failed: {e}")

async def post_init(app):
    await init_db()

def main():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("logs", logs_cmd))
    app.add_handler(CommandHandler("settings", settings_cmd))
    app.add_handler(CallbackQueryHandler(logs_callback, pattern="^logs_"))
    app.add_handler(CallbackQueryHandler(settings_callback, pattern="^set_"))
    app.add_handler(ChatMemberHandler(on_chat_member, ChatMemberHandler.CHAT_MEMBER))

    app.run_polling(allowed_updates=["chat_member", "callback_query", "message"])

if __name__ == "__main__":
    main()
