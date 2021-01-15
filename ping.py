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


def ping_nice_text(bot, times: int = 1) -> tuple:
    times = round(times)
    average, minimum, maximum = ping(bot, times=times)
    if times > 1:
        return f"```\n🏓 Pong! 🏓 Ping is {average} ms! (Averaged over {times} times)\nFastest: {minimum}\nSlowest: {maximum}```", average
    return f"```\n🏓 Pong! 🏓 Ping is {average} ms!\n```", average
