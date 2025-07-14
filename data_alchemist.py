import os
import tempfile
import asyncio
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

from dotenv import load_dotenv
load_dotenv()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler,
    ContextTypes, filters
)

from funzioni_dati.media_aritmetica import calc_media_e_salva
from alive import keep_alive_forever
from keep_alive_server import start_dummy_server 


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
user_state = {}

# 🌐 Dummy HTTP server for Render Web Service
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running.")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("", port), DummyServer)
    server.serve_forever()

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

# 🚀 Start dummy server and bot
if __name__ == "__main__":
    start_dummy_server()  
    loop = asyncio.get_event_loop()
    loop.create_task(keep_alive_forever())  # se vuoi anche il ping, opzionale

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_choice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_numbers))
    app.run_polling()

