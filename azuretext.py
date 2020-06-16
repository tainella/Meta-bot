import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import config
import random
import pymorphy2
morph = pymorphy2.MorphAnalyzer() #работа с формами слов

def authenticateClient():
    credentials = CognitiveServicesCredentials(config.key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=config.endpoint, credentials=credentials)
    return text_analytics_client

client = authenticateClient()
country_hint : "ru"

#получить от сервиса значение по шкале эмоций
def sentiment(text):
    client = authenticateClient()
    try:
        documents = [
            {"id": "1", "language": "ru", "text": text}
        ]
        response = client.sentiment(documents=documents)
        for document in response.documents:
            #print("Document Id: ", document.id, ", Sentiment Score: ",
            #      "{:.2f}".format(document.score))
            score =  "{:.2f}".format(document.score)
            return float(score)
    except Exception as err:
        print("Encountered exception. {}".format(err))
        return None

#формулировка от сервиса: "чем ближе значение к нулю, тем более негативное, чем больше к единице - более положительное"
#будем считать, что если значение от 0 до 0.25 негативные эмоции
#от 0.25 до 0.5 нейтральные
#от 0.5 до 1 положительные


def key_phrases(text):
	client = authenticateClient()
	try:
		documents = [
			{"id": "1", "language": "ru", "text": text}
		]
		response = client.key_phrases(documents=documents)
		for document in response.documents:
			answ = document
		return answ.key_phrases
	except Exception as err:
		print("Encountered exception. {}".format(err))

#поиск слов-ассоциаций
def assos(words):
	filename = './assoc.safe.csv' #https://github.com/dkulagin/kartaslov
	wordsss = []
	for ph in words:
		wordsss.append(morph.parse(ph)[0].normal_form)
	f = open(filename, 'rb')
	answ = []
	while True:
		data = f.readline().decode("utf-8").lower()
		if not data:
			break
		else:
			w = data.split(';')[0]
			a = data.split(';')[1]
			for i in wordsss:
				if w == i.lower():
					if a in answ:
						pass
					else:
						answ.append(a)
					wordsss.remove(i)
	return answ

f = ['Спроси, например, про: ', 'Здесь подходящий вариант для продолжения разговора: ', 'Здесь было бы интересно поговорить про: ', 'Попробуй завести разговор про: ','К тематике этого разговора близки: ']
#формулирование ответа бота - предложения тем
def suggest(words):
	answ = assos(key_phrases(words))
	if answ != []:
		return random.choice(f) + ', '.join(answ)
	else:
		return 'Совсем не знаю, что придумать'

#answ = key_phrases("Шел троллейбус. Увидел его Собянин. И решил, что его надо убрать.")
#suggest(answ)

