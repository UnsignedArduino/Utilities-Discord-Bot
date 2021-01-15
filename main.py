import os
from discord.ext import commands
from discord import Embed, Activity, ActivityType
from dotenv import load_dotenv
import asyncio

from dice import roll_as_embed

from ping import ping_as_embed

from timer import add_timer_as_embed, list_timers_as_embed, remove_timer_as_embed, clear_all_timers_as_embed
from timer import pause_timer_as_embed, resume_timer_as_embed, get_timer_as_embed

from create_logger import create_logger
import logging

logger = create_logger(name="discord", level=logging.DEBUG)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    logger.info(f"{bot.user.name} connected to Discord!")
    logger.debug(f"Connected to {len(bot.guilds)} guild(s)!")
    await bot.change_presence(activity=Activity(type=ActivityType.listening, name="/help"))


@bot.command(name="ping", help="Gets the latency of the bot in milliseconds.")
async def ping(ctx, average_times: int = 1):
    logger.debug(f"Ping requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: average_times = {average_times}")
    embed = ping_as_embed(bot=bot, times=average_times)
    logger.debug(f"Sent: {repr(embed)}")
    await ctx.send(embed=embed)


@bot.command(name="roll", help="Digitally rolls a dice for you.")
async def roll(ctx, sides: int = 6, times: int = 1):
    logger.debug(f"Dice roll requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: sides = {repr(sides)}, times = {repr(times)}")
    embed = roll_as_embed(sides=sides, times=times)
    logger.debug(f"Sent: {repr(embed)}")
    await ctx.send(embed=embed)


@bot.command(name="add-timer", help="Makes a new timer.")
async def add_timer(ctx, name: str):
    logger.debug(f"Timer to be made requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    embed = add_timer_as_embed(guild=str(ctx.guild), name=name)
    logger.debug(f"Sent: {repr(embed)}")
    await ctx.send(embed=embed)


@bot.command(name="list-timers", help="Lists all timers made on this guild.")
async def list_timers(ctx):
    logger.debug(f"Timer list requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: None!")
    embed = list_timers_as_embed(guild=str(ctx.guild))
    logger.debug(f"Sent: {repr(embed)}")
    await ctx.send(embed=embed)


@bot.command(name="remove-timer", help="Delete a timer.")
async def remove_timer(ctx, name: str):
    logger.debug(f"Timer to be popped requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    embed = remove_timer_as_embed(guild=str(ctx.guild), name=name)
    logger.debug(f"Sent: {repr(embed)}")
    await ctx.send(embed=embed)


@bot.command(name="pause-timer", help="Pause a running timer.")
async def pause_timer(ctx, name: str):
    logger.debug(f"Timer to be paused requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    embed = pause_timer_as_embed(guild=str(ctx.guild), name=name)
    logger.debug(f"Sent: {repr(embed)}")
    await ctx.send(embed=embed)


@bot.command(name="resume-timer", help="Resume a paused timer.")
async def resume_timer(ctx, name: str):
    logger.debug(f"Timer to be resumed requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    embed = resume_timer_as_embed(guild=str(ctx.guild), name=name)
    logger.debug(f"Sent: {repr(embed)}")
    await ctx.send(embed=embed)


showing_timer = {}


@bot.command(name="show-timer", help="Shows a message that will update live with the timer.")
async def show_timer(ctx, name: str):
    logger.debug(f"Timer to be shown requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: name = {repr(name)}")
    if ctx.guild not in showing_timer:
        showing_timer[ctx.guild] = False
    if showing_timer[ctx.guild]:
        message = await ctx.send(embed=Embed(title="⏲ Timer ⏲", description="Please wait, un-showing other timer!"))
        showing_timer[ctx.guild] = False
        await asyncio.sleep(3)
        await message.delete()
    embed, con = get_timer_as_embed(guild=str(ctx.guild), name=name)
    showing_timer[ctx.guild] = True
    logger.debug(f"Sent: {repr(embed)}")
    message = await ctx.send(embed=embed)
    while True:
        await asyncio.sleep(1)
        embed, con = get_timer_as_embed(guild=str(ctx.guild), name=name)
        if not showing_timer[ctx.guild]:
            await message.edit(embed=Embed(title="⏲ Timer ⏲",
                                           description="Un-shown because you showed another timer, hid it, removed it, "
                                                       "or the timer does not exist!"))
            break
        logger.debug(f"Sent: {repr(embed)}")
        await message.edit(embed=embed)


@bot.command(name="hide-timers", help="Stop showing a shown timer live.")
async def hide_timers(ctx):
    logger.debug(f"Timer to be hidden requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: None")
    showing_timer[ctx.guild] = False
    message = await ctx.send(embed=Embed(title="⏲ Timer ⏲", description="Stopping live timer updates..."))
    await asyncio.sleep(2)
    await message.edit(embed=Embed(title="⏲ Timer ⏲", description="Successfully stopped live timer updates!"))


@bot.command(name="clear-all-timers", help="Deletes all timers.")
async def clear_all_timers(ctx):
    logger.debug(f"All timers to be cleared requested from {repr(ctx.guild)}")
    logger.debug(f"Parameters: None")
    embed = clear_all_timers_as_embed(guild=str(ctx.guild))
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    embed = Embed(title="⚠ Error! ⚠", description="Uh oh, an error occurred!")
    embed.add_field(name="Error", value=error, inline=True)
    logger.warning(f"An error occurred! Sent: {repr(embed)}")
    await ctx.send(embed=embed)


logger.debug(f"Connecting to Discord...")
bot.run(TOKEN)
