import datetime
from telegram import Bot

def log(message: str):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{time}] {message}")

async def send_audio_to_telegram(bot: Bot, chat_id, audio_url):
    try:
        log(f"🎧 Sending audio to Telegram: {audio_url}")
        await bot.send_audio(chat_id=chat_id, audio=audio_url, caption="📞 New Live Call Detected!")
        log("✅ Audio sent successfully!")
    except Exception as e:
        log(f"❌ Failed to send audio: {e}")
