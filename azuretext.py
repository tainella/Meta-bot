import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import config

def authenticateClient():
    credentials = CognitiveServicesCredentials(config.key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=config.endpoint, credentials=credentials)
    return text_analytics_client

client = authenticateClient()
country_hint : "ru"

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
