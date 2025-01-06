from telebot import TeleBot
from config import TELEGRAM_TOKEN
from src.handlers.chat_handler import handle_message

def main():
    bot = TeleBot(TELEGRAM_TOKEN)
    
    # Регистрируем только один обработчик для всех сообщений
    @bot.message_handler(func=lambda message: True)
    def handle_all(message):
        handle_message(bot, message)
    
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
