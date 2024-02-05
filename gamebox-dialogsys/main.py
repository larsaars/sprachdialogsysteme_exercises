#!/usr/bin/env python3

"""
dialogue manager for the gamebox bot
"""

from utils import asr, tts, rasa_parse, get_print_mode, set_print_mode
from games import AnimalGame, FoodGame, WordSequenceGame, all_games_instructions
from time import sleep
import random


def confirm(text) -> bool:
    """
    ask the user for confirmation

    :param text: the text to confirm
    """
    tts(text)

    user_input = asr()
    if not user_input:
        return False

    affirmations = ['yes', 'yeah', 'yep', 'yup', 'sure', 'ok', 'okay']
    user_input = user_input.lower().strip()

    # if one of the affirmations is contained in user_input, return True
    if any([True for affirmation in affirmations if affirmation in user_input]):
        return True

    return False

def main():
    # the currently running game
    current_game = None 

    # give entry message
    tts('Hello! I am the gamebox bot. I can play three games with you: the animal, food or word sequence game. Which game would you like to play?')
    
    # run an infinite loop (till stopped)
    while True:
        # get the user's input and
        # parse what he/she said to get the intent and entity
        user_input = asr()
        if not user_input:
            # sleep some time before asking the user to repeat, to avoid asking too often
            sleep(5)
            tts('I\'m sorry, I didn\'t understand that. Please try again. (asr)')
            continue

        intent, entity = rasa_parse(user_input)

        # if is in print mode print the intent and entity
        if get_print_mode():
            print(f'__{intent}, {entity}')

        # if the intent is None, the user's input could not be parsed
        # and there is an error with the server
        if not intent:
            break

        # if entity is None, we can assume that the user's input is the entity
        # (or at least treat it as such for the games)
        if entity is None:
            entity = user_input.lower().strip()

        # if intent is NLU_FALLBACK, the user's input could not be parsed
        # and we should ask the user to repeat
        if intent == 'nlu_fallback':
            tts('I\'m sorry, I didn\'t understand that. Please try again. (nlu_fallback))')
            continue
        # if the intent is wait, the program will sleep a little for the user to think
        elif intent == 'wait':
            # don't always say the same thing here
            tts(random.choice(['Okay. I will sleep a while and let you think.', 'I will give you some time to think.', 'I will wait a little.']))
            tts('And tell you when I\'m back.')
            sleep(20)  # sleep for n secs
            tts('I\'m back. Have you thought of something?')
            continue

        if current_game == None:
            # if we are not currently running a game, we can start a new one
            if intent == 'choose_animal_game':
                current_game = AnimalGame()
            elif intent == 'choose_food_game':
                current_game = FoodGame()
            elif intent == 'choose_word_sequence_game':
                current_game = WordSequenceGame()
            elif intent == 'explain_rules':
                tts(all_games_instructions)
            elif intent == 'end_game':
                tts('Okay! Goodbye!')
                break
            else:
                tts('Sorry, I didn\'t understand that. Please say again which game you want to play.')
        else:
            # is in a game
            # check if the intent is to stop the game or get the instructions
            if intent == 'end_game':
                if confirm('Do you really want to stop the game?'):
                    current_game = None
                    tts('Okay let\'s play another game. Which game would you like to play? We can play the animal, food or word sequence game.')
                else:
                    tts('Okay. I will continue the game.')
            elif intent == 'explain_rules':
                tts(current_game.instructions)
            else:
                # if the intent is not to stop the game or get the instructions,
                # we can assume that the user wants to play the game
                # if game.next_input is true, it is game over
                if current_game.next_input(intent, entity):
                    break



if __name__ == "__main__":
    # set print mode to True to use stdin/stdout instead of asr/tts
    set_print_mode(False)
    # start game
    main()
