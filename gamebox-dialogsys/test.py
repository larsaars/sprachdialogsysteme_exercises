#!/usr/bin/env python3

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import random

# Load pre-trained model tokenizer (vocabulary)
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Load pre-trained model (weights)
model = GPT2LMHeadModel.from_pretrained('gpt2')

def predict(text: str, n_limit=50):
    """
    Generate text using a pre-trained GPT-2 model.

    :param text: Input text to start generating from.
    :param n_limit: Maximum number of words to generate. Note this limits the total
                     output length including the input text.

    :return: Generated text.
    """


    # Encode the input text
    input_ids = tokenizer.encode(text, return_tensors='pt')

    # Calculate the number of tokens in the input
    input_tokens_count = input_ids.size(1)

    # Generate text
    attention_mask = torch.ones(input_ids.shape, device=input_ids.device) # Ensure attention is only on the input sequence
    output_sequences = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=input_tokens_count + n_limit,  # Adjust max_length for the desired number of additional tokens
        temperature=1.0,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )

    # Decode the output
    return tokenizer.decode(output_sequences[0], skip_special_tokens=True)


text = ''
while True:
    user_input = input('>> ')
    text += ' ' + user_input

    prediction = predict(text, n_limit=len(user_input.split(' ')))[len(text):].replace('\n', ' ')
    text += prediction
    print(prediction)
