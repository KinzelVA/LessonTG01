from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Основное меню с кнопками "Привет" и "Пока"
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет")],
        [KeyboardButton(text="Пока")],
    ],
    resize_keyboard=True
)

# Инлайн-клавиатура с URL-ссылками
url_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новости", url="https://news.yandex.ru")],
    [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru")],
    [InlineKeyboardButton(text="Видео", url="https://yandex.ru/video")]
])

# Инлайн-клавиатура для динамического изменения
show_more_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
])

options_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
    [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
])

