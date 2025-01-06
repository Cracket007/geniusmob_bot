from telebot import TeleBot
from telebot.types import Message
from src.utils.langchain_utils import ServiceCenter
from config import ADMIN_ID

service_center = ServiceCenter()

def handle_message(bot: TeleBot, message: Message):
    try:
        user_id = message.from_user.id
        user_message = message.text
        
        # Получаем ответ от LangChain
        response = service_center.process_message(user_id, user_message)
        
        # Проверяем необходимость создания заявки
        repair_info = service_center.check_repair_needed(user_id)
        
        if repair_info and repair_info.get("need_repair"):
            # Форматируем заявку для админа
            admin_message = f"""
📱 Нова заявка на ремонт!

Модель: {repair_info['phone_model']}
Проблема: {repair_info['problem']}
Контакт: {repair_info['client_contact']}
            """
            bot.send_message(ADMIN_ID, admin_message)
        
        # Отправляем ответ пользователю
        bot.send_message(message.chat.id, response)
            
    except Exception as e:
        print(f"Помилка: {str(e)}")
        bot.send_message(message.chat.id, "Вибачте, сталася помилка. Спробуйте повторити повідомлення.")