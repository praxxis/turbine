from turbine.stream import Stream
from turbine.consumers import JSONConsumer
import pprint

USERNAME = ''
PASSWORD = ''

class Consumer(JSONConsumer):
	def on_status(self, status):
		pprint.pprint(status)

consumer = Consumer()

stream = Stream(USERNAME, PASSWORD, consumer)

stream.filter_keywords(['python'])
stream.filter_locations([(140.999283, -37.505032, 159.278717, -28.157021)])

stream.filter()