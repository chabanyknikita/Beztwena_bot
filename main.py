import logging
import re

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import mysql.connector
from aiogram.types.message import ContentType
import markups as nav

LIQTOKEN = "632593626:TEST:sandbox_i29067075948"
logging.basicConfig(level=logging.INFO)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4466,,!!",
    port="3306",
    database="beztwena"
)

cursor = db.cursor()
# cursor.execute("DROP TABLE Maraphon2")
# cursor.execute("CREATE TABLE users (id INT NOT NULL AUTO_INCREMENT, user_id INT UNSIGNED NULL, name VARCHAR(45) NULL, age INT NOT NULL, gender VARCHAR(45) NOT NULL, email VARCHAR(45) NULL, weight INT NULL, telephone VARCHAR(45) NULL, PRIMARY KEY (id))")
# cursor.execute("CREATE TABLE MaraphonMax(user_id INTEGER REFERENCES users(user_id), pay VARCHAR (45))")

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
        reply_markup=nav.mainMenu
    )
    sql = "INSERT INTO users (name, age, gender, email, weight, telephone, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (
        data['name'], data['age'], data['gender'], data['email'], data['weight'], data['phone'], message.from_user.id)
    cursor.execute(sql, val)
    db.commit()

    # Finish conversation
    await state.finish()


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == 'Індивідуальна программа для схудення':
        await bot.send_message(message.from_user.id, '🏅👟Опис програми “Схуднення” : '
                                                     ' Якщо ви замітили,що набрали кілька лишніх кілограмів ,'
                                                     'відчуваєте дискомфорт '
                                                     ',або маєте бажання виглядати більш естетично, '
                                                     'то ви зробили правильний вибір, коли завітали до нас. '
                                                     'Наша команда гарантує вам результат вже за декілька тижнів'
                                                     ' плідної праці ,а також чітким графіком занять . '
                                                     'В цій програмі Ви знайдете чіткий план ваших занять'
                                                     'на один місяць. Якщо ви зацікавлені у наших послугах ,'
                                                     'то ми пропонуємо Вам придбати платну підписку на наш телеграм'
                                                     'канал з заняттями всього лиш за 149,99 грн.Ми віримо у тебе.',
                               reply_markup=nav.info_inline_markup, )

    elif message.text == 'Індивідуальна программа для набору маси':
        await bot.send_message(message.from_user.id, '🏅💪Опис програми “Набір маси” : '
                                                     'За статисткою дві третіх людства незадоволені своїм тілом, '
                                                     'якщо це про тебе ,і ти досі одягаєш світшоти з розміром S,'
                                                     'то тебе спіткала удача ,бо  ти знайшов нашу команду.'
                                                     'BezTwena Team - це топовий вибір ,'
                                                     'якщо ти маєш бажання збільшити свою статуру ,'
                                                     'а також привести твоє тіло в порядок. '
                                                     'У програмі “Набір маси” ,ти знайдеш корисну інформацію з'
                                                     ' програмою вправ на місяць, яка допоможе досягнути тобі '
                                                     'бажаного результату. Рекомендуємо  придбати платну підписку'
                                                     ' на наш телеграм канал з заняттями всього лиш за 149,99 грн. '
                                                     'Ми віримо у тебе.',

                               reply_markup=nav.More_inline_markup)


@dp.callback_query_handler(text="submonth")
async def submonth(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title="Оформлення підписки",
                           description="Покупка програми тренувань",
                           payload="month_sub", provider_token=LIQTOKEN, currency="UAH", start_parameter="test_bot",
                           prices=[{"label": "Грн", "amount": 15000}])


@dp.callback_query_handler(text="submonth2")
async def submonth2(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title="Оформлення підписки",
                           description="Покупка програми тренувань",
                           payload="month_help", provider_token=LIQTOKEN, currency="UAH",
                           start_parameter="test_bot",
                           prices=[{"label": "Грн", "amount": 15000}])


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "month_sub":
        # Підписуєм користувача
        await bot.send_message(message.from_user.id, "👟Вам видана програма тренувань для схудення на місяць!👟",
                               reply_markup=nav.Pos_inline_markup, )
        sql = "INSERT INTO MaraphonMin (user_id, data_pay) VALUES (%s, %s)"
        val = (
            message.from_user.id, message.date)
        cursor.execute(sql, val)
        db.commit()

    elif message.successful_payment.invoice_payload == "month_help":
        await bot.send_message(message.from_user.id, "👟Вам видана програма тренувань для набору маси на місяць!👟",
                               reply_markup=nav.Gyp_inline_markup, )
        sql = "INSERT INTO MaraphonMax (user_id, data_pay) VALUES (%s, %s)"
        val = (
            message.from_user.id, message.date)
        cursor.execute(sql, val)
        db.commit()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
