import json
import requests
from TSB.local_settings import *

class MessengerApiHandler:
    def SendResponseMessage(self, recipient, message):
        payload = {'messaging_type': 'RESPONSE', 'recipient': {'id': str(recipient)}, 'message': {'text': str(message), 'quick_replies': [{'content_type': 'location'}]}}
        return requests.post("https://graph.facebook.com/v2.6/me/messages?access_token="+MESSENGER_API_KEY, json=payload)

    def SendAutoResponseMessage(self, recipient, message):
        message = message.replace("_", " ")
        messages = {
            "hi": "Hello.",
            "how are you": "I'm fine. Thank you.",
            "help": "If you want to update your location click the button below."
        }
        answer = ""
        if message in messages:
            answer = messages[message]
        else:
            answer = "I don't understand this message. Try HELP for more information."
        return self.SendResponseMessage(recipient, answer)
