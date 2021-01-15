from discord import Embed
import random


def roll(sides: int = 6, times: int = 1) -> list:
    dice_rolls = []
    for _ in range(times):
        dice_rolls.append(random.randint(1, sides + 1))
    return dice_rolls


def roll_as_embed(sides: int = 6, times: int = 1) -> Embed:
    times = min(23, times)
    embed = Embed(title="🎲 You rolled: 🎲")
    embed.add_field(name="Sides", value=str(sides), inline=True)
    embed.add_field(name="Times", value=str(times), inline=True)
    for index, value in enumerate(roll(sides=sides, times=times)):
        embed.add_field(name=f"Roll #{index+1}", value=str(value), inline=True)
    return embed
