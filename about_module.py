import os

from main import APP_NAME


with open('LICENSE.txt') as _license_file:
    PROJECT_LICENCE = _license_file.read()

LICENSES_DCT = {APP_NAME: PROJECT_LICENCE}

OTHER_LICENSES_DIR = 'other_licenses'
for p in os.listdir(OTHER_LICENSES_DIR):
    file_path = os.path.join(OTHER_LICENSES_DIR, p)
    with open(file_path) as _license_file:
        l = _license_file.read()
        name = p.replace('_license.txt', '').replace('_', '')
        LICENSES_DCT.update({name: l})


EMAIL = 'FermiParadoxSo@gmail.com'
CONTACT_ME = '[b]Contact me:[/b]\n{}'.format(EMAIL)

DISCLAIMER = '''[b]Disclaimer[/b]\n
The rewards exist only for cosmetic purposes, and have no real currency value.'''


ABOUT_TEXT = '\n\n'.join([CONTACT_ME, DISCLAIMER, ])

