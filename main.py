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

# TODO find appropriate name
APP_NAME = 'Free edu'
STANDARD_BUTTON_HEIGHT = '30sp'

# -----------------------------------------------------------------------------------------------
THIRD_PARTIES_IMAGES_DIR = 'third_parties_images'


# -----------------------------------------------------------------------------------------------

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
# by Alexander Taylor (MIT license)
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
    def third_parties_image_path(im_name):
        return '/'.join([THIRD_PARTIES_IMAGES_DIR, im_name])

    def populate_grid(self):
        for im_name, citation_obj in attributions.FIRST_IMAGE_TO_CITATION_MAP.items():
            im_path = self.third_parties_image_path(im_name=im_name)
            b = Button(background_normal=im_path, size_hint=(None, None), width='50sp', height='50sp')
            b.image_name = im_name
            b.image_text = citation_obj.full_text()
            b.bind(on_release=self.update_popup_and_open)
            self.grid.add_widget(b)

    def update_popup_and_open(self, *args):
        im_name = args[0].image_name
        self.popup_image.source = self.third_parties_image_path(im_name=im_name)
        self.popup_text_label.text = args[0].image_text
        self.popup.open()


class PaintedLabel(Label):
    pass


class VBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(VBoxLayout, self).__init__(orientation='vertical', **kwargs)


# -----------------------------------------------------------------------------------------------
_INITIAL_EXERCISE = exercises.SolveForXLinear(difficulty=2)


class LatexWidget(BoxLayout):
    text = StringProperty('')

    def __init__(self, **kwargs):
        self.scatterlayout = ScatterLayout(do_rotation=False, do_translation_y=False)
        super(LatexWidget, self).__init__(**kwargs)
        self.add_widget(self.scatterlayout)

    @staticmethod
    def latex_image(latex_str):
        fig, ax = pyplot.subplots()
        ax.axis('off')
        ax.text(.5, .5, latex_str,
                size=20,
                horizontalalignment='center', verticalalignment='center',
                bbox={})
        return FigureCanvasKivyAgg(fig)

    def on_text(self, *args):
        if self.scatterlayout.children:
            self.remove_widget(self.scatterlayout.children[0])
        im = LatexWidget.latex_image(self.text)
        self.scatterlayout.add_widget(im)


class LicensesWidget(BoxLayout):
    POPUP_TITLE_SIZE = '20sp'

    def __init__(self, **kwargs):
        super(LicensesWidget, self).__init__(orientation='vertical', **kwargs)
        self.popup = Popup(size_hint=(.9, .7), title_size=self.POPUP_TITLE_SIZE)
        self.popup_content = ScrollLabel()
        self.popup.add_widget(self.popup_content)
        self.populate_widg()

    def populate_widg(self):
        self.add_widget(Label(text=boldify('Licenses'), font_size=self.POPUP_TITLE_SIZE, size_hint_y=None, height='40sp'))
        from about_module import LICENSES_DCT
        for _name, licence in LICENSES_DCT.items():
            name = _name.capitalize()
            b = Button(text=name, bold=True, size_hint_y=None, height=STANDARD_BUTTON_HEIGHT)
            b.popup_title = name
            b.license_txt = licence
            b.bind(on_release=self.on_button_release)
            self.add_widget(b)

    def on_button_release(self, btn):
        self.popup.title = boldify(txt_str=btn.popup_title)
        self.popup_content.text = btn.license_txt
        self.popup.open()


ANSWER_KEY_EQUALS = '{}='


