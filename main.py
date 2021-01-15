import os
from discord.ext import commands
from dotenv import load_dotenv

from dice import roll_nice_text

from ping import ping_nice_text

from timer import add_timer_nice_text, list_timers_nice_text, remove_timer_nice_text
from timer import pause_timer_nice_text, resume_timer_nice_text

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
    logger.debug(f"Parameters: average_times = {average_times}")
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


@bot.command(name="add-timer")
async def add_timer(ctx, name: str):
    logger.debug(f"Timer to be made requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    text = add_timer_nice_text(name=name)
    logger.debug(f"Sent: {repr(text)}")
    await ctx.send(text)


@bot.command(name="list-timers")
async def list_timers(ctx):
    logger.debug(f"Timer list requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: None!")
    text = list_timers_nice_text()
    logger.debug(f"Sent: {repr(text)}")
    await ctx.send(text)


@bot.command(name="remove-timer")
async def remove_timer(ctx, name: str):
    logger.debug(f"Timer to be popped requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    text = remove_timer_nice_text(name=name)
    logger.debug(f"Sent: {repr(text)}")
    await ctx.send(text)


@bot.command(name="pause-timer")
async def pause_timer(ctx, name: str):
    logger.debug(f"Timer to be paused requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    text = pause_timer_nice_text(name=name)
    logger.debug(f"Sent: {repr(text)}")
    await ctx.send(text)


@bot.command(name="resume-timer")
async def resume_timer(ctx, name: str):
    logger.debug(f"Timer to be resumed requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    text = resume_timer_nice_text(name=name)
    logger.debug(f"Sent: {repr(text)}")
    await ctx.send(text)


@bot.event
async def on_command_error(ctx, error):
    text = f"```\n⚠ Uh oh, an error occurred!! ⚠\nError: {repr(error)}\n```"
    logger.warning(f"An error occurred! Sent: {repr(text)}")
    await ctx.send(text)


logger.debug(f"Connecting to Discord...")
bot.run(TOKEN)
