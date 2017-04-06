import configparser
import warnings

import never_importer


config = configparser.ConfigParser()
CONFIG_PATH = never_importer.PROJECT_PATH + '/config.ini'
config.read(CONFIG_PATH)

SELECTED_LANGUAGE = config['LANGUAGE']['selected_language']


class LanguageNotImplemented(Exception):
    pass


class EnglishMissingError(Exception):
    pass


class MissingTranslationWarning(Warning):
    pass

SUPPORTED_LANGUAGES = set()


class Language(str):
    def __new__(cls, name, native_name):
        inst = str.__new__(cls, name)
        inst.name_native = native_name  # Language name spelled with characters of the language itself
        SUPPORTED_LANGUAGES.add(name)
        return inst


# In reality, separators differ for different english-speaking countries
# (e.g. eng_US, eng_ireland, eng_UK ..).
# Since this program is not expected to become very popular initially,
# the convention below should be ok.
# Alternatively, the user could be prompted to select his separator;
# the prompt should be in a very easy to understand form:
# e.g. "Three point one." Select the image that is accurate (used for separator blabla..)
english = Language(name='english', native_name='english')
greek = Language(name='greek',  native_name='ελληνικά')


if SELECTED_LANGUAGE not in SUPPORTED_LANGUAGES:
    raise LanguageNotImplemented('"{}" not implemented'.format(SELECTED_LANGUAGE))


class Message(str):
    def __new__(cls, texts_dct):
        if english not in texts_dct:
            raise EnglishMissingError
        if SELECTED_LANGUAGE in texts_dct:
            s = texts_dct[SELECTED_LANGUAGE]
        else:
            s = texts_dct[english]
            warnings.warn(
                """Missing some translations in {} (will use english instead).
                Check corresponding module.""".format(SELECTED_LANGUAGE),
                MissingTranslationWarning)
        inst = str.__new__(cls, s)
        return inst


# Template
"""
Message(
    texts_dct={
        english: ,
        greek: ,
    })


Message(
    texts_dct={
        languages.english: ,
        languages.greek: ,
    })
"""


ABOUT_MSG = Message(
    texts_dct={
        english: 'About',
        greek: 'Σχετικά',
    })

SOLVE_FOR_X_QUESTION_MSG = Message(
    texts_dct={
        english: 'Find the value of x.',
        greek: 'Βρες την τιμή του x.',
    })
