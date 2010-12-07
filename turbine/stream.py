from urlparse import urljoin
from urllib import urlencode
from cStringIO import StringIO

import pycurl

class Stream(object):

	PACKET_TERMINATOR = "\r\n"

	BASE_URL = 'http://stream.twitter.com/1/'

	def __init__(self, username, password, consumer):

		if not callable(consumer):
			raise Exception('Consumer must be callable')
		
		self.consumer = consumer

		self.curl = pycurl.Curl()

		self.curl.setopt(pycurl.USERPWD, '%s:%s' % (username, password))
		self.curl.setopt(pycurl.WRITEFUNCTION, self._receive)

		self.reset()

	def reset(self):
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
		self.curl.setopt(pycurl.URL, urljoin(self.BASE_URL, path))

		if parameters:
			self.curl.setopt(pycurl.POST, True)
			self.curl.setopt(pycurl.POSTFIELDS, urlencode(parameters))
		print urlencode(parameters)
		self.curl.perform()

	def filter(self):

		parameters = {}

		if self.keywords:
			parameters['track'] = ','.join(self.keywords)

		if self.locations:
			parameters['locations'] = ','.join([','.join([str(latlong) for latlong in loc]) for loc in self.locations])

		if self.usernames:
			parameters['follow'] = ','.join([str(u) for u in self.usernames])

		self.launch('statuses/filter.json', parameters)

	def sample(self):
		self.launch('statuses/sample.json')

	def filter_keywords(self, keywords):
		self.keywords += self._coerce_list(keywords)

	def filter_usernames(self, usernames):
		self.usernames += self._coerce_list(usernames)

	def filter_locations(self, locations):
		if not isinstance(locations, list):
			raise Exception('Locations needs to be a list of 4tuples')

		for location in locations:
			if not isinstance(location, tuple) or len(location) != 4:
				raise Exception('Locations needs to be a list of 4tuples')

		self.locations += locations

	def _coerce_list(self, thing):
		if isinstance(thing, basestring):
			return list((thing,))

		return list(thing)