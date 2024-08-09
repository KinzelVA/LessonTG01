import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
import random
from gtts import gTTS
import os
from googletrans import Translator, LANGUAGES
import logging
import executor
from config import TOKEN, WEATHER_API_KEY

logging.basicConfig(level=logging.INFO)


API_KEY = WEATHER_API_KEY # Замените на ваш API ключ

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help \n /weather \n /translate \n /voice \n /training")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")

@dp.message(Command('weather'))
async def weather(message: Message):
    weather_data = await get_weather("Moscow")
    await message.answer(weather_data)

async def get_weather(city: str) -> str:
    async with aiohttp.ClientSession() as session:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
        async with session.get(url) as response:
            data = await response.json()
            if response.status == 200:
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                feels_like = data['main']['feels_like']
                return (f"Погода в {city}:\n"
                        f"Описание: {weather_description}\n"
                        f"Температура: {temperature}°C\n"
                        f"Ощущается как: {feels_like}°C")
            else:
                return "Не удалось получить данные о погоде. Попробуйте позже."



@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')


# Хэндлер на команду /start
@dp.message(Command('translate'))
async def send_welcome(message: Message):
    await message.answer("Привет! Напиши мне любой текст, и я переведу его на английский язык.")

# Хэндлер на все остальные сообщения
@dp.message()
async def translate_message(message: Message):
    translated = translator.translate(message.text, dest='en')
    await message.answer(translated.text)

@dp.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

   tts = gTTS(text=rand_tr, lang='ru')
   tts.save("training.ogg")
   audio = FSInputFile('training.ogg')
   await bot.send_audio(message.chat.id, audio)
   os.remove("training.ogg")
@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем вебхуки перед началом работы
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
