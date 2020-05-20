import config
import telebot
import apiai, json

bot = telebot.TeleBot(config.token)

#@bot.message_handler(content_types=["text"])
#def repeat_all_messages(message): 

@bot.message_handler(content_types=["text"])
def textMessage(message):
    request = apiai.ApiAI(config.goodmood).text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'melya_meta_bot' # ID Сессии диалога 
    request.query = message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(message.chat.id, text=response)
    else:
        bot.send_message(message.chat.id, text='Я не понимаю, что ты говоришь...')
    
if __name__ == '__main__':
     bot.infinity_polling()