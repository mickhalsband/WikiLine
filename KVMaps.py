__author__ = 'mick'

import sys

import kivy

kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

sys.path.append('../kivyMaps/')
from MapViewer import MapViewer


class KVMaps(App):
    def __init__(self, **kwargs):
        super(KVMaps, self).__init__(**kwargs)
        self.mv = MapViewer(maptype="Roadmap", provider="openstreetmap")

    def build(self):
        layout = FloatLayout()
        layout.add_widget(self.mv)
        return layout