import json
import requests
from flask_babel import _
from flask import current_app
import os, uuid

# this is an old version that doesn't work now
def translate(text, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')

    # Don't forget to replace with your Cog Services subscription key!
    # If you prefer to use environment variables, see Extra Credit for more info.
    subscription_key = current_app.config['MS_TRANSLATOR_KEY']
    subscription_region = current_app.config['MS_TRANSLATOR_REGION']

    auth = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region':subscription_region,
    }
    response = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
                     '/Translate?text={}&to={}'.format(
                         text, dest_language),
                     headers=auth)

    # response = requests.get('https://api.cognitive.microsofttranslator.com/v2/Ajax.svc'
    #                  '/Translate?text={}&from={}&to={}'.format(
    #                      text, source_language, dest_language),
    #                  headers=auth)

    if response.status_code != 200:
        return _('Error: the translation service failed.')

    return json.loads(response.content.decode('utf-8-sig'))


# Our Flask route will supply two arguments: text_input and language_output.
# When the translate text button is pressed in our Flask app, the Ajax request
# will grab these values from our web app, and use them in the request.
# See main.js for Ajax calls.
def new_translate(text_input, language_output):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')

    # Don't forget to replace with your Cog Services subscription key!
    # If you prefer to use environment variables, see Extra Credit for more info.
    subscription_key = current_app.config['MS_TRANSLATOR_KEY']
    subscription_region = current_app.config['MS_TRANSLATOR_REGION']

    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=' + language_output
    constructed_url = base_url + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region':subscription_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text' : text_input
    }]
    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()
