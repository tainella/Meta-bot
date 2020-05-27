#база данных Media для file_id фото на сервере телеграма, загруженных из https://www.cs.rochester.edu/u/qyou/deepemotion/
import config
import os
import datetime
from datetime import timedelta
from sqlalchemy import Column, Integer, String, DateTime, Boolean, and_
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine # для настроек
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import Engine
import random

#список эмоций:
#amusement - восторг, веселье, беззаботность, удовольствие, радость, волнение, азарт, возбуждение
#excitement - радость, волнение, азарт, возбуждение, восторг, веселье, беззаботность, удовольствие
#anger - злость, ярость, раздражение, недовольство, гнев
#awe - трепет, волнение, удивление, паника, ужас, страх, ступор, боязнь, испуг, обеспокоенность
#fear - паника, ужас, страх, ступор, боязнь, испуг, обеспокоенность, трепет, волнение, удивление 
#contentment - довольство, удовлетворенность, спокойствие, умиротворение, комфорт, нега, сытость
#disgust - отвращение, презрение, брезгливость, нелюбовь, ненависть, неприязнь, нерасположение, омерзение, антипатия
#sadness - грусть, печаль, скорбь, уныние, отчаяние, тоска, жалость

Base = declarative_base()
engine = create_engine('sqlite:///Media.db')
Base.metadata.bind = engine 
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
Base.metadata.create_all(engine)	

#ТАБЛИЦЫ ПРМВЯЗКИ ФАЙЛ-АЙДИ ЭМОЦИЯ (для разделов Описание и Эмоция)
class Media(Base):
    __tablename__ = 'Media'
    file_id = Column(String(255), primary_key=True)
    emotion = Column(String(255))

#создать строку с новым файлом в таблице
def add_photo(emotio, file_i):
	session = Session()
	if (None == session.query(Media).filter_by(file_id=file_i).scalar()):
		newitem = Media(file_id = file_i, emotion = emotio)
		session.add(newitem)
		session.commit()
	session.close()
#выдать рандомную картинку заданного настроения
def random_mood(mood):
	session = Session()
	while True:  
		rand = random.randrange(0, session.query(Media).count()) 
		row = session.query(Media)[rand] 
		if row.emotion==mood:
			break
	ag = row.file_id
	session.close()
	return ag

#выдать картинку-описание заданного настроения
def photo_des(moo):
	session = Session()
	row = session.query(Media).filter_by(emotion = moo).first()
	ag = row.file_id
	session.close()
	return ag


#ТАБЛИЦА РАБОТЫ КАЖДОГО ПОЛЬЗОВАТЕЛЯ С РАЗДЕЛОМ ТРЕНИРОВКИ
#на каждое не усвоенное фото пользователем фото строка с уточнением пользователя,
#первым временем ознакомления, последним использованием, "правильный/неправильный" последний ответ
count = 0 #индивидуальный ключ для добавления в dop
Base1 = declarative_base()
engine1 = create_engine('sqlite:///Train.db')
Base1.metadata.bind = engine1 
session_factory1 = sessionmaker(bind=engine1)
Session1 = scoped_session(session_factory1)
Base1.metadata.create_all(engine1)

class Train(Base1):
    __tablename__ = 'Train'
    file_id = Column(String(255)) #файловое айди
    chat_id = Column(String(255))
    dop = Column(Integer, primary_key=True)
    date_in = Column(DateTime) #первое время ознакомления
    last_in = Column(DateTime) #последнее время использования
    step = Column(Integer) #интервал повторения - "шаг выучивания"
    an = Column(Boolean) #"правильный/неправильный" последний ответ

#шаги выучивания:
#1 - 1 час; 2 - 24 часа; 3 - 48 часов; 4 - 72 часа
#если хоть раз ответил на картинку неправильно, картинка добавляется в список повторения, 
#выходит из него только при финальном правильном ответе через 72 часа
	
#изменить последнюю работу с файл-юзер (или добавить новую)
def change_one(chat, file, ann):
	session = Session1()
	if (None == session.query(Train).filter(and_(file_id=file, chat_id = chat))):
		count += 1
		newitem = Train(file_id = file, chat_id = chat, dop = count, date_in = datetime.datetime.now(), last_in = datetime.datetime.now(), an = ann)
		session.add(newitem)
	else:
		vr = session.query(Train).filter(and_(file_id=file, chat_id = chat)).one()
		if ann == True: #увеличение интервала повторения
			if vr.step == 4:
				session.delete(vr)
			else:
				vr.step += 1
		else: #уменьшение интервала повторения
			vr.step = 1
		vr.last_in = datetime.datetime.now()
		vr.an = ann
	session.commit()
	session.close()
	session = Session()
	vr = session.query(Train).filter(and_(file_id=file, chat_id = chat)).one()
	print(vr)
	session.close()

def vr(time):
	if time <= datetime.datetime.now() - timedelta(minutes=55):
		return True
	else:
		return False
