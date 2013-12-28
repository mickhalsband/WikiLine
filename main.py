__author__ = 'mick'

import wiki_line
from subprocess import call
import sys
import kivy

kivy.require('1.0.7')

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty

import KVMaps

class Controller(FloatLayout):
    """
    this calls the "main" function when this script is executed
    "http://en.wikipedia.org/w/index.php?title=Albert_Einstein&printable=yes"
    Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    """

    url = ""
    label_wid = ObjectProperty()
    info = StringProperty()

    def __init__(self, url, **kwargs):
        super(Controller, self).__init__(**kwargs)
        self.url = url

    def do_action(self):
        self.label_wid.text = 'running wikiline'
        self.info = 'New info text'
        self.do_stuff()

    def do_stuff(self):
        print "Starting world..."

        wikiLine = wiki_line.WikiLine()
        wikiLine.run(self.url)

        call(["python", "/Users/mick/Development/externals/timeline-0.19.0/timeline.py", "/Users/mick/timeline_test.timeline"])
        print 'done'

class ControllerApp(App):
    def __init__(self, url, **kwargs):
        super(ControllerApp, self).__init__(**kwargs)
        self.url = url

    def build(self):
        return Controller(self.url)


def main():
    url = "http://en.wikipedia.org/w/index.php?title=Albert_Einstein"
    if len(sys.argv) < 2:
        print "Usage: %s [url]" % sys.argv[0]
    else:
        print "arg[1] = %s" % sys.argv[1]
        url = sys.argv[1]

    ControllerApp(url).run()

if __name__ == '__main__':
    # main()
    KVMaps.KVMaps().run()