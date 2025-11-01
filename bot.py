import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from listener import start_listener
from utils import log

# Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN environment variable not set!")

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Orange Bot is Alive and Running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Orange Carrier Bot is online and monitoring calls!")

def run_bot():
    app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    start_listener()  # Start listening to the call socket
    app_telegram.run_polling()

if __name__ == '__main__':
    log("🚀 Orange Bot Started Successfully!")
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=PORT)
