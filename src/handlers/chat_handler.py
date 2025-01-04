from openai import OpenAI
from telebot import TeleBot
from telebot.types import Message
from src.utils.helpers import (
    add_to_chat_history, 
    chat_histories,
    chat_contexts
)
from config import SYSTEM_INSTRUCTION, ADMIN_ID, OPENAI_API_KEY

# Самая простая инициализация клиента
client = OpenAI()

def handle_message(bot: TeleBot, message: Message):
    try:
        user_id = message.from_user.id
        user_message = message.text
        
        add_to_chat_history(user_id, "user", user_message)
        
        # Получаем сохраненный контекст беседы
        context = chat_contexts.get(user_id, "Контекст отсутствует")
        
        # Формируем полную инструкцию с контекстом
        full_instruction = f"""{SYSTEM_INSTRUCTION}

ТЕКУЩИЙ КОНТЕКСТ БЕСЕДЫ:
{context}

На основе этого контекста и новых сообщений продолжайте консультацию."""

        # Формируем сообщения для API
        messages = [
            {"role": "system", "content": full_instruction}
        ] + chat_histories[user_id][-3:]  # Добавляем последние 3 сообщения
        
        print("\nОтправляем в OpenAI:")
        print(f"Контекст беседы: {chat_contexts.get(user_id, 'нет контекста')}")
        for msg in messages:
            print(f"{msg['role']}: {msg['content']}\n")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        ai_response = response.choices[0].message.content
        add_to_chat_history(user_id, "assistant", ai_response)
        
        # Проверяем наличие метки для создания заявки
        if "[[CREATE_REPAIR_REQUEST]]" in ai_response:
            # Удаляем метку из ответа пользователю
            clean_response = ai_response.replace("[[CREATE_REPAIR_REQUEST]]", "")
            
            # Извлекаем информацию о заявке
            repair_info = extract_repair_info(chat_histories[user_id])
            admin_message = format_repair_request(repair_info)
            
            # Отправляем заявку админу
            bot.send_message(ADMIN_ID, admin_message)
            bot.reply_to(message, clean_response)
        else:
            bot.reply_to(message, ai_response)
            
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        bot.reply_to(message, "Извините, произошла ошибка. Попробуйте повторить сообщение.")

def extract_repair_info(chat_history):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Извлеките из истории чата: модель телефона и описание проблемы. Верните в формате JSON."},
                {"role": "user", "content": str(chat_history)}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при извлечении информации: {str(e)}")
        return "Ошибка при обработке заявки"

def format_repair_request(repair_info):
    return f"""
📱 Новая заявка на ремонт!

{repair_info}
    """ 