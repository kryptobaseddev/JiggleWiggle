from threading import Event
import ctypes

class SystemSettings:
    """A class that manages system settings related to sleep and screen saver using Windows API."""

    prevent_sleep_active = False  # Track sleep state manually

    @staticmethod
    def prevent_sleep():
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000003)
        SystemSettings.prevent_sleep_active = True

    @staticmethod
    def allow_sleep():
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        SystemSettings.prevent_sleep_active = False

    @staticmethod
    def disable_screen_saver():
        ctypes.windll.user32.SystemParametersInfoW(0x0011, 0, 0, 0)

    @staticmethod
    def enable_screen_saver():
        ctypes.windll.user32.SystemParametersInfoW(0x0011, 1, 0, 0)

    @staticmethod
    def is_sleep_prevented():
        """Check if sleep prevention is active based on the last known state."""
        return SystemSettings.prevent_sleep_active

    @staticmethod
    def is_screen_saver_disabled():
        """Check if the screen saver is disabled."""
        is_active = ctypes.c_int()
        ctypes.windll.user32.SystemParametersInfoW(0x0010, 0, ctypes.byref(is_active), 0)
        return is_active.value == 0  # If the screen saver is disabled, value is 0.

class StopEvent(Event):
    """A wrapper around threading.Event to manage stopping of threads."""

    def clear(self):
        """Override the clear method to add extra checks or logs if needed."""
        super().clear()

    def set(self):
        """Override the set method to add extra checks or logs if needed."""
        super().set()
