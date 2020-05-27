import config
import kb
from time import sleep
import dbworker
import os
import requests
import random
import urllib
import time
import datetime
import multiprocessing
from multiprocessing import Process
#import schedule
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


def start_process():#Запуск Process
	list = dbworker.find_for()
	if list != None:
		p1 = Process(target=m_send(list), args=(list))
		p1.start()
	else:
		pass

async def m_send(list):
	for i in list:
		await bot.send_message(chat_id=i.chat_id, text = "Время повторить тренировку в распознавании эмоций! Приходи, чтобы сохранить текущий прогресс")

list_em = ['amusement', 'excitement', 'anger', 'awe', 'fear', 'contentment', 'disgust', 'sadness']
list_1m = ['восторг', 'веселье', 'беззаботность', 'удовольствие', 'радость', 'волнение', 'азарт', 'возбуждение'] #синонимы к 'amusement', 'excitement'
list_2m = ['злость', 'ярость', 'раздражение', 'недовольство', 'гнев'] #синонимы к 'anger'
list_3m = ['паника', 'ужас', 'страх', 'ступор', 'боязнь', 'испуг', 'обеспокоенность', 'трепет', 'волнение', 'удивление'] #синонимы к 'awe', 'fear'
list_4m = ['довольство', 'удовлетворенность', 'спокойствие', 'умиротворение', 'комфорт', 'нега', 'сытость'] #синонимы к contentment
list_5m = ['отвращение', 'презрение', 'брезгливость', 'нелюбовь', 'ненависть', 'неприязнь', 'нерасположение', 'омерзение', 'антипатия'] #синонимы к 'disgust'
list_6m = ['грусть', 'печаль', 'скорбь', 'уныние', 'отчаяние', 'тоска', 'жалость'] #синонимы к sadness
list_0m = list_1m + list_2m + list_3m + list_4m + list_5m + list_6m


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
    	dbworker.set_state(callback_query.message.chat.id, int(config.States.S_TRAIN), "_", 0)
    	chat = callback_query.message.chat.id
    	if dbworker.was1(callback_query.message.chat.id) == True:
    		dbworker.was(callback_query.message.chat.id)
    	await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    	await bot.send_message(chat_id=callback_query.message.chat.id, text = "На фотографии изображен либо человек, либо ситуация, описывающая эмоции. Давай попробуем определить, какие")
    	await in_training(chat)
    elif code == 5:
    	if dbworker.get_state(callback_query.message.chat.id) == int(config.States.S_TRAIN):
    		await bot.send_message(chat_id = callback_query.message.chat.id,text = "Привет :) я могу помочь тебе в общении с людьми. Разбираюсь в таких темах:", reply_markup=kb.inline_kb_start)
    	else:
    		await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,text = "Привет :) я могу помочь тебе в общении с людьми. Разбираюсь в таких темах:", reply_markup = kb.inline_kb_start)
    	dbworker.set_state(callback_query.message.chat.id, int(config.States.S_START), "_", 0)
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
    	t = dbworker.get_answ(callback_query.message.chat.id)
    	tex =  await true_answ(t)
    	await bot.send_message(chat_id=callback_query.message.chat.id, text = tex)
    	await in_training(callback_query.message.chat.id)
    elif code == 13:
    	cha = callback_query.message.chat.id
    	await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    	await bot.send_message(chat_id=cha, text = "Описание", reply_markup = kb.inline_kb_des)

#продолжение тренировки    	
async def in_training(chat_i):
	ph = None
	if dbworker.get_h(chat_i) <= 15:
		if dbworker.was1(chat_i) == True:
			i = h_t(chat_i)
			ph = dbworker.repeat(chat_i)
			if ph == None:
				ph = dbworker.random_mood(random.choice(list_em))
			else:
				ph = dbworker.random_mood(random.choice(list_em))
	if ph == None:
		ph = dbworker.random_mood(random.choice(list_em))
	captio = 'Напиши свой вариант или сразу посмотри ответ'
	await bot.send_photo(chat_id=chat_i,photo = ph,caption= captio, reply_markup = kb.inline_kb_train)
	dbworker.set_h(chat_i) # +1 картинка пройдена
	dbworker.set_send_f(chat_i, ph)

#ВРЕМЯ!

async def true_answ(t):
	if t == "amusement":
		tex = "Ответ: радость"
	elif t == "excitement":
		tex = "Ответ: радость"
	elif t == "anger":
		tex = "Ответ: злость"
	elif t == "awe":
		tex = "Ответ: волнение"
	elif t == "fear":
		tex = "Ответ: страх"
	elif t == "contentment":
		tex = "Ответ: спокойствие"
	elif t == "disgust":
		tex = "Ответ: отвращение"
	elif t == "sadness":
		tex = "Ответ: грусть"
	return tex

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
	await bot.send_message(chat_id = message.chat.id,text = "Привет :) я могу помочь тебе в общении с людьми. Разбираюсь в таких темах:", reply_markup=kb.inline_kb_start)
	dbworker.add_user(message.chat.id)

#ответ в тренировке
@dp.message_handler()
async def what_answ(msg: types.Message):
	if dbworker.get_state(msg.chat.id) == int(config.States.S_TRAIN):
		if msg.text in list_0m:
			t = dbworker.get_answ(msg.chat.id)
			if t == "amusement":
				ino = list_1m
			elif t == "excitement":
				ino = list_1m
			elif t == "anger":
				ino = list_2m
			elif t == "awe":
				ino = list_3m
			elif t == "fear":
				ino = list_3m
			elif t == "contentment":
				ino = list_4m
			elif t == "disgust":
				ino = list_5m
			elif t == "sadness":
				ino = list_6m
			if msg.text in ino:
				await bot.send_message(chat_id = msg.chat.id, text = "Правильный ответ!")
				ann = True
			else:
				ann = False
				answ = await true_answ(t)
				y = "Неправильно."
				file = dbworker.get_cur_file(msg.chat.id)
				#dbworker.change_one(msg.chat.id, file, ann)
				te = y + answ
				await bot.send_message(chat_id = msg.chat.id, text = te)
		else:
			file = get__cur_file(msg.chat.id)
			change_one(msg.chat.id, file, ann)
		await in_training(msg.chat.id)
	else:
		pass

@dp.message_handler(commands=["notification"])
async def change_notif(message: types.Message):
	if dbworker.get_notif(message.chat.id) == True:
		dbworker.set_notif(message.chat.id, False)
		await bot.send_message(chat_id = message.chat.id,text = "Вы выключили оповещения (-)")
	else:
		dbworker.set_notif(message.chat.id, True)
		await bot.send_message(chat_id = message.chat.id,text = "Вы включили оповещения (+)")

@dp.message_handler(commands=["random"])
async def cmd_random(message: types.Message):
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
	start_process()
	executor.start_polling(dp)
