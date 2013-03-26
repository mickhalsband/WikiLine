from xml.dom import minidom
import log
import utils
import re

log = log.Log()

class DataItem:
	def __repr__(self):
		return "{" + self.name + ":" + self.date + ":" + self.location + "}"
			
	def __init__(self):
		self.name = ""
		self.date = ""
		self.location = ""

class WikiParser:
	def __init__(self, page):
		self.xmldoc = minidom.parseString(page)

	def parse(self):
		print "parsing XML"
		log.log("parse_article(" + str(self) + "," + str(self.xmldoc) + ")")
		for title in self.xmldoc.getElementsByTagName("title"):
			log.log_info("title is: " + title.firstChild.nodeValue)
		
		# TODO: should assert only one vcard or something, i guess...
		vcard = self.get_vcards(self.xmldoc).next()

		# find 'Born' values in vcard
		print "Calling 'parse_class'"
		items = []
		itemsOfIterest = ["Born", "Died"]
		for tr in vcard.getElementsByTagName("tr"):
			item = self.parse_class(tr)
			if (item.name in itemsOfIterest):
				items.append(item)
				
		return items

	def get_vcards(self, xmldoc):
		infobox_vcard = "infobox vcard"
		# find the infobox vcard
		vcards = (table for table in xmldoc.getElementsByTagName("table")\
				 if "class" in table.attributes.keys() and \
				table.attributes["class"].value == infobox_vcard)
		return vcards

	# should actually read the entire tr class
	# header is 'Born'
	# data is the birth date and place
	def parse_class(self, tr):
		states = utils.enum(SEARCHING_HEADER=1, SEARCHING_DATA=2, DONE=3)
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
