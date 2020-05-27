import emoji
from emoji import emojize
#разделы
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

#клавиатура начала работы
btn_1 = InlineKeyboardButton('Эмоции', callback_data='1')
btn_2 = InlineKeyboardButton('Темы для разговора', callback_data='2')
inline_kb_start = InlineKeyboardMarkup().add(btn_1).add(btn_2)

#подразделы эмоций
btn_3 = InlineKeyboardButton('Описание', callback_data='3')
btn_4 = InlineKeyboardButton('Тренировка', callback_data='4')
btn_5 = InlineKeyboardButton('<< В начало', callback_data='5')
inline_kb_emotion = InlineKeyboardMarkup().add(btn_3).add(btn_4).add(btn_5)

#описание
btn_6 = InlineKeyboardButton(emojize("Радость :smile:", use_aliases=True), callback_data='6')
btn_7 = InlineKeyboardButton(emojize("Злость :rage:", use_aliases=True), callback_data='7')
btn_8 = InlineKeyboardButton(emojize("Страх :scream:", use_aliases=True), callback_data='8')
btn_9 = InlineKeyboardButton(emojize("Отвращение :nauseated_face:", use_aliases=True), callback_data='9')
btn_10 = InlineKeyboardButton(emojize("Грусть :disappointed:", use_aliases=True), callback_data='10')
btn_11 = InlineKeyboardButton(emojize("Спокойствие:relaxed:", use_aliases=True), callback_data='11')
inline_kb_des = InlineKeyboardMarkup().add(btn_6, btn_7, btn_8).add(btn_9, btn_10, btn_11).add(btn_5)

#тренировка
btn_12 = InlineKeyboardButton('Показать ответ', callback_data='12')
inline_kb_train = InlineKeyboardMarkup().add(btn_12).add(btn_5)

#описание
btn_13 = InlineKeyboardButton('<< Назад', callback_data='13')
inline_kb_des1 = InlineKeyboardMarkup().add(btn_13)

#кнопка вернуться назад
inline_kb_back = InlineKeyboardMarkup().add(btn_5)
