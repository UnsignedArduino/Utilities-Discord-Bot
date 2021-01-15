import os
from discord.ext import commands
from discord import Embed
from dotenv import load_dotenv
import asyncio

from dice import roll_as_embed

from ping import ping_as_embed

from timer import add_timer_as_embed, list_timers_nice_text, remove_timer_nice_text
from timer import pause_timer_nice_text, resume_timer_nice_text, get_timer_nice_text

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
    embed = ping_as_embed(bot=bot, times=average_times)
    logger.debug(f"Sent: {repr(embed)}")
    await ctx.send(embed=embed)


@bot.command(name="roll")
async def roll(ctx, sides: int = 6, times: int = 1):
    logger.debug(f"Dice roll requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: sides = {repr(sides)}, times = {repr(times)}")
    embed = roll_as_embed(sides=sides, times=times)
    logger.debug(f"Sent: {repr(embed)}")
    await ctx.send(embed=embed)


@bot.command(name="add-timer")
async def add_timer(ctx, name: str):
    logger.debug(f"Timer to be made requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    embed = add_timer_as_embed(guild=str(ctx.guild), name=name)
    logger.debug(f"Sent: {repr(embed)}")
    await ctx.send(embed=embed)


# TODO: Switch to embed
@bot.command(name="list-timers")
async def list_timers(ctx):
    logger.debug(f"Timer list requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: None!")
    text = list_timers_nice_text(guild=str(ctx.guild))
    logger.debug(f"Sent: {repr(text)}")
    await ctx.send(text)


# TODO: Switch to embed
@bot.command(name="remove-timer")
async def remove_timer(ctx, name: str):
    logger.debug(f"Timer to be popped requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    text = remove_timer_nice_text(guild=str(ctx.guild), name=name)
    logger.debug(f"Sent: {repr(text)}")
    await ctx.send(text)


# TODO: Switch to embed
@bot.command(name="pause-timer")
async def pause_timer(ctx, name: str):
    logger.debug(f"Timer to be paused requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    text = pause_timer_nice_text(guild=str(ctx.guild), name=name)
    logger.debug(f"Sent: {repr(text)}")
    await ctx.send(text)


# TODO: Switch to embed
@bot.command(name="resume-timer")
async def resume_timer(ctx, name: str):
    logger.debug(f"Timer to be resumed requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    text = resume_timer_nice_text(guild=str(ctx.guild), name=name)
    logger.debug(f"Sent: {repr(text)}")
    await ctx.send(text)


showing_timer = {}


# TODO: Switch to embed
@bot.command(name="show-timer")
async def show_timer(ctx, name: str):
    logger.debug(f"Timer to be shown requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    if ctx.guild not in showing_timer:
        showing_timer[ctx.guild] = False
    if showing_timer[ctx.guild]:
        message = await ctx.send(f"```\n⏲ Please wait, un-showing other timer! ⏲\n```")
        showing_timer[ctx.guild] = False
        await asyncio.sleep(3)
        await message.delete()
    text, con, _ = get_timer_nice_text(guild=str(ctx.guild), name=name)
    showing_timer[ctx.guild] = con
    logger.debug(f"Sent: {repr(text)}")
    message = await ctx.send(text)
    while True:
        await asyncio.sleep(1)
        text, con, time = get_timer_nice_text(guild=str(ctx.guild), name=name)
        if not showing_timer[ctx.guild]:
            if time is None:
                await message.edit(content=f"```\n⏲ Timer removed! ⏲\n```")
                break
            else:
                await message.edit(content=f"```\n⏲ Un-shown because you showed another timer or "
                                           "the timer does not exist! ⏲\n```")
                break
        showing_timer[ctx.guild] = con
        logger.debug(f"Sent: {repr(text)}")
        await message.edit(content=text)


@bot.event
async def on_command_error(ctx, error):
    embed = Embed(title="⚠ Error! ⚠", description="Uh oh, an error occurred!")
    embed.add_field(name="Error", value=error, inline=True)
    logger.warning(f"An error occurred! Sent: {repr(embed)}")
    await ctx.send(embed=embed)


logger.debug(f"Connecting to Discord...")
bot.run(TOKEN)
