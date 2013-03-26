#import os
import sys
import urllib2
import re
from xml.dom import minidom
import log

#def enum(**enums):
#	return type('Enum', (), enums)
#
#log_type = enum(INFO="INFO", DEBUG="DEBUG", WARNING="WARN", ERROR="ERROR")
#product_mode="release"
#def do_log(type, str):
#	print "***" + type + ": " + str
#
#def log(str, type=None):
#	if (type == log_type.WARNING or type == log_type.ERROR)\
#	or (type == log_type.DEBUG and product_mode == "debug")\
#	or (type == log_type.INFO):
#		do_log(type,str)
#
#def log_info(str):
#	log(str, log_type.INFO)

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
		log.log_info("read page length: " + str(page.__len__()))
		log.log("page beings with: " + page[0:256])
		xmldoc = minidom.parseString(page)
		#print ("xml length: " + str(xmldoc.__len__()))
		infile.close()
		return xmldoc

	def parse_article(self, xmldoc):
		print "parsing XML"
		log.log("parse_article(" + str(self) + "," + str(xmldoc) + ")")
		for title in xmldoc.getElementsByTagName("title"):
			log.log_info("title is: " + title.firstChild.nodeValue)
		
		# TODO: should assert only one vcard or something, i guess...
		vcard = VCardParser().get_vcards(xmldoc).next()

		# find 'Born' values in vcard
		print "Calling 'parse_class'"
		for tr in vcard.getElementsByTagName("tr"):
			 self.parse_class(tr)

		#print "Born : " + self.find_born(vcard)
							
		return

	# should actually read the entire tr class
	# header is 'Born'
	# data is the birth date and place
	def parse_class(self, tr):
		print "tr class : "# + str(tr)
		for elem in tr.getElementsByTagName("*"):
			#print "		elem : " + str(elem)
			if (elem.nodeName == "th" and elem.firstChild != None and elem.firstChild.nodeValue != None):
				print "		header : " + elem.firstChild.nodeValue.encode('utf-8')

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
				log.log_info("found: " + str(child.firstChild.nodeValue))
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

				log.log_info("THIS IS THE BIRDTHDAY MARKUP")

				for bday in child.getElementsByTagName("*"):
					#1879-03-14
					res = re.search("\d\d\d\d\-\d\d\-\d\d", bday.firstChild.nodeValue)
					if (res == None):
						continue
						
					return bday.firstChild.nodeValue
	
				return 0

class VCardParser:
	infobox_vcard = "infobox vcard"

	def get_vcards(self, xmldoc):
		# find the infobox vcard
		vcards = (table for table in xmldoc.getElementsByTagName("table")\
				 if "class" in table.attributes.keys() and \
				table.attributes["class"].value == self.infobox_vcard)
		return vcards


class Log:
	product_mode="release"

	def __init__(self):
		self.log_type = self.enum(INFO="INFO", DEBUG="DEBUG", WARNING="WARN", ERROR="ERROR")

	def enum(self,**enums):
		return type('Enum', (), enums)

	def do_log(self,type, str):
		print "***" + type + ": " + str

	def log(self, str, type=None):
		if (type == self.log_type.WARNING or type == self.log_type.ERROR)\
		or (type == self.log_type.DEBUG and product_mode == "debug")\
		or (type == self.log_type.INFO):
			self.do_log(type,str)

	def log_info(self, str):
		self.log(str, self.log_type.INFO)

#this calls the "main" function when this script is executed
#"http://en.wikipedia.org/w/index.php?title=Albert_Einstein&printable=yes"
if __name__ == "__main__":
	url = "http://en.wikipedia.org/w/index.php?title=Albert_Einstein&printable=yes"
	if len(sys.argv) < 2:
		sys.exit("Usage: %s [url]" % sys.argv[0])

	log = Log()
	url = sys.argv[1]
	
	print "Starting world..."

	print "	 arg[1] = %s" %sys.argv[1]

	wikiLine = WikiLine()
	wikiLine.run(url)
