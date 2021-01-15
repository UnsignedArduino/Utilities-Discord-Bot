from discord import Embed
from time import time as unix
from datetime import timedelta


class DuplicateTimerError(BaseException):
    """A timer with the same name is already in use."""


class Timer:
    def __init__(self):
        self.timing = True
        self.time = 0
        self.last_check_time = unix()

    def update(self) -> None:
        if self.timing:
            self.time += unix() - self.last_check_time
        self.last_check_time = unix()

    @property
    def pretty_time(self) -> str:
        return str(timedelta(seconds=self.time))


timers = {}


def add_timer(guild: str, name: str = f"timer{len(timers)}") -> None:
    if guild not in timers:
        timers[guild] = {}
    if name not in timers[guild]:
        timers[guild][name] = Timer()
    else:
        raise DuplicateTimerError


def add_timer_as_embed(guild: str, name: str = f"timer{len(timers)}") -> Embed:
    try:
        add_timer(guild=guild, name=name)
    except DuplicateTimerError:
        return Embed(title="⚠ Error! ⚠", description="A timer with the same name is already in use!")
    else:
        return Embed(title="⏲ Timer ⏲", description=f"Timer named {repr(name)} successfully created!")


def list_timers_as_embed(guild: str) -> Embed:
    embed = Embed(title="⏲ Timer ⏲", description="Timers found:")
    if guild not in timers:
        timers[guild] = {}
    if len(timers[guild]) > 0:
        for name, timer in timers[guild].items():
            timer.update()
            embed.add_field(name=repr(name), value=f"{timer.pretty_time} - {'Running' if timer.timing else 'Paused'}", inline=False)
    else:
        embed.add_field(name="No timers found!", value="Create a timer with \"/add-timer\"!", inline=True)
    return embed


def update_timer(guild: str, name: str) -> None:
    timers[guild][name].update()


def remove_timer(guild: str, name: str) -> None:
    timers[guild].pop(name)


def remove_timer_as_embed(guild: str, name: str) -> Embed:
    try:
        remove_timer(guild=guild, name=name)
    except KeyError:
        return Embed(title="⚠ Error! ⚠", description="Could not find a timer with that name! "
                                                     "Use \"/list-timers\" to list all timers!")
    else:
        return Embed(title="⏲ Timer ⏲", description=f"Timer named {repr(name)} successfully deleted!")


def pause_timer(guild: str, name: str) -> None:
    update_timer(guild=guild, name=name)
    timers[guild][name].timing = False


def pause_timer_as_embed(guild: str, name: str) -> Embed:
    try:
        pause_timer(guild=guild, name=name)
    except KeyError:
        return Embed(title="⚠ Error! ⚠", description="Could not find a timer with that name! "
                                                     "Use \"/list-timers\" to list all timers!")
    else:
        return Embed(title="⏲ Timer ⏲", description=f"Timer named {repr(name)} paused!")


def resume_timer(guild: str, name: str) -> None:
    update_timer(guild=guild, name=name)
    timers[guild][name].timing = True


def resume_timer_as_embed(guild: str, name: str) -> Embed:
    try:
        resume_timer(guild=guild, name=name)
    except KeyError:
        return Embed(title="⚠ Error! ⚠", description="Could not find a timer with that name! "
                                                     "Use \"/list-timers\" to list all timers!")

    else:
        return Embed(title="⏲ Timer ⏲", description=f"Timer named {repr(name)} resumed!")


def get_timer_as_embed(guild: str, name: str) -> tuple:
    try:
        timer = timers[guild][name]
        timer.update()
    except KeyError:
        return Embed(title="⚠ Error! ⚠", description="Could not find a timer with that name! "
                                                     "Use \"/list-timers\" to list all timers!"), False
    else:
        return Embed(title="⏲ Timer ⏲", description=f"{repr(name)}: {timer.pretty_time} - "
                                                    f"{'Running' if timer.timing else 'Paused'}"), True
