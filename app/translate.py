import requests
import uuid

from flask import current_app
from flask_babel import _


def translate(text, source_language, dest_language):
    
    if "AZURE_TRANSLATOR_KEY" not in current_app.config or not current_app.config["AZURE_TRANSLATOR_KEY"]:
        return _("Error: the translation service is not configured.")
    
    subscription_key = current_app.config["AZURE_TRANSLATOR_KEY"]
    location = current_app.config["AZURE_TRANSLATOR_LOCATION"]
    endpoint = current_app.config["TRANSLATION_ENDPOINT"]

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': [dest_language]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated_text = response[0]['translations'][0]['text']
    return translated_text
