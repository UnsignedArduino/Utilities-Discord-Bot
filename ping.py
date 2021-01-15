from discord import Embed


def ping(bot, times: int = 1) -> tuple:
    average = round(bot.latency * 1000)
    minimum = average
    maximum = average
    for _ in range(times-1):
        pong = round(bot.latency * 1000)
        average += pong
        average /= 2
        if pong > maximum:
            maximum = pong
        if pong < minimum:
            minimum = pong
    return average, minimum, maximum


def ping_as_embed(bot, times: int = 1) -> Embed:
    times = round(times)
    average, minimum, maximum = ping(bot, times=times)
    embed = Embed(title="🏓 Pong! 🏓")
    embed.add_field(name="Ping is", value=average, inline=True)
    if times > 1:
        embed.add_field(name="Minimum", value=minimum, inline=True)
        embed.add_field(name="Maximum", value=maximum, inline=True)
        embed.add_field(name="Times", value=str(times), inline=True)
    return embed
