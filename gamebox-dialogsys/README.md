# gamebox bot

This project a combination of multiple modules to be able to play games with you.

## setup

- Install required python packages (might want to use a virtual environment) with `pip install -r requirements.txt`.
- Install espeak.
- Have an active internet connection for the google ASR.
- Train the rasa NLU model with `rasa train nlu`.
- Start program with `./main.py`. Make sure to have the rasa NLU (localhost) server running before starting the program by running `rasa run --enable-api -m models/MODEL_NAME_HERE.tar.gz` on a seperate terminal window.


## components

### text to speech - TTS

For TTS, [espeak](https://espeak.sourceforge.net/) is used.

### automatic speech recognition - ASR

For ASR, the google (cloud based) speech recogntion is used (embedded in the python library [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)).

### natural language understanding - NLU

For NLU, [rasa](https://rasa.com/) is used (only the NLU part, it could also be used for DM, but this is done seperately). The rasa model is trained for doing entity tagging as well as intent recogintion.

### dialog management - DM

For DM, a simple python loop and if/else statements are used.
