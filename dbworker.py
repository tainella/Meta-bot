import config
#from sqlalchemy.types import text
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine # для настроек
from sqlalchemy.orm import relationship 
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import Engine

#создаем базу данных
Base = declarative_base()
class Client(Base):
	__tablename__ = 'Client'
	id = Column(Integer, primary_key= True)
	name = Column(String(255))
	age = Column(Integer)
	state = Column(Integer)
	mood = Column(Integer)
engine = create_engine('sqlite:///Client.db')
Base.metadata.bind = engine 
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
Base.metadata.create_all(engine)	

#удаляем базу данных
def delete_table():
	Base.metadata.drop_all(engine)

# Пытаемся узнать из базы «состояние» пользователя
def get_state(user_id):
	session = Session()
	if (None != session.query(Client).filter_by(id=user_id).scalar()):
		newitem = session.query(Client).filter_by(id=user_id).one()
		ag = newitem.state
	else:
		ag=-1
		print("Нет такого пользователя\n")
	session.close()
	return ag

# Пытаемся узнать из базы настроение бота
def get_mood(user_id):
	session = Session()
	if (None != session.query(Client).filter_by(id=user_id).scalar()):
		newitem = session.query(Client).filter_by(id=user_id).one()
		ag = newitem.mood
	else:
		ag=-1
		print("Нет такого пользователя\n")
	session.close()
	return ag

# Пытаемся узнать из базы имя пользователя
def get_name(user_id):
	session = Session()
	if (None != session.query(Client).filter_by(id=user_id).scalar()):
		newitem = session.query(Client).filter_by(id=user_id).one()
		ag = newitem.name
	else:
		ag = " "
		print("Нет такого пользователя\n")
	session.close()
	return ag

# Пытаемся узнать из базы возраст пользователя
def get_age(user_id):
	session = Session()
	if (None != session.query(Client).filter_by(id=user_id).scalar()):
		newitem = session.query(Client).filter_by(id=user_id).one()
		ag = newitem.age
	else:
		ag = -1
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

# Изменяем имя пользователя
def set_name(user_id, nam):
	session = Session()
	if (None != session.query(Client).filter_by(id=user_id).scalar()):
		newitem = session.query(Client).filter_by(id=user_id).one()
		newitem.name = nam
		session.add(newitem)
		session.commit()
	else:
		print("Нет такого пользователя\n")
	session.close()

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, stat):
	session = Session()
	if (None != session.query(Client).filter_by(id=user_id).scalar()):
		newitem = session.query(Client).filter_by(id=user_id).one()
		newitem.state = stat
		session.add(newitem)
		session.commit()
	else:
		print("Нет такого пользователя\n")
	session.close()

# Меняем настроение бота
def set_mood(user_id, mod):
	session = Session()
	if (None != session.query(Client).filter_by(id=user_id).scalar()):
		newitem = session.query(Client).filter_by(id=user_id).one()
		newitem.mood = mod
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