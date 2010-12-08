import json

class BaseConsumer(object):
	def __call__(self, paylod):
		pass
	
	def on_json(self, json_data):
		pass

class JSONConsumer(BaseConsumer):

	def __call__(self, payload):
		try:
			json_data = json.loads(payload)
		except Exception, e:
			raise Exception('Failed to parse JSON payload: %s' % e)

		self.on_json(json_data)

	def on_json(self, json_data):
		if json_data.has_key('text'):
			self.on_status(json_data)
		elif json_data.has_key('delete'):
			self.on_delete(json_data['delete'])
		elif json_data.has_key('limit'):
			self.on_limit(json_data['limit'])
		else:
			self.on_unknown(json_data)

	def on_status(self, status):
		return

	def on_delete(self, delete):
		return

	def on_limit(self, limit):
		return

	def on_unknown(self, json):
		return

