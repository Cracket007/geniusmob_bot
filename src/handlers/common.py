from telebot import TeleBot
from telebot.types import Message

def register_common_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message: Message):
        welcome_text = """
        👋 Здравствуйте! Я бот-консультант сервисного центра по ремонту смартфонов.
        
        Чем могу помочь?
        /help - показать все команды
        /repair - оставить заявку на ремонт
        /consult - получить консультацию
        """
        bot.reply_to(message, welcome_text)

    @bot.message_handler(commands=['help'])
    def send_help(message: Message):
        help_text = """
        Доступные команды:
        /start - начать общение
        /repair - оставить заявку на ремонт
        /consult - получить консультацию
        /status - проверить статус заявки
        """
        bot.reply_to(message, help_text) 