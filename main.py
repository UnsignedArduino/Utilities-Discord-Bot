import os
from discord.ext import commands
from dotenv import load_dotenv
import dice
from create_logger import create_logger
import logging

logger = create_logger(name=__name__, level=logging.DEBUG)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    logger.info(f"{bot.user.name} connected to Discord!")
    logger.debug(f"Connected to {len(bot.guilds)} guild(s)!")


@bot.command(name="ping")
async def ping(ctx):
    logger.debug(f"Ping requested from {repr(ctx.guild)}")
    ping = round(bot.latency * 1000)
    logger.debug(f"Ping is {ping} ms!")
    await ctx.send(f"> 🏓 Pong! 🏓 Ping is {ping} ms!")


@bot.command(name="roll")
async def roll(ctx):
    logger.debug(f"Dice roll requested from {repr(ctx.guild)}")
    sides = 6
    text, value = dice.roll_nice_text(sides=sides)
    logger.debug(f"Dice with {sides} sides rolled a {value}!")
    await ctx.send(text)


bot.run(TOKEN)
