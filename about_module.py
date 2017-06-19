import os

from main import APP_NAME


with open('LICENSE.txt') as _license_file:
    _PROJECT_LICENCE = _license_file.read()

LICENSES_DCT = {APP_NAME: _PROJECT_LICENCE}

OTHER_LICENSES_DIR = 'other_licenses'
for _p in os.listdir(OTHER_LICENSES_DIR):
    _file_path = os.path.join(OTHER_LICENSES_DIR, _p)
    with open(_file_path) as _license_file:
        _l = _license_file.read()
        _name = _p.replace('_license.txt', '').replace('_', '')
        LICENSES_DCT.update({_name: _l})


EMAIL = 'FermiParadoxSo@gmail.com'
_CONTACT_ME = '[b]Contact me:[/b]\n{}'.format(EMAIL)

_DISCLAIMER = '''[b]Disclaimer[/b]\n
The rewards exist only for cosmetic purposes, and have no real currency value.'''


ABOUT_TEXT = '\n\n'.join([_CONTACT_ME, _DISCLAIMER, ])