class AnswersInputBox(BoxLayout):
    exercise = ObjectProperty()
    answers_given = DictProperty()

    def __init__(self, **kwargs):
        super(AnswersInputBox, self).__init__(**kwargs)
        self.textinputs_box = BoxLayout(orientation='vertical', padding='3sp')
        self.textinputs_lst = []
        self.add_widget(self.textinputs_box)
        self.specials_buttons_box = BoxLayout(orientation='vertical', size_hint_x=.3)
        self.add_widget(self.specials_buttons_box)
        Clock.schedule_once(self.populate_textinputs_box, .5)
        Clock.schedule_once(self.populate_specials_buttons_box, .5)

    def set_input_text_to_answer(self, *args):
        obj = args[0]
        self.answers_given[obj.answer_name] = obj.text

    def populate_textinputs_box(self, *args):
        self.textinputs_box.clear_widgets()
        self.textinputs_lst = []
        for answer_name in self.exercise.expected_answers:
            box = BoxLayout(size_hint_y=None, height=STANDARD_BUTTON_HEIGHT)
            self.textinputs_box.add_widget(box)

            label_text = ANSWER_KEY_EQUALS.format(answer_name)
            box.add_widget(Label(text=label_text, size_hint_x=.2))

            t_input = TextInput(hint_text=languages.TYPE_ANSWER_PROMPT_MSG, multiline=False)
            t_input.answer_name = answer_name
            t_input.bind(text=self.set_input_text_to_answer)
            box.add_widget(t_input)
            self.textinputs_lst.append(t_input)

    def set_special_answer_to_answers(self, *args):
        obj = args[0]
        # (text must be changed first otherwise answers will change twice `on_text`)
        for i in self.textinputs_lst:
            i.text = ''
        for a in self.answers_given:
            self.answers_given[a] = obj.special_val_

    def populate_specials_buttons_box(self, *args):
        self.specials_buttons_box.clear_widgets()
        for a_class in self.exercise.special_answers_allowed:
            b = Button(text=a_class.button_text,
                       size_hint_y=None, height=STANDARD_BUTTON_HEIGHT)
            b.special_val_ = a_class
            b.bind(on_release=self.set_special_answer_to_answers)
            self.specials_buttons_box.add_widget(b)

    def populate_everything(self, *args):
        self.populate_textinputs_box()
        self.populate_specials_buttons_box()

    def on_exercise(self, *args):
        self.populate_everything()


class UserReactionToRevealedAnswersBox(BoxLayout):
    pass


class RevealedAnswersBox(BoxLayout):
    expected_answers_in_latex = DictProperty({'x_placeholder': 'placeholder'})
    reveal_button = ObjectProperty()
    answers_input_box = ObjectProperty()
    check_answers_button = ObjectProperty()

    def __init__(self, **kwargs):
        super(RevealedAnswersBox, self).__init__(**kwargs)
        self.latex_widg = LatexWidget()
        self.special_answer_label = Label()
        self.main_content_box = BoxLayout(orientation='vertical')
        self.main_content_box.add_widget(Label(text=languages.CORRECT_ANSWER_IS_MSG))
        self.main_label_box = BoxLayout()
        self.main_content_box.add_widget(self.main_label_box)

        self.user_reaction_options_box = UserReactionToRevealedAnswersBox()
        self.user_reaction_options_box.ids.ok_button.bind(on_release=self.on_ok_button_release)
        self.main_content_box.add_widget(self.user_reaction_options_box)

    def _main_label(self):
        special_found = set(arbitrary_pieces.SPECIAL_ANSWERS_TYPES) & set(self.expected_answers_in_latex.values())
        if special_found:
            w = self.special_answer_label
            w.text = list(special_found)[0].long_description
        else:
            w = self.latex_widg
            w.text = self.all_answers_as_latex_str()
        return w

    def create_main_label(self, *args):
        self.main_label_box.clear_widgets()
        self.main_label_box.add_widget(self._main_label())

    def show_main_content(self, *args):
        self.clear_widgets()
        self.create_main_label()
        self.add_widget(self.main_content_box)

    def all_answers_as_latex_str(self):
        non_latex_s = ''
        for a_name in sorted(self.expected_answers_in_latex):
            a_val = self.expected_answers_in_latex[a_name]
            # (simply places "z=" at the start;
            # different type of answers would need different implementation elsewhere too)
            if non_latex_s:
                non_latex_s += ', '
            non_latex_s += ANSWER_KEY_EQUALS.format(a_name) + r'{}'.format(a_val.strip('$'))
        return '${}$'.format(non_latex_s)

    def on_ok_button_release(self, *args):
        self.clear_widgets()
        self.add_widget(Label())
        self.reveal_button.disabled = False
        self.check_answers_button.disabled = False
        self.answers_input_box.disabled = False
        app.root.exercise = exercises.SolveForXLinear(difficulty=2)


class MainWidget(Carousel):
    exercise = ObjectProperty()
    question_in_latex = ObjectProperty()

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

    app = PreciousMathApp()
    app.run()
