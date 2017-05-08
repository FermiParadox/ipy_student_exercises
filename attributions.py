"""Used for attributing all third party images.

An image could have several derivatives.
In that case all its derivatives have the same attribution.
"""
ACCEPTABLE_LICENSES = {'cc0', 'public domain', 'cc by'}

IMAGES_CITED = set()    # File names
FIRST_IMAGE_TO_CITATION_MAP = {}


class ImageCitation(object):
    """
    Used for attributing each individual work.
    Citation includes all related data along with extra requirements by the copyright owner.

    NOTE: Assumes the returned text will be displayed with markup enabled.
    """

    def __init__(self,
                 work_name,
                 creation_date,
                 licence,
                 adaptation,
                 nearly_identical_files,
                 creator_name=None, creator_pseudonym=None,
                 url='',
                 extra_text='',
                 ignore=False):
        """
        Takes all needed data for the attribution.
        Creator can be identified by either name or pseudonym.

        In case of a pseudonym, pseudonym related origin should be present.

        WARNING: In case of multiple files, start with original file
            since only the first image is displayed.

        :param work_name: (str)
        :param creator_name: (str)
        :param creator_pseudonym: (str) Pseudonym with pseudonym origin, e.g. "TallPony (wikipedia user)"
        :param creation_date: (str) Work creation date. e.g. 10-May-2015 (avoid displaying month as a number)
        :param url: (str)
        :param licence: (str) "cc0", "public domain" etc
        :param adaptation: (bool) Adapted (modified) or original work (refers to first file in file_names)
        :param nearly_identical_files: (list) File names derived (minor changes) from the work.
        :param extra_text: (str) Extra text required by the copyright owner.
        :param ignore: (bool) Used if attribution has been created but image is not included.
            Useful in case a previously discarded image is used again, in order to avoid creating 
            its attribution all over again.
        """
        if not (creator_name or creator_pseudonym):
            raise ValueError('At least one of `creator_name` and `creator_pseudonym` should be provided.')
        if creator_name and creator_pseudonym:
            raise ValueError('Only one of `creator_name` and `creator_pseudonym` should be provided.')
        if licence not in ACCEPTABLE_LICENSES:
            raise ValueError('Licence not acceptable')

        self.file_names = nearly_identical_files
        self.adaptation = adaptation
        self.licence = licence
        self.url = url
        self.creation_date = creation_date
        self.creator_name = creator_name
        self.creator_pseudonym = creator_pseudonym
        self._creator = creator_name or creator_pseudonym
        self.work_name = work_name
        self.extra_text = extra_text

        if not ignore:
            IMAGES_CITED.update(nearly_identical_files)
            FIRST_IMAGE_TO_CITATION_MAP.update({nearly_identical_files[0]: self})

    def full_text(self):
        """
        Final attribution text.

        NOTE: Assumes markup is done by "[b]", "[size=8]", etc.
        """
        final_text = ("[b]'{work_name}'[/b] image by {creator} ({creation_date}). "
                      "\n[size=10]{url}[/size]").format(work_name=self.work_name,
                                                        creator=self._creator,
                                                        creation_date=self.creation_date,
                                                        url=self.url)

        if self.adaptation:
            final_text = 'My adaptation of ' + final_text

        if self.extra_text:
            final_text += '\n' + self.extra_text

        return '[size=12]{}[/size]'.format(final_text)


# TEMPLATE
"""
 = ImageCitation(
    work_name=,
    creation_date=,
    licence=,
    adaptation=,
    nearly_identical_files=,
    creator_name=,
    creator_pseudonym=,
    url=,
    extra_text=)
"""

if __name__ == '__main__':
    print()
    print(GOLD_ZEUS_COIN.full_text())
