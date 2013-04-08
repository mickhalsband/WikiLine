import os
import urllib2
import utils
import log
import sys
from wiki_parser import WikiParser
from timeline_writer import TimelineWriter
import ggl_map_drawer

from subprocess import call

log = log.Log()

class WikiLine:
	def __init__(self):
		self.opener = urllib2.build_opener()
		self.opener.addheaders = [("User-agent", "Mozilla/5.0")]

	def read_article(self, url):
		print "reading url '%s'" %url
		infile = self.opener.open(url)
		page = infile.read()
		log.log_info("read page length: " + str(page.__len__()))
		log.log("page beings with: " + page[0:256])
#		xmldoc = minidom.parseString(page)
		#print ("xml length: " + str(xmldoc.__len__()))
		infile.close()
		return page
		
	def run(self, url):
		print "Running WikiLine..."
		page = self.read_article(url)
		dict = WikiParser(page).parse()

		for key, value in dict.items():
			print "{field}: {date}, {location}".format(field = key, date = value.date, location = value.location)

		timeline = TimelineWriter()
		timeline.write(dict)
		self.compose_map_html()

	def compose_map_html(self):
		map_html_filename = "/Users/mick/map.html"
		print "composing map to " + map_html_filename
		map_script = ggl_map_drawer.showmap()
		html_str = """
		<html>
			<head>
				<title>The Title</title>
			</head>
			<body onload="load()" onunload="GUnload()">
				<div id="map" style="width: 760px; height: 460px">{script}</div>
				<div id="blurb" style="width: 760px; height: 460px">blurb</div>
			</body>
		</html>
		""".format(	script = map_script)
		with open(map_html_filename, "w") as f:
			f.write(html_str)

#this calls the "main" function when this script is executed
#"http://en.wikipedia.org/w/index.php?title=Albert_Einstein&printable=yes"
if __name__ == "__main__":
	url = "http://en.wikipedia.org/w/index.php?title=Albert_Einstein&printable=yes"
	if len(sys.argv) < 2:
		sys.exit("Usage: %s [url]" % sys.argv[0])

	url = sys.argv[1]
	
	print "Starting world..."

	print "	 arg[1] = %s" %sys.argv[1]

	wikiLine = WikiLine()
	wikiLine.run(url)
