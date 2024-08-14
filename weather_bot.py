import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
import random
from gtts import gTTS
import os
from googletrans import Translator
import logging
from config import TOKEN, WEATHER_API_KEY
import keyboards as kb  # Импортируем клавиатуры

logging.basicConfig(level=logging.INFO)

API_KEY = WEATHER_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help \n /weather \n /translate \n /voice \n /training \n /links \n /dynamic")


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!", reply_markup=kb.main_menu)


@dp.message(F.text == "Привет")
async def hello(message: Message):
    user_name = message.from_user.first_name
    await message.answer(f"Привет, {user_name}!")


@dp.message(F.text == "Пока")
async def goodbye(message: Message):
    user_name = message.from_user.first_name
    await message.answer(f"Пока, {user_name}!")

@dp.message(Command('links'))
async def send_links(message: Message):
    await message.answer("Выберите ссылку:", reply_markup=kb.url_keyboard)


@dp.message(Command('dynamic'))
async def show_dynamic_keyboard(message: Message):
    await message.answer("Нажмите кнопку ниже:", reply_markup=kb.show_more_keyboard)


@dp.callback_query(lambda c: c.data == 'show_more')
async def show_more_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Выберите опцию:", reply_markup=kb.options_keyboard)


@dp.callback_query(lambda c: c.data == 'option_1')
async def option_1_callback(callback_query: CallbackQuery):
    await callback_query.message.answer("Вы выбрали Опцию 1")


@dp.callback_query(lambda c: c.data == 'option_2')
async def option_2_callback(callback_query: CallbackQuery):
    await callback_query.message.answer("Вы выбрали Опцию 2")


# Оставшиеся хэндлеры и функции (например, для погоды, фото, перевода и тренировок) остаются без изменений

async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем вебхуки перед началом работы
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
