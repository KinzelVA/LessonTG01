import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


API_KEY = "0571c8dec7a964f9d24a2b45888aa0f1"  # Замените на ваш API ключ

bot = Bot(token="6943602251:AAHV3rXWQltWOT8aRXyl7pDahm-6x0kd6vU")
dp = Dispatcher()

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help \n /weather")

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

async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем вебхуки перед началом работы
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
