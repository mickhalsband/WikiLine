#import os
import urllib2
from xml.dom import minidom

def debug(str):
    print "***" + str

class WikiLine:
    def __init__(self):
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    def run(self):
        print "Running WikiLine..."
        xmldoc = self.read_article("http://en.wikipedia.org/w/index.php?title=Albert_Einstein&printable=yes")
        self.parse_article(xmldoc)

    def read_article(self, url):
        infile = self.opener.open(url)
        page = infile.read()
        print "***page length: " + str(page.__len__())
        print "***page beings with: " + page[0:256]
        xmldoc = minidom.parseString(page)
        #print ("xml length: " + str(xmldoc.__len__()))
        infile.close()
        return xmldoc

    def parse_article(self, xmldoc):
        debug("parse_article(" + str(self) + "," + str(xmldoc) + ")")
        title = xmldoc.getElementsByTagName('title')

        for e in title:
            print e
            #print e.Value
            if e.attributes.__len__() > 0:
                for attr in e.attributes:
                    print attr
            else:
                print "no attributes for " + str(e)

        #debug("title is '" + title[0].attributes['name'].value + "'")

        tag = 'th'
        itemlist = xmldoc.getElementsByTagName(tag)
        debug ("itemlist length: " + str(len(itemlist)))
                    
        debug ("iterating elements by tag '" + tag + "'")
        for e in itemlist[0:1] :
            print "element is: " + str(e)
            print "element attributes: " + str(e.attributes)
#          print s.attributes['name'].value

        #print xmldoc.toxml()

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    print "Starting world..."
    wikiLine = WikiLine()
    wikiLine.run()
