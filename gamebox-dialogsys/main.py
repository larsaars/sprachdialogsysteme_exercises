#!/usr/bin/env python3

"""
dialogue manager for the gamebox bot
"""

from utils import asr, tts, rasa_parse, set_print_mode

# define the games
GAME_NONE = 0
GAME_ANIMAL = 1
GAME_FOOD = 2

# the currently running game
current_game = GAME_NONE


class Game:
    """abstract game class"""
    def __init__(self):
        """each game has to have an instruction set"""
        self.instructions = '' 
    
    def init_game(self):
        """initialize the game"""
        pass

    def next_input(self, entity):
        """get the next input from the user, we only expect games that are played with one word (with entities)"""
        pass

class AnimalGame(Game):
    def __init__(self):
        self.instructions = """The game is simple.
At the beginning of the game, I will decide upon a random letter.
Then, you will have to name an animal that starts with that letter.
Then, I will do the same.
We will continue until one of us can't think of an animal anymore."""

    def init_game(self):
        

    def next_input(self, entity):
        tts('Please name an animal.')

def confirm(text) -> bool:
    """
    ask the user for confirmation

    :param text: the text to confirm
    """
    tts(text)

    user_input = asr()
    if not user_input:
        return False

    intent, _ = rasa_parse(user_input)
    if intent == 'affirm':
        return True

    return False

def main():
    # run an infinite loop (till stopped)
    while True:
        # get the user's input and
        # parse what he/she said to get the intent and entity
        user_input = asr()
        if not user_input:
            tts('I\'m sorry, I didn\'t understand that. Please try again.')
            continue

        intent, entity = rasa_parse(user_input)

        # if the intent is None, the user's input could not be parsed
        # and there is an error with the server
        if not intent:
            break

        if game == GAME_NONE:
            tts('Please choose a game. You can play the animal game or the food game.')
            # if we are not currently running a game, we can start a new one
            if intent == 'choose_animal_game':
                current_game = GAME_ANIMAL
                game = AnimalGame()
                game.init_game()
            elif intent == 'choose_food_game':
                current_game = GAME_FOOD
                game = FoodGame()
                game.init_game()
            else:
                tts('Sorry, I didn\'t understand that. Please say again.')
        else:
            # is in a game
            # check if the intent is to stop the game or get the instructions
            if intent == 'end_game':
                if confirm('Do you really want to stop the game?'):
                    break
            elif intent == 'explain_rules':
                tts(game.instructions)
            else:
                # if the intent is not to stop the game or get the instructions,
                # we can assume that the user wants to play the game
                tts(game.next_input(entity))


if __name__ == "__main__":
    # set print mode to True to use stdin/stdout instead of asr/tts
    set_print_mode(True)
    # start game
    main()
