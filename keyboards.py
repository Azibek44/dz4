from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,KeyboardButton,ReplyKeyboardMarkup
 
but1 = [
    KeyboardButton('номер',callback_data='nomer'),
    KeyboardButton('местоположение',callback_data='mesto'),
    KeyboardButton('пицца',callback_data='pizza')
]
button = InlineKeyboardMarkup().add(*but1)
but2 = [
    KeyboardButton('Подтвердите номер',request_contact=True)
]
nomer = ReplyKeyboardMarkup().add(*but2)
but3 = [
    KeyboardButton('Подтвердите местоположение', request_location=True)
]

mesto = ReplyKeyboardMarkup().add(*but3)