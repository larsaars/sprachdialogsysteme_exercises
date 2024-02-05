#!/usr/bin/env python3

"""
games module for the dialogmanager
"""

from utils import asr, tts, rasa_parse

import string
import random
import json
from time import sleep

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel


all_games_instructions = """The animal game works as follows: At the beginning of the game, I will decide upon a random letter.
Then, you will have to name an animal that starts with that letter.
Then, I will do the same.
We will continue until one of us can't think of an animal anymore.
You can't repeat animals.
The food game works the same way, but with food instead of animals.
The word sequence or story game is different.
You will start with as many words as you like.
Then I will continue the text you started with as many words as I like.
This way we try to tell a story together.
The game does not end, until you say so."""

class Game:
    """abstract game class"""
    def __init__(self):
        """each game has to have an instruction set"""
        self.instructions = '' 

    def next_input(self, user_input, intent, entity) -> bool:
        """
        get the next input from the user, we only expect games that are played with one word (with entities)

        :param intent: the intent of the user's input
        :param entity: the entity of the user's input
        :return: True if the game is over, False otherwise
        """
        return False


class FoodGame(Game):

    def __init__(self):
        self.instructions = """At the beginning of the game, I will decide upon a random letter.
Then, you will have to name a food that starts with that letter.
Then, I will do the same.
We will continue until one of us can't think of an food anymore.
You can't repeat foods."""
        # generate a random letter
        self.letter = random.choice(string.ascii_uppercase)

        # load the list of foods starting with the letter
        # from the json file
        with open('./game_data/foods.json', 'r') as f:
            self.foods = json.load(f)[self.letter]
        # set the foods index counter to zero
        self.foods_index = 0
        # set of foods already used
        self.used_foods = set()
        # generate a random number between 3-10
        # after which the computer will give up
        self.give_up_at = random.randint(1, 10)
        self.give_up_counter = 0

        # get the first food to be said
        first_food = self._get_next_food()
        # start the game!
        tts('Good choice! Let\'s play the food game. I will start.')
        tts(f'I have chosen the letter {self.letter}. I begin by saying {first_food}. Now it\'s your turn!')


    def _get_next_food(self):
        # update food index
        self.foods_index += 1
        # check if we have reached the end of the list
        if self.foods_index >= len(self.foods):
            return None
        
        # else get the next food
        next_food = self.foods[self.foods_index]

        # if the next food has already been used, get the next one recursively
        if next_food in self.used_foods:
            return self._get_next_food()
        else:
            # add to list of used foods and return
            self.used_foods.add(next_food)
            return next_food

    def next_input(self, user_input, intent, entity) -> bool:
        if intent != 'game_answer':
            tts('I\'m sorry, I didn\'t understand your food. Could you please repeat that?')
            # feeback is game_answer
        else:
            # check if the food starts with the right letter
            if entity[0].upper() == self.letter:
                # check if food has already been used
                if entity not in self.used_foods:
                    self.used_foods.add(entity)
                    # correct case!
                    # btw, we do not really check if this is really an existing food
                    # but we could do that with a web request
                    # for now, we just assume that the user is honest
                    # and knows the rules of the game

                    # check as well if the computer gives up
                    if self.give_up_counter >= self.give_up_at:
                        tts(f'Good call! I give up. I can\'t think of any more foods starting with {self.letter}. You won!')
                        return True  # return true to end the game
                    else:
                        # computer's turn
                        next_food = self._get_next_food()

                        # if is None, we have reached the end of the list
                        if not next_food:
                            tts(f'Good call! I can\'t think of any more foods starting with {self.letter}. You won!')
                            return True
                        else:
                            # it is nice to have some randomness in the game
                            # so that the computer does not always say the same thing
                            # and the game is more fun
                            # sleep a little bit sometimes to pretend to think
                            if random.random() < 0.3:
                                tts(random.choice(['Good one! I need some time to think',
                                                   'Nice choice! I need some time to think',
                                                   'Great! Wait...',
                                                   'Ok...']))
                                sleep(random.uniform(1, 4))
                                tts(random.choice([f'Got something! I\'ll say {next_food}. Your turn.',
                                                   f'Ok, I\'ll say {next_food}. Your turn.',
                                                   f'Here we go! I\'ll say {next_food}. Your turn.',]))
                            else:
                                # don't always say the same thing
                                tts(random.choice([f'Great! {entity} is a valid food. I\'ll say {next_food}. Your turn.',
                                                   f'Nice choice! I\'ll say {next_food}. Your turn.',
                                                   f'Good one! I\'ll say {next_food}.',
                                                   f'You got it! I\'ll say {next_food}. Your turn.']))
                            # increment the give up counter
                            self.give_up_counter += 1

                else:
                    tts('This food has already been named! Try again.')
            else:
                tts(f'The food has to start with the letter {self.letter}. Please try again.')

        return False  # return False to continue game

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
        self.animals_index = 0
        # set of animals already used
        self.used_animals = set()
        # generate a random number between 3-10
        # after which the computer will give up
        self.give_up_at = random.randint(1, 10)
        self.give_up_counter = 0

        # get the first animal to be said
        first_animal = self._get_next_animal()
        # start the game!
        tts('Good choice! Let\'s play the animal game. I will start.')
        tts(f'I have chosen the letter {self.letter}. I begin by saying {first_animal}. Now it\'s your turn!')


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

    def next_input(self, user_input, intent, entity) -> bool:
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
                            # it is nice to have some randomness in the game
                            # so that the computer does not always say the same thing
                            # and the game is more fun
                            # sleep a little bit sometimes to pretend to think
                            if random.random() < 0.3:
                                tts(random.choice(['Good one! I need some time to think',
                                                   'Nice choice! I need some time to think',
                                                   'Great! Wait...',
                                                   'Ok...']))
                                sleep(random.uniform(1, 4))
                                tts(random.choice([f'Got something! I\'ll say {next_animal}. Your turn.',
                                                   f'Ok, I\'ll say {next_animal}. Your turn.',
                                                   f'Here we go! I\'ll say {next_animal}. Your turn.',]))
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


