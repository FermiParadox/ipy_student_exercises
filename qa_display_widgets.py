from ipywidgets import Layout, Button, HBox, VBox, Label, Text, Box

import languages
import arbitrary_pieces


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
        self.answer = self.qa_obj.answer
        self.answer_types = self.qa_obj.answer_types
        self.question_title = self.qa_obj.question_title
        self.question_in_latex = self.qa_obj.question_in_latex
        self.answer_given = ''

    @staticmethod
    def _special_answers_buttons_box(answer_types):
        buttons_lst = []
        for a_class in answer_types:
            if issubclass(a_class, arbitrary_pieces.SpecialAnswerType):
                b = Button(description=a_class.button_text, )
                b.style.button_color = '#d6d6d6'
                buttons_lst.append(b)
        return VBox(buttons_lst)

    @staticmethod
    def _answers_inputs_box(answer, answer_types):
        # Text-inputs
        texts_widgets_lst = []
        for a_key in answer:
            label_text = '{}= '.format(a_key)
            single_text_box = HBox([
                Label(label_text, layout=Layout(width='auto')),
                Text(placeholder=TYPE_ANSWER_PROMPT_MSG, layout=Layout(width='auto'))])
            texts_widgets_lst.append(single_text_box)
        texts_widgets_box = Box(texts_widgets_lst)
        check_ans_button = Button(description=CHECK_MY_ANSWER_MSG, layout=Layout(width='auto'))
        check_ans_button.style.button_color = '#5dfd57'
        return VBox(
            [
                HBox(
                    [texts_widgets_box,
                     FillGapsBox._special_answers_buttons_box(answer_types=answer_types),
                     Button(description='?', layout=Layout(width='40px'))]
                ),
                check_ans_button,
            ], layout=Layout(border='thin solid grey', width=FillGapsBox.Q_AND_A_WIDTH)
        )

    @staticmethod
    def q_box(q_title, q_in_latex):
        return VBox([
            Label(q_title, layout=Layout(width='auto')),
            Label(q_in_latex, layout=Layout(width='auto'))],
            layout=Layout(border='thin solid grey', width=FillGapsBox.Q_AND_A_WIDTH))

    def box(self):
        textinputs_box = FillGapsBox._answers_inputs_box(answer=self.answer,
                                                         answer_types=self.answer_types)
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
