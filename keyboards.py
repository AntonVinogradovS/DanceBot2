from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

secondKeyboard = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="Да", callback_data="yes")).add(InlineKeyboardButton(text="Нет", callback_data="no"))

urlKeyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Ссылка", url = "https://intensive.todes.ru/winter-prokach/"))