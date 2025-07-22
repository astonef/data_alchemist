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

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
user_state = {}

# 🤖 Bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Calcola Media", callback_data="media")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Che vuoi fare con i dati?", reply_markup=reply_markup)

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_state[query.from_user.id] = query.data
    await query.edit_message_text("Inserisci i numeri separati da virgola:")

async def handle_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_state:
        await update.message.reply_text("Prima scegli un'operazione con /start")
        return

    operation = user_state.pop(user_id)
    testo = update.message.text

    try:
        if operation == "media":
            with tempfile.TemporaryDirectory() as tmpdir:
                filepath = calc_media_e_salva(testo, tmpdir)
                with open(filepath, "rb") as f:
                    await update.message.reply_document(document=InputFile(f, filename=os.path.basename(filepath)))
    except Exception as e:
        await update.message.reply_text(f"Errore: {str(e)}")

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