#достать картинку для повторения по:
# 1 приоритет: максимальная длина интервала (почти доученные фото)
# 2 приоритет: дата первого ознакомления
def repeat(chat):
	session = Session1()
	if (None != session.query(Train).filter(chat_id = chat, step = func.max(step)).filter(vr,last_in).scalar):
		vr = session.query(Train).filter(chat_id = chat, step = func.max(step)).filter(vr,last_in).one()
		if vr.step < 48:
			h = session.query(Train).filter(chat_id = chat, step = vr.step, date_in = func.min(date_in)).one()
		else:
			h = vr
		return h.file_id
	else:
		return None

#достать новую картинку для изучения - def random_mood(mood) (описана выше)

#проверка пришел ли пользователь СЕЙЧАС на повторную тренировку (хранится в таблице Us1)
def was1(chat):
	session = Session2()
	vr = session.query(Us1).filter_by(chat_id = chat).one()
	if vr.last_in <= (datetime.datetime.now() - timedelta(minutes=55)):
		was(chat)
		return True
	else:
		return False
	session.close()

#добавить последнюю картинку в тренировке
def set_send_f(chat, ph):
	session = Session2()
	vr = session.query(Us1).filter_by(chat_id = chat).one()
	vr.dop1 = ph
	session.commit()
	session.close()

#file_id текущей картинки
def get__cur_file(chat):
	session = Session2()
	vr = session.query(Us1).filter_by(chat_id = chat).one()
	file = vr.dop1
	session.close()
	return file
	
#ответ на текущую картинку
def get_answ(chat):
	session = Session2()
	vr = session.query(Us1).filter_by(chat_id = chat).one()
	file = vr.dop1
	vr = session.query(Media).filter_by(file_id = file).one()
	session.close()
	return vr.emotion

def set_h(chat):
	session = Session2()
	vr = session.query(Us1).filter_by(chat_id = chat).one()
	vr.dop2 += 1
	session.commit()
	session.close()
	
#проверка сколько прошло картинок на одной тренировке
def get_h(chat):
	session = Session2()
	vr = session.query(Us1).filter_by(chat_id = chat).one()
	session.close()
	return vr.dop2

def get_state(chat):
	session = Session2()
	vr = session.query(Us1).filter_by(chat_id = chat).one()
	session.close()
	return vr.state
	
#изменить состояние пользователя
def set_state(chat, stat, do1, do2):
	session = Session2()
	vr = session.query(Us1).filter_by(chat_id = chat).one()
	vr.state = stat
	vr.dop1 = do1
	vr.dop2 = do2
	session.commit()
	session.close()

#пользователь пришел на повторную тренировку (записывается в таблицу Us)
def was(chat):
	session = Session2()
	vr = session.query(Us1).filter_by(chat_id = chat).one()
	vr.was = True
	session.commit()
	session.close()

#найти пользователей, которым сейчас надо отправить оповещение о том, что нужно пройти тренировку
def find_for():
	session = Session1()
	list = session.query(Train).filter_by(last_in = (datetime.datetime.now() - timedelta(hours=24))).all()
	list1 = session.query(Train).filter_by(last_in = (datetime.datetime.now() - timedelta(hours=1))).all()
	session.close()
	return list + list1
	
#БАЗА ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ
Base2 = declarative_base()
engine2 = create_engine('sqlite:///Us1.db')
Base2.metadata.bind = engine2
session_factory2 = sessionmaker(bind=engine2)
Session2 = scoped_session(session_factory2)
Base2.metadata.create_all(engine2)

class Us1(Base):
    __tablename__ = 'Us1'
    chat_id = Column(String(255), primary_key=True)
    state = Column(Integer) #раздел где сейчас находится
    was = Column(Boolean) #true был на 2 тренировке в день, false не был на 2 тренировке
    dop1 = Column(String(255))
    dop2 = Column(Integer)
    notif = Column(Boolean) #включенные/выключенные оповещения

def get_notif(chat):
	session = Session2()
	newitem = session.query(Us1).filter_by(chat_id = chat).one()
	session.close()
	return newitem.notif

def set_notif(chat, noti):
	session = Session2()
	newitem = session.query(Us1).filter_by(chat_id = chat).one()
	newitem.notif = noti
	session.commit()
	session.close()

#Добавлям пользователя в базу данных
def add_user(chat):
	session = Session2()
	if (None == session.query(Us1).filter_by(chat_id = chat).scalar()):
		newitem = Us1(chat_id = chat, state = int(config.States.S_START), was = False, dop1 = "_", dop2 = 0,notif = True)
		session.add(newitem)
		session.commit()
	session.close()

#Меняем состояние пользователя
def change_user(chat, stat, do1, do2):
	session = Session2()
	if (None != session.query(Us1).filter_by(chat_id = chat).scalar()):
		newitem = Us1(chat_id = chat, state = stat, dop1 = do1, dop2 = do2,notif = True)
		session.add(newitem)
		session.commit()
	session.close()

#Удалить пользователя
def delete_user(chat):
	session = Session2()
	if (None != session.query(Us1).filter_by(chat_id = chat).scalar()):
		ditem = session.query(Us1).filter_by(chat_id = chat).one()
		session.delete(ditem)
		session.commit()
	else:
		print("Нет такого пользователя\n")
	session.close()

#удаляем базу данных
def delete_table1():
	Base.metadata.drop_all(engine1)
	
