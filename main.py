import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import markups as nav

TOKEN = "2141163298:AAGz-iSZR9LcBOewuySWAscDHsm4XBxGq3U"
LIQTOKEN = "632593626:TEST:sandbox_i29067075948"

logging.basicConfig(level=logging.INFO)

# Initializate bot
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Добрий день', reply_markup=nav.mainMenu)


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
                                   reply_markup=nav.info_inline_markup)

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
                           payload="month_help", provider_token=LIQTOKEN, currency="UAH", start_parameter="test_bot",
                           prices=[{"label": "Грн", "amount": 15000}])




@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "month_sub":
        # Підписуєм користувача
        await bot.send_message(message.from_user.id, "👟Вам видана програма тренувань для схудення на місяць!👟",
                                    reply_markup=nav.Pos_inline_markup,)
    elif message.successful_payment.invoice_payload == "month_help":
        await bot.send_message(message.from_user.id, "👟Вам видана програма тренувань для набору маси на місяць!👟",
                               reply_markup=nav.Gyp_inline_markup,)




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