class WordSequenceGame(Game):
    
    def __init__(self):
        self.instructions = """You will start with as many words as you like.
Then I will continue the text you started with as many words as I like.
This way we try to tell a story together.
The game does not really end, until you say so."""

        # set text to empty string
        self.text = ''

        # load the transformer models
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')

        # start the game!
        tts('Great! Let\'s play the word sequence game. You can start by saying as many words as you like. I will continue from there.')

    def _predict_next_words(self, text: str, n_limit=1):
        """
        Generate text using a pre-trained GPT-2 model.

        :param text: Input text to start generating from.
        :param n_limit: Maximum number of words to generate. Note this limits the total
                         output length including the input text.

        :return: Generated text.
        """


        # Encode the input text
        input_ids = self.tokenizer.encode(text, return_tensors='pt')

        # Calculate the number of tokens in the input
        input_tokens_count = input_ids.size(1)

        # Generate text
        attention_mask = torch.ones(input_ids.shape, device=input_ids.device) # Ensure attention is only on the input sequence
        output_sequences = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=input_tokens_count + n_limit,  # Adjust max_length for the desired number of additional tokens
            temperature=1.0,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id
        )

        # Decode the output
        return self.tokenizer.decode(output_sequences[0], skip_special_tokens=True)


    def next_input(self, user_input, intent, entity) -> bool:
        # add the user's input to the text
        self.text += ' ' + user_input

        # make prediction about the next words
        # generate a random amount of next words
        n_limit = random.randint(1, 10)
        # (prediction is only the next words, not the whole text)
        prediction = self._predict_next_words(self.text, n_limit=n_limit)[len(self.text):].replace('\n', ' ')

        # add the prediction to the text
        self.text += prediction

        # say the prediction and wait for next input
        tts(prediction)

        return False

