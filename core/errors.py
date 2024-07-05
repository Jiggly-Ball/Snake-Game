class BaseError(Exception):
    """The base class to all errors in Snake Game."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StateError(BaseError):
    """Raised when a operation is done over an invalid state."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ExitStateError(BaseError):
    """An error class used to exit the current state."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ExitGameError(BaseError):
    """An error class used to exit out of the game"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
