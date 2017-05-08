import sys

import matplotlib
matplotlib.use("module://kivy.garden.matplotlib.backend_kivy")
from matplotlib import pyplot
from matplotlib.text import Text

from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.properties import StringProperty


class A(App):

    mathtext = StringProperty(r"$x^2+\frac{2}{4}=12$")

    def build(self):
        fig = pyplot.figure()

        ax = pyplot.gca()
        ax.axis('off')
        text = ax.text(0.5, 0.5, self.mathtext, horizontalalignment='center', verticalalignment='center',
                       bbox={'facecolor': 'wheat'})

        renderer = FigureCanvasKivyAgg(fig)
        s = Scatter()
        s.add_widget(Image(source=renderer))
        return s

if __name__ == "__main__":
    A().run()

