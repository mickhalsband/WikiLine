__author__ = 'mick'

import wiki_line
from subprocess import call
import sys
import kivy
kivy.require('1.0.7')

from kivy.app import App


class TestApp(App):
    url = ""
    """
    this calls the "main" function when this script is executed
    "http://en.wikipedia.org/w/index.php?title=Albert_Einstein&printable=yes"
    """

    def __init__(self, url, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.url = url

    def do_stuff(self):
        # print "Starting world..."

        # wikiLine = wiki_line.WikiLine()
        # wikiLine.run(url)
        #
        # call(["python", "/Users/mick/Development/externals/timeline-0.19.0/timeline.py", "/Users/mick/timeline_test.timeline"])
        print 'now in do stuff'
        pass

if __name__ == '__main__':
    url = "http://en.wikipedia.org/w/index.php?title=Albert_Einstein"
    if len(sys.argv) < 2:
        print "Usage: %s [url]" % sys.argv[0]
    else:
        print "arg[1] = %s" % sys.argv[1]
        url = sys.argv[1]

    TestApp(url).run()