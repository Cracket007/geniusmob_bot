from telebot import TeleBot
from telebot.types import Message
import openai
from src.utils.helpers import user_states

def register_consultation_handlers(bot: TeleBot):
    @bot.message_handler(commands=['consult'])
    def start_consultation(message: Message):
        user_id = message.from_user.id
        user_states[user_id] = 'consultation'
        bot.reply_to(message, "Опишите вашу проблему, и я постараюсь помочь:") 