#!/usr/bin/env python3

import os
import subprocess


def tts(text):
    """Text to speech function using espeak"""

    command = f'espeak -v de -s 150 "{text}" --stdout | aplay'
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()





