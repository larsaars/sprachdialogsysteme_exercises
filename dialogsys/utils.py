#!/usr/bin/env python3

"""
tts utils file
"""

import os
import subprocess
import speech_recognition as sr

# in print mode stdin/stdout is used instead of asr/tts
print_mode = False

def tts(text, language='en'):
    """Text to speech function using espeak"""

    if not text:
        return


    if print_mode:
        print(text)
        return

    # use espeak to convert text to speech
    command = f'espeak -v {language} -s 150 "{text}" --stdout | aplay'
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()


def asr() -> str:
    """perform automatic speech recognition using google speech recognition"""

    if print_mode:
        return input('>> ')

    # speech recognition using google speech recognition
    # could also easily use bing, sphinx, etc. using this lib
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something')
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except Exception as e:
        return None


