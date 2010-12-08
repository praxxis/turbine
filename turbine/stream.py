from urlparse import urljoin
from urllib import urlencode
from cStringIO import StringIO

import pycurl

class Stream(object):
	"""A simple twitter stream connection.
	"""

	PACKET_TERMINATOR = "\r\n"

	BASE_URL = 'http://stream.twitter.com/1/'

	def __init__(self, username, password, consumer):
		"""Create a stream instance that will connect to the Twitter API
		with the specified username and password. The callable callback will be
		invoked on each JSON message sent by the API.
		"""
		
		if not callable(consumer):
			raise Exception('Consumer must be callable')
		
		self.consumer = consumer

		self.curl = pycurl.Curl()

		self.curl.setopt(pycurl.USERPWD, '%s:%s' % (username, password))
		self.curl.setopt(pycurl.WRITEFUNCTION, self._receive)

		self.reset()

	def reset(self):
		"""Reset filters back to empty
		"""
		self.keywords = []
		self.locations = []
		self.usernames = []

		self._reset_buffer()

	def _reset_buffer(self):
		self.buffer = StringIO()

	def _receive(self, data):
		self.buffer.write(data)

		if data.endswith(self.PACKET_TERMINATOR):
			payload = self.buffer.getvalue().strip()

			if payload:
				self.consumer(payload)

			self._reset_buffer()

	def launch(self, path, parameters=None):
		"""Initiate a connection to the specified Twitter stream.
		"""
		self.curl.setopt(pycurl.URL, urljoin(self.BASE_URL, path))

		if parameters:
			# default to POST to make sure large parameter lists always work
			self.curl.setopt(pycurl.POST, True)
			self.curl.setopt(pycurl.POSTFIELDS, urlencode(parameters))

		self.curl.perform()

	def filter(self):
		"""Connect to the Twitter firehose. Specify locations, keywords or usernames
		to track before connecting.
		"""
		parameters = {}

		if self.keywords:
			parameters['track'] = ','.join(self.keywords)

		if self.locations:
			parameters['locations'] = ','.join([','.join([str(latlong) for latlong in loc]) for loc in self.locations])

		if self.usernames:
			parameters['follow'] = ','.join([str(u) for u in self.usernames])

		self.launch('statuses/filter.json', parameters)

	def sample(self):
		"""Launch an unfiltered sample of the streaming API.
		"""
		self.launch('statuses/sample.json')

	def filter_keywords(self, keywords):
		"""Filter the Twitter stream based on a list of keywords.
		"""
		self.keywords += self._coerce_list(keywords)

	def filter_usernames(self, usernames):
		"""Track a list of usernames.
		"""
		self.usernames += self._coerce_list(usernames)

	def filter_locations(self, locations):
		"""Filter the streaming API based on a list of locations. Locations are specified
		by a bounding box, specified by a tuple of longitude/latitude pairs.
		"""
		if not isinstance(locations, list):
			raise Exception('Locations needs to be a list of 4tuples')

		for location in locations:
			if not isinstance(location, tuple) or len(location) != 4:
				raise Exception('Locations needs to be a list of 4tuples')

		self.locations += locations

	def _coerce_list(self, thing):
		"""Coerce a string in to a single item list.
		"""
		if isinstance(thing, basestring):
			return list((thing,))

		return list(thing)