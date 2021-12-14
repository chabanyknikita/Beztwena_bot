from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# --- Main menu ---


btnInfo = KeyboardButton('Індивідуальна программа для схудення')
btnMore = KeyboardButton('Індивідуальна программа для набору маси')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnInfo)
mainMenu.add(btnMore)

# --- Схудення Inline Buttons ---

info_inline_markup = InlineKeyboardMarkup(row_width=1)

btnInfoRev = InlineKeyboardButton(text="Місяць - 150 гривень", callback_data="submonth")

info_inline_markup.insert(btnInfoRev)

# --- Pay Схудення Inline Buttons ---

Pos_inline_markup = InlineKeyboardMarkup(row_width=1)

btnPosRev = InlineKeyboardButton(text="Посилання на канал", url="https://t.me/+5tw1qEGwZMgyYjI6")

Pos_inline_markup.insert(btnPosRev)


# --- Набір Inline Buttons ---
More_inline_markup = InlineKeyboardMarkup(row_width=1)

btnMoreRev = InlineKeyboardButton(text="Місяць - 150 гривень", callback_data="submonth2")

More_inline_markup.insert(btnMoreRev)

# --- Pay Набір Маси Inline Buttons ---

Gyp_inline_markup = InlineKeyboardMarkup(row_width=1)

btnGypRev = InlineKeyboardButton(text="Посилання на канал", url="https://t.me/+jrdSGEtEjLQ1MTEy")

Gyp_inline_markup.insert(btnGypRev)

