import main

# TODO: refactor; make all strings classes whose usage in final string is enforced
_MIT_LICENCE = """'The MIT License (MIT)'
{}

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

_KIVY_LICENCE_FIRST_LINE = "Copyright (c) 2010-2016 Kivy Team and other contributors"

with open('LICENSE.txt') as _license_file:
    _license_file_as_str = _license_file.read()
PROJECT_LICENCE = _license_file_as_str

KIVY_LICENCE = _MIT_LICENCE.format(_KIVY_LICENCE_FIRST_LINE)

EMAIL = 'FermiParadoxSo@gmail.com'

DISCLAIMER = '''[b]Disclaimer[/b]\n
The rewards exist only for cosmetic purposes, and have no real currency value.\n\n'''

NO_ENDORSEMENT_TEXT = ''

ABOUT_TEXT = '[b]{} licence[/b]\n\n'.format(main.APP_NAME)
ABOUT_TEXT += '[size=12]{}[/size]\n\n'.format(PROJECT_LICENCE)
ABOUT_TEXT += '[b]Contact me[/b]\n\n{}\n\n'.format(EMAIL)
ABOUT_TEXT += NO_ENDORSEMENT_TEXT
ABOUT_TEXT += DISCLAIMER
ABOUT_TEXT += '[b]Kivy licence[/b]\n\n'
ABOUT_TEXT += '[size=12]{}[/size]'.format(KIVY_LICENCE)

