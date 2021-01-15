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


def add_timer(name: str = f"timer{len(timers)}") -> None:
    if name not in timers:
        timers[name] = Timer()
    else:
        raise DuplicateTimerError


def add_timer_nice_text(name: str = f"timer{len(timers)}") -> str:
    try:
        add_timer(name=name)
    except DuplicateTimerError:
        return f"```\n⚠ Error! ⚠ A timer with the same name is already in use!\n```"
    else:
        return f"```\n⏲ Timer with name {repr(name)} successfully created! ⏲\n```"


def list_timers_nice_text() -> str:
    text = "```\n⏲ Timers found: ⏲\n"
    if len(timers) > 0:
        for name, timer in timers.items():
            timer.update()
            text += f" - {repr(name)}: {timer.pretty_time} - {'Running' if timer.timing else 'Paused'}\n"
    else:
        text += "No timers found! Create one with \"/add-timer\"!\n"
    text += "```"
    return text


def update_timer(name: str) -> None:
    timers[name].update()


def remove_timer(name: str) -> None:
    timers.pop(name)


def remove_timer_nice_text(name: str) -> str:
    try:
        remove_timer(name=name)
    except KeyError:
        return f"```\n⚠ Error! ⚠ Could not find that timer! Use \"/list-timers\" to list all timers!\n```"
    else:
        return f"```\n⏲ Timer with name {repr(name)} successfully deleted! ⏲\n```"


def pause_timer(name: str) -> None:
    update_timer(name=name)
    timers[name].timing = False


def pause_timer_nice_text(name: str) -> str:
    try:
        pause_timer(name=name)
    except KeyError:
        return f"```\n⚠ Error! ⚠ Could not find that timer! Use \"/list-timers\" to list all timers!\n```"
    else:
        return f"```\n⏲ Timer with name {repr(name)} paused! ⏲\n```"


def resume_timer(name: str) -> None:
    update_timer(name=name)
    timers[name].timing = True


def resume_timer_nice_text(name: str) -> str:
    try:
        resume_timer(name=name)
    except KeyError:
        return f"```\n⚠ Error! ⚠ Could not find that timer! Use \"/list-timers\" to list all timers!\n```"
    else:
        return f"```\n⏲ Timer with name {repr(name)} resumed! ⏲\n```"

