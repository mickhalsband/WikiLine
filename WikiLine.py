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
			res = self.parse_class(tr)
			print str(res)
			
		#print "Born : " + self.find_born(vcard)
							
		return

	# should actually read the entire tr class
	# header is 'Born'
	# data is the birth date and place
	def parse_class(self, tr):
		states = enum(SEARCHING_HEADER=1, SEARCHING_DATA=2, DONE=3)
		state = states.SEARCHING_HEADER
		
		item = DataItem()
		
		#print "tr class : "# + str(tr)
		for elem in tr.getElementsByTagName("*"):
			#print "		elem : " + str(elem)
			if (state == states.SEARCHING_HEADER and \
				elem.nodeName == "th" and elem.firstChild != None and elem.firstChild.nodeValue != None):
				state = states.SEARCHING_DATA
				#print "		header : " + elem.firstChild.nodeValue.encode('utf-8')
				item.name = elem.firstChild.nodeValue.encode('utf-8')
				continue
				
			if (state == states.SEARCHING_DATA):
				#print "calling recurse"
				res = self.recurseNode(elem)
				ignoreChars = ["(","[","]"]
				if (res != None and res != "" and not res in ignoreChars):
					data = res.encode('utf-8')
					#print "		" + data
					if (re.search("\d\d\d\d\-\d\d\-\d\d", data) != None or \
						re.search("...-\d\d\-\d\d\d\d", data) != None):
						item.date = data
					else:
						item.location = data			
		
		return item
		
	# recurse a given node and return whatever valid data found
	def recurseNode(self, node):
		# end recursion
		if (node.nodeValue != None and node.nodeValue != ""):
			return node.nodeValue
		
		child = node.firstChild
		while (child != None and child.nodeType != 1):
			res = self.recurseNode(child)
			if (res != None):
				return res
			child = child.nextSibling
			
		return None

class VCardParser:
	infobox_vcard = "infobox vcard"

	def get_vcards(self, xmldoc):
		# find the infobox vcard
		vcards = (table for table in xmldoc.getElementsByTagName("table")\
				 if "class" in table.attributes.keys() and \
				table.attributes["class"].value == self.infobox_vcard)
		return vcards

class DataItem:
	def __repr__(self):
		return "{" + self.name + ":" + self.date + ":" + self.location + "}"
			
	def __init__(self):
		self.name = ""
		self.date = ""
		self.location = ""

def enum(**enums):
	return type('Enum', (), enums)

class Log:
	product_mode="release"

	def __init__(self):
		self.log_type = enum(INFO="INFO", DEBUG="DEBUG", WARNING="WARN", ERROR="ERROR")

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
