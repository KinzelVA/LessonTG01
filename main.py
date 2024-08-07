import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


bot = Bot(token="")
dp = Dispatcher()

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")

@dp.message(Command('translate'))
async def translate(message: Message):
    text_to_translate = message.text[len("/translate "):].strip()
    if not text_to_translate:
        await message.answer("Пожалуйста, укажите текст для перевода после команды /translate.")
        return
    print(text_to_translate)
    try:
        translated = translator.translate(text_to_translate, dest='en')
        await message.answer(f"Перевод:\n{translated.text}")
    except Exception as e:
        await message.answer(f"Ошибка при переводе: {str(e)}")
    print(translated.text)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())