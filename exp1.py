# This is *not* under MIT; it's used for testing and might contain proprietary code

import sys

import matplotlib
matplotlib.use("module://kivy.garden.matplotlib.backend_kivy")
from matplotlib import pyplot
from matplotlib.text import Text
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.button import Button as Button
from kivy.animation import Animation
from kivy.uix.label import Label as Label
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, BooleanProperty, ListProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock
from kivy.uix.carousel import Carousel
from kivy import platform
from kivy.event import EventDispatcher
from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image


from functools import partial
import abc
import os


kv = """
<MainWidget>

"""
Builder.load_string(kv)


class MyApp(App):
    def build(self):
        return Button()

if __name__ == "__main__":
    MyApp().run()

