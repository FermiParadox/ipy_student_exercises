# DO NOT IMPORT ANYTHING HERE
# to avoid circular imports.


class UnexpectedValueError(Exception):
    """Used for Exceptions that should not be handled,
    instead of an existing Exception (to prevent accidental handling during `try`).
    """
    pass

