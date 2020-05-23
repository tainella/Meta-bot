import config
import kb
from time import sleep
import dbworker
import os
import requests
import urllib
from requests import get
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

BASE_MEDIA_PATH = './agg'

bot = Bot(token=config.token)
dp = Dispatcher(bot)

@dp.callback_query_handler(lambda callback_query: True)
async def send(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 1:
    	await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,text = "Эмоции", reply_markup = kb.inline_kb_emotion)
    elif code == 2:
    	await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,text = "Темы для разговора", reply_markup = kb.inline_kb_back)
    elif code == 3:
    	await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,text = "Описание", reply_markup = kb.inline_kb_des)
    elif code == 4:
    	await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    	ran = dbworker.random_mood('amusement')
    	await bot.send_message(chat_id=callback_query.message.chat.id, text = "На фотографии изображен либо человек, либо ситуация, описывающая эмоции. Давай попробуем определить, какие")
    	captio = 'Напиши свой вариант или сразу посмотри ответ'
    	await bot.send_photo(chat_id=callback_query.message.chat.id,photo = ran,caption= captio, reply_markup = kb.inline_kb_train)
    elif code == 5:
    	await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,text = "Привет :) я могу помочь тебе в общении с людьми. Разбираюсь в таких темах:", reply_markup = kb.inline_kb_start)
    elif code == 6:
    elif code == 7:
    elif code == 8:
    elif code == 9:
    elif code == 10:
    elif code == 11:
    elif code == 12:
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
	await bot.send_message(chat_id = message.chat.id,text = "Привет :) я могу помочь тебе в общении с людьми. Разбираюсь в таких темах:", reply_markup=kb.inline_kb_start)

@dp.message_handler(commands=["random"])
async def cmd_start(message: types.Message):
	ran = dbworker.random_mood('amusement')
	await bot.send_photo(message.chat.id, ran)

#парсер датасета в базу данных
@dp.message_handler(commands=["load"])
async def load(message: types.Message):
	#загрузка файлов на телеграм сервер -> добавление в базу данных
	for filename in os.listdir(BASE_MEDIA_PATH):
		if filename.find('.csv') > 0:
			f = open(os.path.join(BASE_MEDIA_PATH, filename), 'rb')
			print(f)
			i = 0
			while True:
				data = f.readline().decode("utf-8")
				if not data:
					break
				if i > 20:
					break
				if (int(data[-2]) >= 3): # берем из датасета самые точные картинки-описания
					emotion = data.split(',')[0]
					url = data.split(',')[1]
					if (get(url).status_code == 200):
						g1 = await bot.send_photo(message.chat.id, get(url).content)
						file_id = g1.photo[0].file_id
						dbworker.add_photo(emotion, file_id) #создать строку с новым файлом в базе данных
						i = i + 1
						sleep(2)
if __name__ == "__main__":
    executor.start_polling(dp)
