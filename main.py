import logging
import re

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4466,,!!",
    port="3306",
    database="beztwena"
)

cursor = db.cursor()
# cursor.execute("DROP TABLE users")
# cursor.execute("CREATE TABLE users (id INT NOT NULL AUTO_INCREMENT, user_id INT UNSIGNED NULL, name VARCHAR(45) NULL, age INT NOT NULL, gender VARCHAR(45) NOT NULL, email VARCHAR(45) NULL, weight INT NULL, telephone VARCHAR(45) NULL, PRIMARY KEY (id))")

# sql = "INSERT INTO users (name, age, gender, email, weight, telephone, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
# val = ("Sanya", "42", "Чоловік", "sasha123@gmail.com", "76", "0987655546", 6)
# cursor.execute(sql, val)
# db.commit()

# print(cursor.rowcount, "запис добавлений.")

# sql = "INSERT INTO users (name, age, gender, email, weight, telephone, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
# val = [
#  ('Nick', '43', 'Чоловік', 'nick@gmail.com', '87', '0985655576', 2),
#  ('Mary', '13', 'Жінка', 'matty@gmail.com', '47', '0635655576', 3),
#  ('Jon', '33', 'Чоловік', 'john@gmail.com', '97', '0505655576', 4),
# ]

# cursor.executemany(sql, val)

# db.commit()

# print(cursor.rowcount, "записи добавлені.")

logging.basicConfig(level=logging.INFO)

API_TOKEN = '2137005184:AAHwKMgWpr_QYzQMDiBBpn3EUYGnbYAzDB4'

# 2129667283:AAENu9KxnyqobfH2VbVr3eG8mrF9-3c_dBo
bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
email_re = re.compile(pattern)

pattern = r'(\w{3})\w{3}\w{4}'
phone_re = re.compile(pattern)


# States
class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    age = State()  # Will be represented in storage as 'Form:age'
    gender = State()  # Will be represented in storage as 'Form:gender'
    email = State()
    weight = State()
    phone = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.name.set()

    await message.reply("Привіт, давай заповнювати заявку на нашу програму тренувань! 😃\nТвоє ім'я? 🤓")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: not message.text.isalpha(), state=Form.name)
async def process_name_invalid(message: types.Message):
    return await message.reply("Вводь буквами! 😕")


@dp.message_handler(lambda message: message.text.isalpha(), state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("Скільки тобі років? 🤓")


# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def process_age_invalid(message: types.Message):
    """
    If age is invalid
    """
    return await message.reply("Вводь цифрами 😕\nСкільки тобі років?")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(age=int(message.text))

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Чоловік", "Жінка")
    markup.add("Інше")

    await message.reply("Твоя стать? 🤓", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["Чоловік", "Жінка", "Інше"], state=Form.gender)
async def process_gender_invalid(message: types.Message):
    """
    In this example gender has to be one of: Male, Female, Other.
    """
    return await message.reply("Не правильно 😕\nВибери свою стать з кнопок!")


@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, text="Твій email? 🤓", reply_markup=markup)
    # Finish conversation
    await Form.next()


@dp.message_handler(lambda msg: not re.match(email_re, msg.text), state=Form.email)
async def process_email_invalid(message: types.Message):
    text = 'Ти ввів неправильну пошту 😕\nСпробуй ще раз!'
    await bot.send_message(message.chat.id, text=text)


@dp.message_handler(lambda msg: re.match(email_re, msg.text), state=Form.email)
async def process_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

    await Form.next()
    await bot.send_message(message.chat.id, text="Твоя вага? 🤓 ")


@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.weight)
async def process_weight_invalid(message: types.Message):
    text = 'Ти ввів неправильну вагу 😕\nСпробуй ще раз!'
    await bot.send_message(message.chat.id, text=text)


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.weight)
async def process_weight(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weight'] = message.text

    await Form.next()
    await bot.send_message(message.chat.id, text="Твій номер тлефону? 🤓")


@dp.message_handler(lambda msg: not re.match(phone_re, msg.text), state=Form.phone)
async def process_phone_invalid(message: types.Message):
    text = 'Ти ввів неправильний номер телефону 😕\nСпробуй ще раз!'
    await bot.send_message(message.chat.id, text=text)


@dp.message_handler(lambda msg: re.match(phone_re, msg.text), state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    # And send message
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('📨Твоя заяка: ', md.bold(data['name'])),
            md.text('🗓Вік:', md.code(data['age'])),
            md.text('📌Вага:', data['weight']),
            md.text('🧬Пол:', data['gender']),
            md.text('📞Телефон:', data['phone']),
            md.text('📧Email:', data['email']),
            sep='\n',
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
    sql = "INSERT INTO users (name, age, gender, email, weight, telephone, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (data['name'], data['age'], data['gender'], data['email'], data['weight'], data['phone'], message.from_user.id)
    cursor.execute(sql, val)
    db.commit()

    # Finish conversation

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
