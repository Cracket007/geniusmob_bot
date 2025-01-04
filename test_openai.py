from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def test_openai_key():
    try:
        client = OpenAI()
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}]
        )
        
        print("✅ API ключ работает корректно")
        print(f"Ответ: {completion.choices[0].message.content}")
            
    except Exception as e:
        print("❌ Ошибка при проверке API ключа:")
        print(f"Тип ошибки: {type(e).__name__}")
        print(f"Описание: {str(e)}")

if __name__ == "__main__":
    test_openai_key() 