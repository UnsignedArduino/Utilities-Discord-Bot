import os
from discord.ext import commands
from dotenv import load_dotenv
from dice import roll_nice_text
from ping import ping_nice_text
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
async def ping(ctx, average_times: int = 1):
    logger.debug(f"Ping requested from {repr(ctx.guild)}")
    text, _ = ping_nice_text(bot=bot, times=average_times)
    logger.debug(f"Sent: {repr(text)}")
    await ctx.send(text)


@bot.command(name="roll")
async def roll(ctx, sides: int = 6, times: int = 1):
    logger.debug(f"Dice roll requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: sides = {repr(sides)}, times = {repr(times)}")
    text, value = roll_nice_text(sides=sides, times=times)
    logger.debug(f"Sent: {repr(text)}")
    await ctx.send(text)


@bot.event
async def on_command_error(ctx, error):
    text = f"```\n⚠ Uh oh, the error was too fast for us to catch! ⚠\nError: {repr(error)}\n```"
    logger.warning(f"An error occurred! Sent: {repr(text)}")
    await ctx.send(text)


logger.debug(f"Connecting to Discord...")
bot.run(TOKEN)
