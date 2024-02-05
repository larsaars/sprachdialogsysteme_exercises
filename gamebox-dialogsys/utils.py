#!/usr/bin/env python3

"""
utils needed by the dialog manager
"""

import os
import subprocess
import speech_recognition as sr
import requests
import json

# in print mode stdin/stdout is used instead of asr/tts
print_mode = False

def set_print_mode(mode: bool):
    global print_mode
    print_mode = mode

def get_print_mode() -> bool:
    return print_mode

def tts(text, language='en'):
    """Text to speech function using espeak"""

    if not text:
        return

    global print_mode

    # print anyways what is being said
    print('<< ' + text)

    # if in print mode, return to not speak out loud
    if print_mode:
        return

    # use espeak to convert text to speech
    command = f'espeak -v {language} -s 150 "{text}" --stdout | aplay'
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()


def asr() -> str:
    """perform automatic speech recognition using google speech recognition"""

    global print_mode

    if print_mode:
        return input('>> ')

    # speech recognition using google speech recognition
    # could also easily use bing, sphinx, etc. using this lib
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        rec = recognizer.recognize_google(audio)
        # print what has been recognized
        print('>> ' + rec)
        return rec
    except Exception as e:
        return None


def rasa_parse(text):
    """
    input text into the rasa NLU model
    
    :param text: input text
    :return: most probable intent, entity (is type None if there is none)
    """

    # if the text is empty, return None
    if not text:
        return None, None

    url = 'http://localhost:5005/model/parse'
    data = {'text': text}

    # Set the headers for the request
    headers = {'Content-Type': 'application/json'}

    # Make the POST request
    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Check the response
    if response.status_code == 200:
        # Parse the JSON response
        parsed_data = response.json()

        # get the most probable intent from data
        intent = parsed_data['intent']['name']
        entity = None

        # and the entity if there is one 
        if len(parsed_data['entities']) > 0:
            entity = parsed_data['entities'][0]['value']

        return intent, entity 
    else:
        # If the response code is not 200, print an error message
        tts('Rasa NLU server error')
        return None, None
