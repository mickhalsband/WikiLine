#import os
import sys
import urllib2
import re
from xml.dom import minidom

def enum(**enums):
	return type('Enum', (), enums)

log_type = enum(INFO="INFO", DEBUG="DEBUG", WARNING="WARN", ERROR="ERROR")
product_mode="release"
def do_log(type, str):
	print "***" + type + ": " + str



def log(str, type=None):
	if (type == log_type.WARNING or type == log_type.ERROR)\
	or (type == log_type.DEBUG and product_mode == "debug")\
	or (type == log_type.INFO):
		do_log(type,str)

class WikiLine:
	def __init__(self):
		self.opener = urllib2.build_opener()
		self.opener.addheaders = [("User-agent", "Mozilla/5.0")]

	def run(self, url):
		print "Running WikiLine..."
		xmldoc = self.read_article(url)
		self.parse_article(xmldoc)

	def read_article(self, url):
		print "reading url '%s'" %url
		infile = self.opener.open(url)
		page = infile.read()
		log("read page length: " + str(page.__len__()), log_type.INFO)
		log("page beings with: " + page[0:256])
		xmldoc = minidom.parseString(page)
		#print ("xml length: " + str(xmldoc.__len__()))
		infile.close()
		return xmldoc

	def parse_article(self, xmldoc):
		print "parsing XML"
		log("parse_article(" + str(self) + "," + str(xmldoc) + ")")
		for title in xmldoc.getElementsByTagName("title"):
			log("title is: " + title.firstChild.nodeValue, log_type.INFO)
		
		# find the infobox vcard
		infobox_vcard = "infobox vcard"
		vconf = (table for table in xmldoc.getElementsByTagName("table")\
				 if "class" in table.attributes.keys() and \
				table.attributes["class"].value == "infobox vcard")
				
		vcard_found = False
		for table in vconf:
			vcard_found = True
			log("table attributes: " + str(table.attributes.keys()))
			log("table class: " + table.attributes["class"].value)
			
			# find 'Born' values in vcard
			print "Born : " + self.find_born(table)
					
		if (not vcard_found):
			log("No " + infobox_vcard + " in page",log_type.ERROR)

		return

	# should actually read the entire tr class
	# header is 'Born'
	# data is the birth date and place
	def find_born(self, table):
		states = enum(LOOKING_FOR_TH=1, LOOKING_FOR_TR=2)
		state = states.LOOKING_FOR_TH
		for child in table.getElementsByTagName("*"):
			if (state == states.LOOKING_FOR_TH):
				#log(str(child),log_type.DEBUG)
				if (child.nodeName != "th"):
					# log("skipping nodeName: " + str(child.nodeName), log_type.DEBUG)
					continue
					
				if (child.firstChild.nodeValue != "Born"):
					continue
				log("found: " + str(child.firstChild.nodeValue), log_type.INFO)
				state = states.LOOKING_FOR_TR
				continue
				
			if (state == states.LOOKING_FOR_TR):
				if (child.nodeName != "td"):
					continue
				
				#log("child: " + str(child),log_type.INFO)
				#log("child firstChild " + str(child.firstChild),log_type.INFO)
				#log("child nodeValue: " + str(child.firstChild.nodeValue),log_type.INFO)
				
				if ("class" in child.firstChild.attributes.keys() \
				and child.firstChild.attributes["class"] != "bday"):
					continue

				log("THIS IS THE BIRDTHDAY MARKUP",log_type.INFO)

				for bday in child.getElementsByTagName("*"):
					#1879-03-14
					res = re.search("\d\d\d\d\-\d\d\-\d\d", bday.firstChild.nodeValue)
					if (res == None):
						continue
						
					return bday.firstChild.nodeValue
	
				return 0

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
