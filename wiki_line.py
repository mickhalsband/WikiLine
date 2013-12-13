import urllib2
import log
from wiki_parser import WikiParser
from timeline_writer import TimelineWriter
import ggl_map_drawer
#from geopy import geocoders

#from subprocess import call

log = log.Log()


class WikiLine:
    def __init__(self):
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [("User-agent", "Mozilla/5.0")]

    def read_article(self, url):
        print "reading url '%s'" % url
        infile = self.opener.open(url)
        page = infile.read()
        log.log_info("read page length: " + str(page.__len__()))
        log.log("page beings with: " + page[0:256])
#        xmldoc = minidom.parseString(page)
        #print ("xml length: " + str(xmldoc.__len__()))
        infile.close()
        return page

    def run(self, url):
        print "Running WikiLine..."
        page = self.read_article(url)
        dict = WikiParser(page).parse()

        for key, value in dict.items():
            print "{field}: {date}, {location}".format(field=key, date=value.date, location=value.location)

        timeline = TimelineWriter()
        timeline.write(dict)

        #query_string = "10900 Euclid Ave in Cleveland"
        query_string = "Princeton, New Jersey"
        #lat, lng = self.query_location(query_string)
        #self.compose_map_html(lat, lng)

    def query_location(self, query_string):
        g = geocoders.GoogleV3()
#        place, (lat, lng) = g.geocode(query_string)
#        print place
#        print (lat, lng)
        bounds = None
        region = None
        language = None
        sensor = False
        exactly_one = False
        place, (lat, lng) = g.geocode(query_string, bounds, region, language, sensor, exactly_one)

        print (lat, lng)
        return (lat, lng)

    def compose_map_html(self, lat, lng):
        map_html_filename = "/Users/mick/map.html"
        print "composing map to " + map_html_filename
        map_script = ggl_map_drawer.showmap(lat, lng)
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
        """.format(script=map_script)
        with open(map_html_filename, "w") as f:
            f.write(html_str)
