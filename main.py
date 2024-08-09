import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
from gtts import gTTS
import os
from googletrans import Translator
import logging
from config import TOKEN, WEATHER_API_KEY


logging.basicConfig(level=logging.INFO)


API_KEY = WEATHER_API_KEY # Замените на ваш API ключ

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создание или подключение к базе данных
conn = sqlite3.connect('school_data.db')
cursor = conn.cursor()

# Создание таблицы students
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    grade TEXT
)
''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
# Определение состояний
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

# Хранилище для временного хранения данных пользователя
user_data = {}

# Запрос имени
@dp.message(Command('start'))
async def start_message(message: Message, state: FSMContext):
    await message.answer("Привет! Введите ваше имя.")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    user_data['name'] = message.text
    await message.answer("Введите ваш возраст.")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def get_age(message: Message, state: FSMContext):
    try:
        user_data['age'] = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст.")
        return
    await message.answer("Введите ваш класс.")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def get_grade(message: Message, state: FSMContext):
    user_data['grade'] = message.text
    save_to_database(user_data)
    await message.answer("Данные сохранены. Спасибо!")
    await state.clear()

def save_to_database(data):
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (name, age, grade) 
        VALUES (?, ?, ?)
    ''', (data['name'], data['age'], data['grade']))
    conn.commit()
    conn.close()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем вебхуки перед началом работы
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
