import config
import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine # для настроек
from sqlalchemy.orm import relationship 
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import Engine
import random

BASE_MEDIA_PATH = './agg'

#создаем базу данных фото эмоций
Base = declarative_base()
class Media(Base):
    __tablename__ = 'Media'
    file_id = Column(String(255), primary_key=True)
    emotion = Column(String(255))
engine = create_engine('sqlite:///Media.db')
Base.metadata.bind = engine 
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
Base.metadata.create_all(engine)	

#список эмоций:
#amusement - восторг, веселье, беззаботность, удовольствие, радость, волнение, азарт, возбуждение
#excitement - радость, волнение, азарт, возбуждение, восторг, веселье, беззаботность, удовольствие
#anger - злость, ярость, раздражение, недовольство, гнев
#awe - трепет, волнение, удивление, паника, ужас, страх, ступор, боязнь, испуг, обеспокоенность
#fear - паника, ужас, страх, ступор, боязнь, испуг, обеспокоенность, трепет, волнение, удивление 
#contentment - довольство, удовлетворенность, спокойствие, умиротворение, комфорт, нега, сытость
#disgust - отвращение, презрение, брезгливость, нелюбовь, ненависть, неприязнь, нерасположение, омерзение, антипатия
#sadness - грусть, печаль, скорбь, грусть, уныние, отчаяние, тоска, жалость

#создаем базу данных развития пользователя
Base1 = declarative_base()
class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    #
engine1 = create_engine('sqlite:///Users.db')
Base1.metadata.bind = engine1
session_factory1 = sessionmaker(bind=engine1)
Session1 = scoped_session(session_factory1)
Base1.metadata.create_all(engine1)	

#удаляем базу данных
def delete_table():
	Base.metadata.drop_all(engine)

#создать строку с новым файлом в таблице
def add_photo(emotio, file_i):
	session = Session()
	if (None == session.query(Media).filter_by(file_id=file_i).scalar()):
		newitem = Media(file_id = file_i, emotion = emotio)
		session.add(newitem)
		session.commit()
	session.close()
	
#выбор картинки по текущей работе пользователя

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

#Добавлям пользователя в базу данных
def add_user(user_id):
	session = Session()
	if (None == session.query(Client).filter_by(id=user_id).scalar()):
		newitem = Client(id = user_id, name = " ", age = -1, state = int(config.States.S_START), mood = int(config.Moods.M_START))
		session.add(newitem)
		session.commit()
	session.close()

#Изменяем текущий прогресс пользователя

# Изменяем имя пользователя
def set_age(user_id, ag):
	session = Session()
	if (None != session.query(Client).filter_by(id=user_id).scalar()):
		newitem = session.query(Client).filter_by(id=user_id).one()
		newitem.age = ag
		session.add(newitem)
		session.commit()
	else:
		print("Нет такого пользователя\n")
	session.close()

#Удалить пользователя
def delete_user(user_id):
	session = Session()
	if (None != session.query(Client).filter_by(id=user_id).scalar()):
		ditem = session.query(Client).filter_by(id=user_id).one()
		session.delete(ditem)
		session.commit()
	else:
		print("Нет такого пользователя\n")
	session.close()
