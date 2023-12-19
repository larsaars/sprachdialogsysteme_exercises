#!/usr/bin/env python3

from gtts import gTTS
import speech_recognition as sr
import spacy

class VendingMachine:
    def __init__(self):
        self.inventory = {'cat': 10, 'dog': 15, 'hamster': 20}
        self.nlp = spacy.load('en_core_web_sm')

    def text_to_speech(self, text):
        print(text)

    def speech_recognition(self):
        return input('>> ')
        # recognizer = sr.Recognizer()

        # with sr.Microphone() as source:
        #     print("Please speak. You can say 'exit' to end the session.")
        #     recognizer.adjust_for_ambient_noise(source)

        #     try:
        #         audio = recognizer.listen(source, timeout=5)
        #         return recognizer.recognize_google(audio).lower()
        #     except sr.UnknownValueError:
        #         return None
    

    def analyze_input(self, text):
        doc = self.nlp(text)
        animal, quantity = None, None

        for ent in doc.ents:
            if ent.label_ == 'ANIMAL':
                animal = ent.text
            elif ent.label_ == 'QUANTITY':
                quantity = int(ent.text)

        return animal, quantity

    def start_dialog(self):
        self.text_to_speech("Welcome to the Animal Feed Vending Machine!")

        while True:
            self.text_to_speech("Please tell me about your animal or say 'exit' to quit.")
            user_input = self.speech_recognition()

            if user_input == 'exit':
                self.text_to_speech("Thank you for using the vending machine. Goodbye!")
                break

            animal, quantity = self.analyze_input(user_input)

            if not animal:
                self.text_to_speech("I couldn't understand the type of animal. Please try again.")
                continue

            if animal not in self.inventory:
                self.text_to_speech(f"Sorry, we don't have feed for {animal}.")
                continue

            if not quantity:
                self.text_to_speech("I couldn't understand the quantity. Please try again.")
                continue

            if quantity <= 0:
                self.text_to_speech("Please specify a positive quantity.")
                continue

            if quantity > self.inventory[animal]:
                self.text_to_speech(f"Sorry, we don't have enough sacks for {animal}.")
            else:
                self.inventory[animal] -= quantity
                self.text_to_speech(f"Dispensing {quantity} sacks of animal feed for {animal}. Remaining inventory: {self.inventory}")

vending_machine = VendingMachine()
vending_machine.start_dialog()
