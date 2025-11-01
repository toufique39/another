import asyncio
import websockets
import json
import os
from telegram import Bot
from utils import log, send_audio_to_telegram

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
ORANGE_SOCKET_URL = os.environ.get("ORANGE_SOCKET_URL")
AUDIO_BASE_URL = os.environ.get("AUDIO_BASE_URL")
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", 5))

bot = Bot(token=BOT_TOKEN)

async def listen_calls():
    log("📡 Connecting to OrangeCarrier live call socket...")
    async for websocket in websockets.connect(ORANGE_SOCKET_URL):
        try:
            async for message in websocket:
                data = json.loads(message)
                call_id = data.get("call_id")
                caller = data.get("caller")
                audio_file = f"{AUDIO_BASE_URL}/{call_id}.wav"

                log(f"📞 Incoming Call Detected: {caller}")
                await send_audio_to_telegram(bot, ADMIN_CHAT_ID, audio_file)
        except Exception as e:
            log(f"⚠️ Connection lost! Retrying... ({e})")
            await asyncio.sleep(CHECK_INTERVAL)
            continue

def start_listener():
    asyncio.run(listen_calls())
