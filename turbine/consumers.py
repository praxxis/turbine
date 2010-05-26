from turbine import TurbineError

class JSONConsumer(object):

    def __init__(self):
        try:
            self.__json = __import__('simplejson')
        except ImportError:
            self.__json = __import__('json')

    def __call__(self, payload):
        try:
            json = self.__json.loads(payload)
        except Exception, e:
            raise TurbineError('Failed to parse JSON payload: %s' % e)

        self.on_json(json)

    def on_json(self, json):
        if json.has_key('text'):
            self.on_status(json)
        elif json.has_key('delete'):
            self.on_delete(json['delete'])
        elif json.has_key('limit'):
            self.on_limit(json['limit'])
        else:
            self.on_unknown(json)

    def on_status(self, status):
        return

    def on_delete(self, delete):
        return

    def on_limit(self, limit):
        return

    def on_unknown(self, json):
        return

