from aiogram import Bot, types, Dispatcher, executor
from dotenv import load_dotenv
from list import cs
from keyboards import nomer, mesto, button
import logging,time, os

db = cs()
connect = db.connect
db.connect_db()

load_dotenv('.env')

bot = Bot(os.environ.get('TOKEN'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Здраствуйте {message.from_user.full_name}")
    await message.answer(f"я бот для заказа пиццы",reply_markup=button)
    cursor = connect.cursor()
    cursor.execute(f'SELECT user_id FROM customers WHERE user_id = {message.from_user.id};')
    result = cursor.fetchall()
    if result == []:
        cursor.execute(f"INSERT INTO customers VALUES ('{message.from_user.first_name}', '{message.from_user.last_name}', '{message.from_user.username}', '{message.from_user.id}', 'None');")
    connect.commit()

@dp.callback_query_handler(lambda call : call)
async def inline(call):
    if call.data == 'nomer':
        await get_number(call.message)
    elif call.data == 'mesto':
        await get_location(call.message)
    elif call.data == 'pizza':
        await take_order(call.message)

@dp.message_handler(commands='number')
async def get_number(message:types.Message):
    await message.answer('Подтвердите отправку своего номера.', reply_markup=nomer)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def piz(message:types.Message):
    cursor = connect.cursor()
    cursor.execute(f"UPDATE customers SET phone_number = '{message.contact['phone_number']}' WHERE user_id = {message.from_user.id};")
    connect.commit()
    await message.answer("Ваш номер успешно добавлен.")

@dp.message_handler(commands='location')
async def get_location(message:types.Message):
    await message.answer("Отправьте адрес.", reply_markup=mesto)

@dp.message_handler(content_types=types.ContentType.LOCATION)
async def fuga(message:types.Message):
    await message.answer("Ваш адрес записан.")
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO address VALUES ('{message.from_user.id}', '{message.location.longitude}', '{message.location.latitude}');")
    connect.commit()

@dp.message_handler(commands='take_order')
async def take_order(message:types.Message):
    await message.reply(f"так {message.from_user.first_name} вот наше меню")
    with open("12.jpg", "rb") as pic1:
        await message.answer_photo(pic1)
    
    with open("13.jpg", "rb") as pic2:
        await message.answer_photo(pic2)
    
    with open("14.jpg", "rb") as pic3:
        await message.answer_photo(pic3)

    with open("15.jpg", "rb") as pic4:
        await message.answer_photo(pic4)


@dp.message_handler(text=[1,2,3,4])
async def li(message:types.Message):
    cursor = connect.cursor()
    if message.text == '1':
        cursor.execute(f"INSERT INTO orders VALUES('Салями', 'None', '{time.ctime()}');")
        await message.answer("Салями")
    elif message.text == '2':
        cursor.execute(f"INSERT INTO orders VALUES('Восточная', 'None', '{time.ctime()}');")
        await message.answer("Восточная")
    elif message.text == '3':
        cursor.execute(f"INSERT INTO orders VALUES('Ассорти', 'None', '{time.ctime()}');")
        await message.answer("Ассорти")
    elif message.text == '4':
        cursor.execute(f"INSERT INTO orders VALUES('Манако', 'None', '{time.ctime()}');")
        await message.answer("Манако")
    
    connect.commit()
    await message.reply("заказ принят ожидайте")

@dp.message_handler()
async def pidr(message:types.Message):
    await message.reply("Ошибка! у меня нет таких команд вот мои команды", reply_markup=button)
executor.start_polling(dp)