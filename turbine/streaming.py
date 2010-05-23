from urlparse import urljoin
from urllib import urlencode

import pycurl

class Stream(object):

    BASE_URL = 'http://stream.twitter.com/1/'

    def __init__(self, username, password, consumer):
        self.consumer = consumer

        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.USERPWD, '%s:%s' % (username, password))
        self.curl.setopt(pycurl.WRITEFUNCTION, self.on_receive)

    def on_receive(self, data):
        #TODO
        print data

    def launch(self, method, parameters=None):
        self.curl.setopt(pycurl.URL, urljoin(self.BASE_URL, method))
        self.curl.setopt(pycurl.POST, 1)
        self.curl.setopt(pycurl.POSTFIELDS, urlencode(parameters))
        self.curl.perform()

    def filter(self, keywords=None, users=None):
        parameters = {}
        if keywords:
            parameters['track'] = ','.join(keywords)
        if users:
            parameters['follow'] = ','.join([str(u) for u in users])
        self.launch('statuses/filter.json', parameters)
