from telegram import Bot
from telegram.constants import ParseMode

class TelegramManager:
    """Async Telegram manager using python-telegram-bot v20+ (asyncio).

    Use `await send_alert(...)` when calling.
    """
    def __init__(self, token: str, chat_id: str):
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def send_alert(self, title: str, body: str, png_bytes: bytes = None):
        text = f"{title}\n{body}"
        if png_bytes:
            await self.bot.send_photo(chat_id=self.chat_id, photo=png_bytes, caption=text, parse_mode=ParseMode.HTML)
        else:
            await self.bot.send_message(chat_id=self.chat_id, text=text, parse_mode=ParseMode.HTML)
