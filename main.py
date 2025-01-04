import telebot
import openai
from config import TELEGRAM_TOKEN, OPENAI_API_KEY
from src.handlers.chat_handler import handle_message

# Инициализация
bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    handle_message(bot, message)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
