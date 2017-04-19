from ipywidgets import Layout, Button, HBox, VBox, Label, Text, Box

import languages


TYPE_ANSWER_PROMPT_MSG = languages.Message(
    texts_dct={
        languages.english: '(type the answer)',
        languages.greek: '(γράψε την απάντηση)',
    })

CHECK_MY_ANSWER_MSG = languages.Message(
    texts_dct={
        languages.english: 'Check my answer.',
        languages.greek: 'Έλεγξε απάντηση.',
    }
)


class QADisplayBox(object):
    pass


class FillGapsBox(QADisplayBox):
    Q_AND_A_WIDTH = '60%'

    def __init__(self, qa_obj):
        self.qa_obj = qa_obj
        self.expected_answer = self.qa_obj.answers
        self.special_answers_allowed = self.qa_obj.special_answers_allowed
        self.question_title = self.qa_obj.question_title
        self.question_in_latex = self.qa_obj.question_in_latex
        self.answer_given = ''

        self.check_answer_button = Button(description=CHECK_MY_ANSWER_MSG, layout=Layout(width='auto'))
        self.check_answer_button.style.button_color = '#5dfd57'

    @staticmethod
    def _special_answers_buttons_box(special_answers_allowed):
        buttons_lst = []
        for a_class in special_answers_allowed:
            b = Button(description=a_class.button_text, )
            b.style.button_color = '#d6d6d6'
            buttons_lst.append(b)
        return VBox(buttons_lst)

    def _answers_inputs_box(self, answer, special_answers_allowed):
        # Text-inputs
        texts_widgets_lst = []
        for a_key in answer:
            label_text = '{}= '.format(a_key)
            single_text_box = HBox([
                Label(label_text, layout=Layout(width='auto')),
                Text(placeholder=TYPE_ANSWER_PROMPT_MSG, layout=Layout(width='auto'))])
            texts_widgets_lst.append(single_text_box)
        texts_widgets_box = Box(texts_widgets_lst)

        return VBox(
            [
                HBox(
                    [texts_widgets_box,
                     FillGapsBox._special_answers_buttons_box(special_answers_allowed=special_answers_allowed),
                     Button(description='?', layout=Layout(width='40px'))]
                ),
                self.check_answer_button,
            ], layout=Layout(border='thin solid grey', width=FillGapsBox.Q_AND_A_WIDTH)
        )

    @staticmethod
    def q_box(q_title, q_in_latex):
        return VBox([
            Label(q_title, layout=Layout(width='auto')),
            Label(q_in_latex, layout=Layout(width='auto'))],
            layout=Layout(border='thin solid grey', width=FillGapsBox.Q_AND_A_WIDTH))

    def box(self):
        textinputs_box = self._answers_inputs_box(answer=self.expected_answer,
                                                  special_answers_allowed=self.special_answers_allowed)
        box_layout = Layout(display='flex',
                            flex_flow='column',
                            align_items='stretch',
                            border='solid',
                            width='70%')
        items = [
            FillGapsBox.q_box(q_title=self.question_title, q_in_latex=self.question_in_latex),
            textinputs_box
        ]

        return VBox(children=items, layout=box_layout)
