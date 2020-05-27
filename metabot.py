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
#from aiogram.utils.markdown import bold, code, italic, text
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

BASE_MEDIA_PATH = './agg'

bot = Bot(token=config.token)
dp = Dispatcher(bot)

@dp.callback_query_handler(lambda callback_query: True)
async def send(callback_query: types.CallbackQuery):
    code = callback_query.data
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
    	captio = '<b>Радость</b>\n<i>Аналоги</i>: Восторг, Ликование, Блаженство, Восхищение\n\nСчастливый человек улыбается. Это самый верный признак радости, удовлетворенности и всех сопряженных эмоций. В настоящей улыбке счастливого человека участвует все лицо: от бровей до подбородка. Этим она отличается от улыбки фальшивой: притворщик поднимает уголки губ, не задействуя щеки и мышцы вокруг глаз. \n\n<i>Выражение лица</i>: Губы растянуты за счет поднятия щек, в уголках глаз появляются морщинки, человек как будто немного жмурится от удовольствия.\n\n<i>Положение тела</i>: Люди двигаются легко и энергично, шагают широко и позволяют рукам раскачиваться.'
    	await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    	ran = dbworker.photo_des('happy1.png')
    	await bot.send_photo(chat_id=callback_query.message.chat.id,photo = ran,caption= captio,parse_mode=types.ParseMode.HTML, reply_markup = kb.inline_kb_des1)
    elif code == 7:
    	captio = '<b>Злость</b>\n<i>Аналоги</i>: Гнев, Раздражение, Ярость, Неистовство, Ненависть\n\n<i>Выражение лица</i>: брови нахмурены, глубокая складка на стыке бровей над переносицей;зубы стиснуты, скулы напряжены;рот закрыт, губы немного поджаты и сужены;глаза «страшные», т. е. открыты так широко, насколько позволяют опущенные брови;лицо немного наклонено вперед, взгляд исподлобья. \n\n<i>Положение тела</i>: Показывая пальцем на кого-то, человек демонстрирует агрессию; скрещенные руки на груди; сжатые в кулаки руки; корпус направлен вперед.'
    	ran = dbworker.photo_des('anger1.png')
    	await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    	await bot.send_photo(chat_id=callback_query.message.chat.id,photo = ran,caption= captio,parse_mode=types.ParseMode.HTML, reply_markup = kb.inline_kb_des1)
    elif code == 8:
    	captio = '<b>Страх</b>\n<i>Аналоги</i>: Беспокойство, Опасение, Настороженность, Тревожность, Испуг, Ужас\n\n<i>Выражение лица</i>: Брови подняты, сужены и вытянуты; морщинка над переносицей на стыке бровей; приподнятые верхние веки; рот приоткрыт, губы напряжены и слегка растянуты; глаза могут быть широко открыты. \n\n<i>Положение тела</i>: Движения того, кто испытывает страх, резкие и нерешительные. Он склонен поворачиваться боком к другим, пряча уязвимый торс, съеживаться, трястись.'
    	ran = dbworker.photo_des('fear1.png')
    	await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    	await bot.send_photo(chat_id=callback_query.message.chat.id,photo = ran,caption= captio,parse_mode=types.ParseMode.HTML, reply_markup = kb.inline_kb_des1)
    elif code == 9:
    	captio = '<b>Отвращение</b>\n<i>Аналоги</i>: Омерзение, Гадливость, Неприязнь\n\nВыражение отвращения называют «гримасой», т. к. в нем участвуют все лицевые мышцы, лицо человека резко преображается. Гримасу отвращения трудно с чем-то спутать, т. к. ни одна эмоция не вызывает столько мышечных сокращений сразу: под воздействием отвратительного зрелища лицо буквально сморщивается. \n\n<i>Выражение лица</i>: щеки подняты, переносица наморщена; глаза сильно сужены; рот приоткрыт, обнажены верхние зубы за счет приподнятой верхней губы. \n\n<i>Положение тела</i>: Сведенные вперед плечи, закрывающаяся поза, "защищающающаяся" от неприятного, корпус отодведён назад.'
    	ran = dbworker.photo_des('disgust1.png')
    	await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    	await bot.send_photo(chat_id=callback_query.message.chat.id,photo = ran,caption= captio,parse_mode=types.ParseMode.HTML, reply_markup = kb.inline_kb_des1)
    elif code == 10:
    	captio = '<b>Грусть</b>\n<i>Аналоги</i>: Грусть, Тоска, Ностальгия, Уныние, Безнадежность, Скорбь\n\nГрусть принято считать свойством взгляда, отсюда выражения вроде «грустные глаза», «тоска во взгляде» и т. п. На самом деле, единственная роль взгляда в грустном выражении лица – его отрешенность или направленность вниз в одну точку.\n\n<i>Выражение лица</i>: взгляд невидящий, рассеянный, направленный вовнутрь; глаза полуприкрыты; опущенные уголки губ в противоположность улыбке; рот закрыт, нижняя губа может быть немного выставлена вперед.\n\n<i>Положение тела</i>: Проявления грусти заметнее всего в верхней части торса — это слегка опущенные плечи и поникшая голова.'
    	ran = dbworker.photo_des('sadness1.png')
    	await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    	await bot.send_photo(chat_id=callback_query.message.chat.id,photo = ran,caption= captio,parse_mode=types.ParseMode.HTML, reply_markup = kb.inline_kb_des1)
    elif code == 11:
    	captio = '<b>Спокойствие</b>\n<i>Аналоги</i>: Умиротворение, Довольство, Удовлетворение\n\n<i>Выражение лица</i>: Лицо малоэмоционально, можно спутать с грустью, но взгляд подвижен, может быть лёгкая улыбка без зубов. \n\n<i>Положение тела</i>: Тело расслаблено, спина не напряжена, у большинства свои отличительные позы расслабленности.'
    	ran = dbworker.photo_des('contentment1.png')
    	await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    	await bot.send_photo(chat_id=callback_query.message.chat.id,photo = ran,caption= captio,parse_mode=types.ParseMode.HTML, reply_markup = kb.inline_kb_des1)
    elif code == 12:
    	await bot.send_message(chat_id=callback_query.message.chat.id, text = "Раздрел не доделан", reply_markup = kb.inline_kb_back)
    elif code == 13:
    	cha = callback_query.message.chat.id
    	await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    	await bot.send_message(chat_id=cha, text = "Описание", reply_markup = kb.inline_kb_des)
    	
    
    
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
	await bot.send_message(chat_id = message.chat.id,text = "Привет :) я могу помочь тебе в общении с людьми. Разбираюсь в таких темах:", reply_markup=kb.inline_kb_start)

@dp.message_handler(commands=["random"])
async def cmd_start(message: types.Message):
	ran = dbworker.random_mood('amusement')
	await bot.send_photo(message.chat.id, ran)

BASE2_MEDIA_PATH = './des'
@dp.message_handler(commands=["des"])
async def cmd_des(message: types.Message):
	for filename in os.listdir(BASE2_MEDIA_PATH):
		if filename.find('.png') > 0:
			f = open(os.path.join(BASE2_MEDIA_PATH, filename), 'rb')
			g1 = await bot.send_photo(message.chat.id, f)
			file_id = g1.photo[0].file_id
			dbworker.add_photo(filename, file_id) #создать строку с новым файлом в базе данных
			sleep(2)
	print(dbworker.random_mood('anger1'))

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
