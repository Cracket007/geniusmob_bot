from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from typing import Dict
from config import SYSTEM_INSTRUCTION

class ServiceCenter:
    def __init__(self):
        self.llm = ChatOpenAI()
        self.memories: Dict[int, ConversationBufferMemory] = {}
        
        # Парсер для заявок на ремонт
        response_schemas = [
            ResponseSchema(name="phone_model", description="Модель телефона"),
            ResponseSchema(name="problem", description="Проблема"),
            ResponseSchema(name="client_contact", description="Контактные данные"),
            ResponseSchema(name="need_repair", description="Нужен ли ремонт")
        ]
        self.repair_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        
        # Шаблон для создания заявок
        self.repair_prompt = PromptTemplate(
            template="""На основе диалога определите:
            1. Модель телефона
            2. Проблему
            3. Контактные данные клиента
            4. Нужен ли ремонт

            {format_instructions}
            
            Диалог:
            {chat_history}
            """,
            input_variables=["chat_history"],
            partial_variables={"format_instructions": self.repair_parser.get_format_instructions()}
        )
    
    def get_memory(self, user_id: int) -> ConversationBufferMemory:
        """Получает или создает память для пользователя"""
        if user_id not in self.memories:
            self.memories[user_id] = ConversationBufferMemory(return_messages=True)
        return self.memories[user_id]
    
    def process_message(self, user_id: int, message: str) -> str:
        """Обрабатывает сообщение пользователя"""
        memory = self.get_memory(user_id)
        
        # Формируем сообщения для API
        messages = [
            {"role": "system", "content": SYSTEM_INSTRUCTION}
        ] + memory.chat_memory.messages[-5:]  # Последние 5 сообщений
        
        print("\n=== Отправляем в OpenAI ===")
        print("🔵 System:", SYSTEM_INSTRUCTION[:100] + "...")
        for msg in memory.chat_memory.messages[-5:]:
            print(f"{'🟢' if msg.type == 'human' else '🤖'} {msg.type.capitalize()}: {msg.content}")
        
        conversation = ConversationChain(
            llm=self.llm,
            memory=memory,
            verbose=True  # Включаем подробный вывод
        )
        
        response = conversation.predict(input=message)
        print("\n=== Ответ OpenAI ===")
        print("🤖 Assistant:", response)
        
        return response
    
    def check_repair_needed(self, user_id: int) -> dict:
        """Проверяет необходимость создания заявки"""
        memory = self.get_memory(user_id)
        chat_history = memory.load_memory_variables({})["history"]
        
        print("\n=== Проверка необходимости ремонта ===")
        print("📝 Анализ последних сообщений...")
        
        repair_chain = self.llm.generate(
            [self.repair_prompt.format_prompt(chat_history=chat_history).to_string()]
        )
        
        try:
            repair_info = self.repair_parser.parse(repair_chain.generations[0][0].text)
            print("✅ Результат анализа:", repair_info)
            return repair_info
        except Exception as e:
            print("❌ Ошибка при анализе:", str(e))
            return None 