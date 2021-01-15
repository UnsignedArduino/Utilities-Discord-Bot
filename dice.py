import random


def roll(sides: int = 6):
    return random.randint(1, sides + 1)


def roll_nice_text(sides: int = 6):
    value = roll(sides=sides)
    return f"> 🎲 You got: {value}! 🎲", value
