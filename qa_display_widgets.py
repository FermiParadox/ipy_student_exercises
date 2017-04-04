from ipywidgets import Layout, Button, HBox, VBox, Label, Text, Box

import languages
import arbitrary_pieces


TYPE_ANSWER_PROMPT = languages.Message(
    texts_dct={
        languages.english: '(type the answer)',
        languages.greek: '(γράψε την απάντηση)',
    })


class QADisplayBox(object):
    pass


class FillGapsBox(QADisplayBox):
    def __init__(self, qa_obj):
        self.qa_obj = qa_obj

    @staticmethod
    def _special_answers_buttons_box(answer_types):
        buttons_lst = []
        for a_type in answer_types:
            if issubclass(a_type, arbitrary_pieces.SpecialAnswerType):
                b = Button(description=arbitrary_pieces.AnyNumber.button_text)
                buttons_lst.append(b)
        return VBox(buttons_lst)

    @staticmethod
    def _answers_inputs_box(answer, answer_types):
        # Text-inputs
        texts_widgets_lst = []
        for a_key in answer:
            label_text = '{}= '.format(a_key)
            single_text_box = HBox([
                Label(label_text),
                Text(placeholder=TYPE_ANSWER_PROMPT, layout=Layout(width='auto'))])
            texts_widgets_lst.append(single_text_box)
        texts_widgets_box = Box(texts_widgets_lst)

        return VBox(
            [
                HBox(
                    [texts_widgets_box,
                     FillGapsBox._special_answers_buttons_box(answer_types=answer_types),
                     Button(description='?', layout=Layout(width='40px'))]
                ),
                Button(description='Check my answer.', layout=Layout(width='auto'))
            ],
        )

    def box(self):
        text_box = FillGapsBox._answers_inputs_box(answer=self.qa_obj.answer,
                                                   answer_types=self.qa_obj.answer_types)
        box_layout = Layout(display='flex',
                            flex_flow='column',
                            align_items='stretch',
                            border='solid',
                            width='70%')
        items = [
            Label(self.qa_obj.question_title),
            Label(self.qa_obj.question_in_latex),
            text_box
        ]

        return VBox(children=items, layout=box_layout)
