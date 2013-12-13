__author__ = 'mick'

import wiki_line
from subprocess import call
import sys

#this calls the "main" function when this script is executed
#"http://en.wikipedia.org/w/index.php?title=Albert_Einstein&printable=yes"
if __name__ == "__main__":
    url = "http://en.wikipedia.org/w/index.php?title=Albert_Einstein"
    if len(sys.argv) < 2:
        print "Usage: %s [url]" % sys.argv[0]
    else:
        print "arg[1] = %s" % sys.argv[1]
        url = sys.argv[1]

    print "Starting world..."

    wikiLine = wiki_line.WikiLine()
    wikiLine.run(url)

    call(["python", "/Users/mick/Development/externals/timeline-0.19.0/timeline.py", "/Users/mick/timeline_test.timeline"])