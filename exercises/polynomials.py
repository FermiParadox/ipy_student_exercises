import main
import languages

from ipywidgets import Layout, Button, HBox, VBox, Label, Text
from IPython.display import display

# TODO: Rename dir+file,
# TODO: create input-class that automatically takes SolveForX-type of classes
# and creates input fields etc, checks correct answer and displays feedback.

TYPE_AND_ENTER_PROMPT = languages.Message(
    texts_dct={
        languages.english: '(type the answer and press enter)',
        languages.greek: '(γράψε την απάντηση και πάτα enter)',
    })


def solve_for_x():
    inst = main.SolveForXLinear(3)
    q = inst.question

    text_box = HBox([Label('x= '), Text(placeholder=TYPE_AND_ENTER_PROMPT)])
    box_layout = Layout(display='flex',
                        flex_flow='column',
                        align_items='stretch',
                        border='solid',
                        width='50%')
    items = [
        Label(inst.question_title),
        Label('${}$'.format(q.replace('*', ''))),
        text_box
    ]

    q_box = VBox(children=items, layout=box_layout)
    display(q_box)
