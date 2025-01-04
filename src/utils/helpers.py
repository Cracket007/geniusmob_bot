from datetime import datetime
from typing import Dict, List
from openai import OpenAI
from config import OPENAI_API_KEY

# Самая простая инициализация клиента
client = OpenAI()

# Словарь для хранения истории и контекста
chat_histories: Dict[int, List[dict]] = {}
chat_contexts: Dict[int, str] = {}  # Новый словарь для хранения сжатого контекста
MAX_HISTORY_LENGTH = 20

def summarize_context(user_id: int) -> str:
    """Создает сжатый контекст из истории чата"""
    if user_id not in chat_histories:
        return "Новая беседа"
        
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Создайте краткое описание контекста беседы.
                    Обязательно укажите:
                    1. Модель телефона (если обсуждалась)
                    2. Проблему (если обсуждалась)
                    3. Статус обсуждения (консультация/оформление ремонта)
                    4. Важные детали (цена, сроки и т.д.)"""
                },
                {
                    "role": "user",
                    "content": str(chat_histories[user_id][-10:])
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при создании контекста: {str(e)}")
        return "Ошибка создания контекста"

def add_to_chat_history(user_id: int, role: str, content: str):
    """Добавляет сообщение в историю и обновляет контекст"""
    if user_id not in chat_histories:
        chat_histories[user_id] = []
    
    chat_histories[user_id].append({"role": role, "content": content})
    
    # Сохраняем только последние 20 сообщений
    if len(chat_histories[user_id]) > MAX_HISTORY_LENGTH:
        chat_histories[user_id] = chat_histories[user_id][-MAX_HISTORY_LENGTH:]
        
    # Обновляем контекст каждые 5 сообщений
    if len(chat_histories[user_id]) % 5 == 0:
        chat_contexts[user_id] = summarize_context(user_id)

def get_chat_context(user_id: int) -> List[dict]:
    """Возвращает системную инструкцию с контекстом и последние сообщения"""
    context = chat_contexts.get(user_id, "")
    recent_messages = chat_histories[user_id][-3:] if user_id in chat_histories else []
    
    messages = [
        {
            "role": "system",
            "content": f"""Вы - консультант сервисного центра по ремонту смартфонов.
            
Текущий контекст беседы: {context}

Используйте этот контекст при ответе."""
        }
    ]
    
    return messages + recent_messages 