from nose.tools import raises, with_setup, eq_

from turbine.stream import Stream

class TestStream():

	TEST_USERNAME = 'example'
	TEST_PASSWORD = 'example'

	def setup(self):
		def callback(x):
			pass

		self.stream = Stream(consumer=callback, username=self.TEST_USERNAME, password=self.TEST_PASSWORD)

	@raises(Exception)
	@with_setup(None, None)
	def test_invalid_consumer(self):
		callback = set()

		Stream(consumer=callback, username=self.TEST_USERNAME, password=self.TEST_PASSWORD)

	@with_setup(None, None)
	def test_consumer(self):
		def callback(x):
			pass

		stream = Stream(consumer=callback, username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
		
		assert stream

	def test_reset(self):
		self.stream.reset()

		eq_([], self.stream.keywords)
		eq_([], self.stream.locations)
		eq_([], self.stream.usernames)

	def test_filter_keywords_list(self):
		words = ['a', 'list', 'of', 'keywords']

		self.stream.filter_keywords(words)

		eq_(words, self.stream.keywords)

	def test_filter_keywords_string(self):
		self.stream.filter_keywords('a keyword')

		eq_(['a keyword'], self.stream.keywords)

	def test_append_keywords(self):
		words = ['a', 'list', 'of', 'keywords']

		self.stream.filter_keywords(words[:2])

		eq_(['a', 'list'], self.stream.keywords)

		self.stream.filter_keywords(words[2:4])

		eq_(words, self.stream.keywords)

	def test_filter_locations(self):
		locations = [(1, 2, 3, 4)]

		self.stream.filter_locations(locations)

		eq_(locations, self.stream.locations)

	@raises(Exception)
	def test_filter_invalid_locations(self):
		self.stream.filter_locations([1, 2, 3, 4])