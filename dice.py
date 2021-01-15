import random


def roll(sides: int = 6, times: int = 1) -> list:
    dice_rolls = []
    for _ in range(times):
        dice_rolls.append(random.randint(1, sides + 1))
    return dice_rolls


def roll_nice_text(sides: int = 6, times: int = 1) -> tuple:
    text = "```\n🎲 You got: "
    values = []
    for index, value in enumerate(roll(sides=sides, times=times)):
        if index == 0:
            text += str(value)
        else:
            text += f", {value}"
        values += str(value)
    text += "! 🎲\n```"
    return text, values
