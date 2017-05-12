# Used for screenshots that match size of current screenshots in GooglePlay
if 1:
    from kivy.config import Config
    Config.set('graphics', 'width', '410')
    Config.set('graphics', 'height', '700')


import matplotlib
matplotlib.use("module://kivy.garden.matplotlib.backend_kivy")
from matplotlib import pyplot
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label as Label
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, BooleanProperty, ListProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock
from kivy.uix.carousel import Carousel
from kivy import platform


import arbitrary_pieces
import attributions
import exercises
import languages


__version__ = '0.0.1'

APP_NAME = 'Free edu'


# -----------------------------------------------------------------------------------------------
THIRD_PARTIES_IMAGES_DIR = 'third_parties_images'


# -----------------------------------------------------------------------------------------------
COLORS_TO_HEX_MAP = {
    'red': 'FF3232',
    'gold': 'FFAA00',
    'green': '00FF00',
    'blue': '1a1aff',
    'black': '000000'
}


def paint_text(text_str, color_str):
    """
    Adds markup around given text.
    Supports some colors by name instead of hexadecimal.

    :param text_str:
    :param color_str: (str) Hexadecimal or color name.
    :return: (str)
    """

    if color_str in COLORS_TO_HEX_MAP:
        color_str = COLORS_TO_HEX_MAP[color_str]

    return '[color={color_str}]{text_str}[/color]'.format(text_str=text_str,
                                                          color_str=color_str)


BACKGROUND_COLOR = .9,.9,1,1
BLACK_RGBA = 0,0,0,1
GREEN_RGBA = 0,1,0,1
BLUE_RGBA = 0,0,1,1
RED_RGBA = 1,0,0,1


def boldify(txt_str):
    return '[b]{}[/b]'.format(txt_str)


# -----------------------------------------------------------------------------------------------
class MyProgressBar(Widget):
    DEFAULT_FILLED_COLOR = 0,1,0,1
    DEFAULT_EMPTY_COLOR = 1,0,0,1
    filled_color = ListProperty(DEFAULT_FILLED_COLOR)
    empty_color = ListProperty(DEFAULT_EMPTY_COLOR)
    filled_ratio = NumericProperty(.01)
    empty_ratio = NumericProperty(.01)


# Class code below (including the corresponding in .kv file)
# by Alexander Taylor
# from https://github.com/kivy/kivy/wiki/Scrollable-Label
class ConfinedTextLabel(Label):
    pass


class ScrollLabel(ScrollView):
    pass


class AttributionsBox(BoxLayout):
    # TODO: Grid buttons need to maintain ratio, without resorting to fixed size.
    def __init__(self, **kwargs):
        super(AttributionsBox, self).__init__(orientation='vertical', **kwargs)
        self.add_widget(Label(text='Attributions', size_hint_y=.2, bold=True))
        self.grid = GridLayout(cols=3)
        self.add_widget(self.grid)
        self.populate_grid()
        self.popup = Popup(title='', size_hint=[.9, .7], separator_color=(0, 0, 0, 0))
        self.popup_image = Image(source='')
        self.popup_text_label = ScrollLabel(text='')
        box = BoxLayout(orientation='vertical')
        box.add_widget(self.popup_image)
        box.add_widget(self.popup_text_label)
        self.popup.add_widget(box)

    @staticmethod
    def image_path(im_name):
        return '/'.join([THIRD_PARTIES_IMAGES_DIR, im_name])

    def populate_grid(self):
        for im_name, citation_obj in attributions.FIRST_IMAGE_TO_CITATION_MAP.items():
            im_path = self.image_path(im_name=im_name)
            b = Button(background_normal=im_path, size_hint=(None, None), width='50sp', height='50sp', border=(0,0,0,0))
            b.image_name = im_name
            b.image_text = citation_obj.full_text()
            b.bind(on_release=self.update_popup_and_open)
            self.grid.add_widget(b)

    def update_popup_and_open(self, *args):
        im_name = args[0].image_name
        self.popup_image.source = self.image_path(im_name=im_name)
        self.popup_text_label.text = args[0].image_text
        self.popup.open()


class PaintedLabel(Label):
    pass


class VBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(VBoxLayout, self).__init__(orientation='vertical', **kwargs)


# -----------------------------------------------------------------------------------------------
_INITIAL_EXERCISE = exercises.SolveForXLinear(difficulty=2)


class LatexWidget(ScatterLayout):
    text = StringProperty('')

    def __init__(self, **kwargs):
        super(LatexWidget, self).__init__(
            do_rotation=False, do_translation=False,
            **kwargs)

    @staticmethod
    def latex_image(latex_str):
        fig, ax = pyplot.subplots()
        ax.axis('off')
        ax.text(0.5, 0.5, latex_str,
                size=15,
                horizontalalignment='center', verticalalignment='center',
                bbox={})
        return FigureCanvasKivyAgg(fig)

    def on_text(self, *args):
        if self.children:
            self.remove_widget(self.children[0])
        im = LatexWidget.latex_image(self.text)
        self.add_widget(im)


class LicensesWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(LicensesWidget, self).__init__(orientation='vertical', **kwargs)
        self.popup = Popup(size_hint=(.9, .7))
        self.popup_content = ScrollLabel()
        self.popup.add_widget(self.popup_content)
        self.populate_widg()

    def populate_widg(self):
        self.add_widget(Label(text=boldify('Licenses'), size_hint_y=None, height='40sp'))
        from about_module import LICENSES_DCT
        for _name, licence in LICENSES_DCT.items():
            name = _name.capitalize()
            b = Button(text=name, bold=True, size_hint_y=None, height='30sp', border=(0,0,0,0))
            b.popup_title = boldify(txt_str=name)
            b.license_txt = licence
            b.bind(on_release=self.on_button_release)
            self.add_widget(b)

    def on_button_release(self, *args):
        self.popup.title = args[0].popup_title
        self.popup_content.text = args[0].license_txt
        self.popup.open()


class AnswersInputBox(BoxLayout):
    exercise = ObjectProperty(_INITIAL_EXERCISE)
    answers_given = DictProperty()

    def __init__(self, **kwargs):
        super(AnswersInputBox, self).__init__(**kwargs)
        self.textinputs_box = BoxLayout(orientation='vertical', padding='3sp')
        self.textinputs_lst = []
        self.add_widget(self.textinputs_box)
        self.specials_buttons_box = BoxLayout(orientation='vertical', size_hint_x=.3)
        self.add_widget(self.specials_buttons_box)
        self.populate_textinputs_box()
        self.populate_specials_buttons_box()

    def set_input_text_to_answer(self, *args):
        obj = args[0]
        self.answers_given[obj.answer_name_] = obj.text

    def populate_textinputs_box(self, *args):
        self.textinputs_lst = []
        for a_key in self.exercise.expected_answers:
            label_text = '{}= '.format(a_key)
            single_text_box = BoxLayout(size_hint_y=None, height='30sp')
            single_text_box.add_widget(Label(text=label_text, size_hint_x=.2))
            txt_input = TextInput(hint_text=languages.TYPE_ANSWER_PROMPT_MSG, multiline=False)
            txt_input.answer_name_ = a_key
            txt_input.bind(text=self.set_input_text_to_answer)
            self.textinputs_lst.append(txt_input)
            single_text_box.add_widget(txt_input)
            self.textinputs_box.add_widget(single_text_box)

    def set_special_answer_to_answers(self, *args):
        obj = args[0]
        # (text must be changed first otherwise answers will change twice `on_text`)
        for i in self.textinputs_lst:
            i.text = ''
        for a in self.answers_given:
            self.answers_given[a] = obj.special_val_

    def populate_specials_buttons_box(self, *args):
        for a_class in self.exercise.special_answers_allowed:
            b = Button(text=a_class.button_text,
                       size_hint_y=None, height='30sp',
                       border=(0,0,0,0))
            b.special_val_ = a_class
            b.bind(on_release=self.set_special_answer_to_answers)
            self.specials_buttons_box.add_widget(b)

    def populate_everything(self, *args):
        self.populate_textinputs_box()
        self.populate_specials_buttons_box()

    def on_exercise(self, *args):
        self.populate_everything()


class RevealedAnswersBox(BoxLayout):
    expected_answers = ObjectProperty(_INITIAL_EXERCISE.expected_answers)

    def __init__(self, **kwargs):
        super(RevealedAnswersBox, self).__init__(**kwargs)
        self.main_content_box = BoxLayout()
        self.add_widget(self.main_content_box)
        self.set_main_label()

    def set_main_label(self, *args):
        special_found = set(arbitrary_pieces.SPECIAL_ANSWERS_TYPES) & set(self.expected_answers.values())
        if special_found:
            w = Label(text=list(special_found)[0].long_description)
        else:
            w = LatexWidget(text=self.all_answers_as_latex_str())
        self.main_content_box.clear_widgets()
        self.main_content_box.add_widget(w)

    def all_answers_as_latex_str(self):
        non_latex_s = ''
        for a_name in sorted(self.expected_answers):
            a_val = self.expected_answers[a_name]
            non_latex_s += '{}={}'.format(a_name, a_val)
        return '${}$'.format(non_latex_s)


class MainWidget(Carousel):
    exercise = ObjectProperty(_INITIAL_EXERCISE)

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)


class PreciousMathApp(App):
    def build(self):
        return MainWidget()


if __name__ == '__main__':

    try:
        import IGNORE_BUILD_ensure_images_cited
    except ImportError:
        pass

    PreciousMathApp().run()
