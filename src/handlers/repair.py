from telebot import TeleBot
from telebot.types import Message
from datetime import datetime
from src.database.db import RepairRequest, repair_requests
from src.utils.helpers import user_states

def register_repair_handlers(bot: TeleBot):
    @bot.message_handler(commands=['repair'])
    def start_repair_request(message: Message):
        user_id = message.from_user.id
        user_states[user_id] = 'waiting_for_model'
        repair_requests[user_id] = RepairRequest()
        bot.reply_to(message, "Пожалуйста, укажите модель вашего телефона:") 