# bot/handlers.py

import os
import tempfile
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
from funzioni_dati.media_aritmetica import calc_media
from bot.db import conn

user_state = {}

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
            output = calc_media(testo)
            await update.message.reply_text(output)

            lines = [line.strip() for line in output.splitlines() if ": " in line]

            if len(lines) < 4:
                await update.message.reply_text("❌ Errore: formato non valido, righe insufficienti.")
                return

            try:
                data = datetime.strptime(lines[0].split(": ", 1)[1], "%d/%m/%y").date()
                ora = datetime.strptime(lines[1].split(": ", 1)[1], "%H:%M").time()
                numeri = lines[2].split(": ", 1)[1]
                media = float(lines[3].split(": ", 1)[1])
            except Exception as parse_error:
                await update.message.reply_text(f"❌ Errore parsing dati: {parse_error}")
                return

            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO data_alchemist_media_aritmetica (user_id, data_stamp, ora_stamp, numeri, media)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    user_id,
                    data,
                    ora,
                    numeri,
                    media
                ))
                conn.commit()

            await update.message.reply_text("✅ Media salvata nel database!")

    except Exception as e:
        await update.message.reply_text(f"Errore: {str(e)}")
