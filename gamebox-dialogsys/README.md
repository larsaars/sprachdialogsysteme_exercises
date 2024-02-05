# gamebox bot

Play word-based games!

## setup

- Install required python packages (might want to use a virtual environment) with `pip install -r requirements.txt`.
- Maybe pytorch has to be installed differently on your machine.
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


## what can you do?

(Please have a look at the video to save yourself probably a lot of time for understanding)

### choice mode

In this mode you can:

- let youself explain the games
- end the dialog
- ask for thinking time (makes the game sleep)
- choose between the three games

### in-game

In-game, you can always:

- ask for the game rules
- end the game and get back to choice mode
- play the game
- ask for thinking time (makes the game sleep)

### animal and food game

These two games work as following:
At the beginning the game chooses a random letter. Based on the character both computer and user have to take turns naming animals (or foods in the food game) that start with the selected letter, until one of them doesn't know any animal or food anymore. You can't repeat something that has already been said.

### story / word sequence game

The word sequence game is not rather a game, more than it is an interactive story creation mode, ie.:

- user: I once went to a bar
- computer: where I saw
- user: how two people
- computer: danced with each other. One
- ... and so on until the user says to end the game

## what does not work so well

The ASR is sometimes stuck. As well as the entity recogntion, this might not work well at times.
