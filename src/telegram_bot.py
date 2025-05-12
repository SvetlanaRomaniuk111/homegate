from telegram import Bot

TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
bot = Bot(token=TOKEN)

def send_notification(listing):
    message = f"New apartment: {listing['title']}\nPrice: {listing['price']}\nLink: {listing['link']}"
    bot.send_message(chat_id=CHAT_ID, text=message)