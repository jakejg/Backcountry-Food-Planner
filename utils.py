import string
import random

def to_lbs(amount):
    """Converts an amount from grams to lbs rounded to two decimal places"""

    return round(amount*.0022, 2)

def get_random_word(length):
    """Generate a random word with a specified length"""
    
    word = []
    for i in range(length):
        word.append(random.choice(string.ascii_letters))

    return ''.join(word)