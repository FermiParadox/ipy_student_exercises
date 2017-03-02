import configparser


config = configparser.ConfigParser()
config.read('config.ini')

SELECTED_LANGUAGE = config['LANGUAGE']['selected_language']


class LanguageNotImplemented(Exception):
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
        inst = str.__new__(cls, texts_dct[SELECTED_LANGUAGE])
        return inst


ABOUT = Message(
    texts_dct={
        english: 'About',
        greek: 'Σχετικά',
    })

