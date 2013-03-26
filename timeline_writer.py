import sys

class TimelineWriter:

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
			{event}
		</events>
		<view>
			<displayed_period>
				<start>1800-1-1 12:00:00</start>
				<end>2000-1-1 12:00:00</end>
			</displayed_period>
			<hidden_categories>
			</hidden_categories>
		</view>
	</timeline>""".format(event = self.compose_event(items))
	
		return output

	def compose_event(self, items):
		return \
		"""<event>
			<start>{start_date} 13:20:0</start>
			<end>{end_date} 13:20:0</end>
			<text>{event_name}</text>
			<fuzzy>True</fuzzy>
			<locked>False</locked>
			<ends_today>False</ends_today>
			<category>Timeline</category>
		</event>""".format(	start_date = items["Born"].date,
							end_date = items["Died"].date,
							event_name = "Einstein")

	def write(self, items):
		output = self.compose_xml(items)
		print output
		with open("/Users/mick/timeline_test.timeline", "w") as f:
			f.write(output)

