import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import logging
from config import TOKEN  # Убедитесь, что в файле config.py есть ваш токен
from datetime import datetime
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# URL для получения котировок валют от Центробанка РФ
CBR_URL = "http://www.cbr.ru/scripts/XML_daily.asp"

# Клавиатура с кнопкой "Котировки"
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Котировки")]
    ],
    resize_keyboard=True
)

# Хранилище для отслеживания состояния ожидания ввода даты
user_states = {}


async def fetch_currency_data(date: str = None) -> dict:
    """Запрашивает данные о котировках валют с сайта Центробанка РФ."""
    async with aiohttp.ClientSession() as session:
        params = {"date_req": date} if date else {}
        async with session.get(CBR_URL, params=params) as response:
            if response.status == 200:
                xml_data = await response.text()
                return parse_currency_xml(xml_data)
            else:
                return {}


def parse_currency_xml(xml_data: str) -> dict:
    """Парсит XML данные и возвращает словарь с котировками валют."""
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()
    currencies = {}
    for currency in root.findall('Valute'):
        char_code = currency.find('CharCode').text
        value = currency.find('Value').text
        currencies[char_code] = value
    return currencies


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет, я бот, который предоставляет котировки валют на основе данных Центробанка РФ.\n"
        "Для получения котировок нажмите на кнопку ниже.",
        reply_markup=start_keyboard
    )


@dp.message(F.text == "Котировки")
async def ask_for_date(message: Message):
    await message.answer("На какую дату вы хотите узнать котировки? Введите дату в формате ДД/ММ/ГГГГ:")
    user_states[message.from_user.id] = "waiting_for_date"


@dp.message()
async def handle_date_input(message: Message):
    user_id = message.from_user.id
    if user_id in user_states and user_states[user_id] == "waiting_for_date":
        try:
            date = message.text.strip()
            datetime.strptime(date, "%d/%m/%Y")  # Проверка на корректность формата
            await get_cotirovki(message, date)
        except ValueError:
            await message.answer("Неверный формат даты. Пожалуйста, используйте формат ДД/ММ/ГГГГ.")
        finally:
            user_states.pop(user_id, None)  # Удаляем пользователя из отслеживания состояния


@dp.message(Command('cotirovki'))
async def get_cotirovki(message: Message, date: str = None):
    currency_data = await fetch_currency_data(date)

    if not currency_data:
        await message.answer("Не удалось получить данные о котировках. Попробуйте позже.")
        return

    response_text = f"Котировки валют на {date if date else 'сегодня'}:\n\n"
    for char_code, value in currency_data.items():
        response_text += f"{char_code}: {value} руб.\n"

    await message.answer(response_text)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем вебхуки перед началом работы
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
