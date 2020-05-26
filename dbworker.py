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
class Train(Base):
    __tablename__ = 'Train'
    file_id = Column(String(255)) #файловое айди
    chat_id = Column(String(255))
    dop = Column(Integer, primary_key=True)
    date_in = Column(DateTime) #первое время ознакомления
    last_in = Column(DateTime) #последнее время использования
    step = Column(Integer) #интервал повторения - "шаг выучивания"
    an = Column(Boolean()) #"правильный/неправильный" последний ответ

#шаги выучивания:
#1 - 1 час; 2 - 24 часа; 3 - 48 часов; 4 - 72 часа
#если хоть раз ответил на картинку неправильно, картинка добавляется в список повторения, 
#выходит из него только при финальном правильном ответе через 72 часа
	
#изменить последнюю работу с файл-юзер (или добавить новую)
def change_one(chat, file, ann):
	session = Session()
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

#достать картинку для повторения по:
# 1 приоритет: максимальная длина интервала (почти доученные фото)
# 2 приоритет: дата первого ознакомления
def repeat(chat):
	session = Session()
	vr = session.query(Train).filter(chat_id = chat, func.max(step), (last_in < (datetime.datetime.now() - timedelta(minutes=55)))).one()
	if vr.step < 48:
		h = session.query(Train).filter(chat_id = chat, step = vr.step, func.min(date_in)).one()
	else:
		h = vr
	return h.file_id

#достать новую картинку для изучения - def random_mood(mood) (описана выше)

	
#БАЗА ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ
class Us(Base):
    __tablename__ = 'Us'
    id = Column(Integer, primary_key=True)
    state = Column(Integer) #раздел где сейчас находится
    dop1 = Column(String(255))
    dop2 = Column(String(255))

#Добавлям пользователя в базу данных
def add_user(user_id):
	session = Session()
	if (None == session.query(Us).filter_by(id=user_id).scalar()):
		newitem = Us(id = user_id, state = int(config.States.S_START), dop1 = "_", dop2 = "_",)
		session.add(newitem)
		session.commit()
	session.close()

#Меняем состояние пользователя
def change_user(user_id, stat, do1, do2):
	session = Session()
	if (None != session.query(Us).filter_by(id=user_id).scalar()):
		newitem = Us(id = user_id, state = stat, dop1 = do1, dop2 = do2,)
		session.add(newitem)
		session.commit()
	session.close()

#Удалить пользователя
def delete_user(user_id):
	session = Session()
	if (None != session.query(Us).filter_by(id=user_id).scalar()):
		ditem = session.query(Us).filter_by(id=user_id).one()
		session.delete(ditem)
		session.commit()
	else:
		print("Нет такого пользователя\n")
	session.close()

#удаляем базу данных
def delete_table():
	Base.metadata.drop_all(engine)
	
