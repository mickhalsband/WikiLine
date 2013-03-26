import sys

class TimelineWriter:
#	_output = \
#"""<?xml version="1.0" encoding="utf-8"?>
#<timeline>
#	<version>0.19.0</version>
#	<categories>
#		<category>
#			<name>Test</name>
#			<color>255,0,0</color>
#			<font_color>0,0,0</font_color>
#		</category>
#	</categories>
#	<events>
#		<event>
#			<start>2012-7-4 13:20:0</start>
#			<end>2012-7-4 13:20:0</end>
#			<text>Test</text>
#			<fuzzy>False</fuzzy>
#			<locked>False</locked>
#			<ends_today>False</ends_today>
#			<category>Test</category>
#		</event>
#	</events>
#	<view>
#		<displayed_period>
#			<start>2012-6-5 13:20:34</start>
#			<end>2012-7-5 13:20:34</end>
#		</displayed_period>
#		<hidden_categories>
#		</hidden_categories>
#	</view>
#</timeline>"""

	def compose_xml(self, items):
		output = \
	"""<?xml version="1.0" encoding="utf-8"?>
	<timeline>
		<version>0.19.0</version>
		<categories>
			<category>
				<name>Timeline</name>
				<color>119,170,136</color>
				<font_color>0,0,0</font_color>
			</category>
		</categories>
		<events>
			<event>
				<start>{start_date} 13:20:0</start>
				<end>{end_date} 13:20:0</end>
				<text>{event_name}</text>
				<fuzzy>False</fuzzy>
				<locked>False</locked>
				<ends_today>False</ends_today>
				<category>Timeline</category>
			</event>
		</events>
		<view>
			<displayed_period>
				<start>1800-1-1 12:00:00</start>
				<end>2000-1-1 12:00:00</end>
			</displayed_period>
			<hidden_categories>
			</hidden_categories>
		</view>
	</timeline>""".format(	start_date = items[0].date,
							end_date = items[1].date,
							event_name = "Einstein")
		return output
		
	def write(self, items):
		output = self.compose_xml(items)
		print output
		with open("/Users/mick/timeline_test.timeline", "w") as f:
			f.write(output)

