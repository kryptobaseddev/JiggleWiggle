from threading import Event
import ctypes

class StopEvent(Event):
    """A wrapper around threading.Event to manage stopping of threads."""
    pass