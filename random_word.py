import string
import random

def get_random_word(length):
    """Generate a random word with a specified length"""
    
    word = []
    for i in range(length):
        word.append(random.choice(string.ascii_letters))

    return ''.join(word)