# DO NOT IMPORT ANY PROJECT MODULES HERE
# to avoid circular imports.
import os


# WARNING: project-path assumes this file is in the project folder itself.
CURRENT_FILE_PATH = os.path.abspath(__file__)
PROJECT_PATH = os.path.dirname(CURRENT_FILE_PATH)
PROJECT_PARENT_PATH = os.path.dirname(PROJECT_PATH)


class UnexpectedValueError(Exception):
    """Used for Exceptions that should not be handled,
    instead of an existing Exception (to prevent accidental handling during `try`).
    """
    pass

