import os
import tempfile
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler,
    ContextTypes, filters
)
from aiohttp import web

from funzioni_dati.media_aritmetica import calc_media_e_salva
from bot.handlers import start, handle_choice, handle_numbers

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# 🌐 Web server per Render
async def handle_ping(request):
    return web.Response(text="✅ Bot attivo")

# 🚀 Avvio bot e server aiohttp
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_choice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_numbers))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    web_app = web.Application()
    web_app.router.add_get("/", handle_ping)

    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
    await site.start()

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
