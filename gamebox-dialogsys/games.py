#!/usr/bin/env python3

"""
games module for the dialogmanager
"""

from utils import asr, tts, rasa_parse

import string
import random
import json


class Game:
    """abstract game class"""
    def __init__(self):
        """each game has to have an instruction set"""
        self.instructions = '' 

    def next_input(self, intent, entity) -> bool:
        """
        get the next input from the user, we only expect games that are played with one word (with entities)

        :param intent: the intent of the user's input
        :param entity: the entity of the user's input
        :return: True if the game is over, False otherwise
        """
        return False


class FoodGame(Game):
    pass

class AnimalGame(Game):

    def __init__(self):
        self.instructions = """At the beginning of the game, I will decide upon a random letter.
Then, you will have to name an animal that starts with that letter.
Then, I will do the same.
We will continue until one of us can't think of an animal anymore.
You can't repeat animals."""
        # generate a random letter
        self.letter = random.choice(string.ascii_uppercase)

        # load the list of animals starting with the letter
        # from the json file
        with open('./game_data/animals.json', 'r') as f:
            self.animals = json.load(f)[self.letter]
        # set the animals index counter to zero
        self.animals_index = -1
        # set of animals already used
        self.used_animals = set()
        # generate a random number between 3-10
        # after which the computer will give up
        self.give_up_at = random.randint(1, 10)
        self.give_up_counter = 0

        # start the game!
        tts('Good choice! Let\'s play the animal game. I will start.')
        tts(f'I have chosen the letter {self.letter}. Your turn.')


    def _get_next_animal(self):
        # update animal index
        self.animals_index += 1
        # check if we have reached the end of the list
        if self.animals_index >= len(self.animals):
            return None
        
        # else get the next animal
        next_animal = self.animals[self.animals_index]

        # if the next animal has already been used, get the next one recursively
        if next_animal in self.used_animals:
            return self._get_next_animal()
        else:
            # add to list of used animals and return
            self.used_animals.add(next_animal)
            return next_animal

    def next_input(self, intent, entity) -> bool:
        if intent != 'game_answer':
            tts('I\'m sorry, I didn\'t understand your animal. Could you please repeat that?')
            # feeback is game_answer
        else:
            # check if the animal starts with the right letter
            if entity[0].upper() == self.letter:
                # check if animal has already been used
                if entity not in self.used_animals:
                    self.used_animals.add(entity)
                    # correct case!
                    # btw, we do not really check if this is really an existing animal
                    # but we could do that with a web request
                    # for now, we just assume that the user is honest
                    # and knows the rules of the game

                    # check as well if the computer gives up
                    if self.give_up_counter >= self.give_up_at:
                        tts(f'Good call! I give up. I can\'t think of any more animals starting with {self.letter}. You won!')
                        return True  # return true to end the game
                    else:
                        # computer's turn
                        next_animal = self._get_next_animal()

                        # if is None, we have reached the end of the list
                        if not next_animal:
                            tts(f'Good call! I can\'t think of any more animals starting with {self.letter}. You won!')
                            return True
                        else:
                            # don't always say the same thing
                            tts(random.choice([f'Great! {entity} is a valid animal. I\'ll say {next_animal}. Your turn.',
                                               f'Nice choice! I\'ll say {next_animal}. Your turn.',
                                               f'Good one! I\'ll say {next_animal}.',
                                               f'You got it! I\'ll say {next_animal}. Your turn.']))
                            # increment the give up counter
                            self.give_up_counter += 1

                else:
                    tts('This animal has already been named! Try again.')
            else:
                tts(f'The animal has to start with the letter {self.letter}. Please try again.')

        return False  # return False to continue game
