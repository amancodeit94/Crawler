

from __future__ import unicode_literals
import beautifulsoup from bs4
import os
import sys
import six
import copy
import time

import tornado.ioloop
import tornado.httputil
import tornado.httpclient
import pyspider

from six.moves import queue, http_cookies
from six.moves.urllib.robotparser import RobotFileParser
from requests import cookies
from six.moves.urllib.parse import urljoin, urlsplit
from tornado import gen
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado.simple_httpclient import SimpleAsyncHTTPClient

from pyspider.libs import utils, dataurl, counter
from pyspider.libs.url import quote_chinese
from .cookie_utils import extract_cookies_to_jar
logger = logging.getLogger('fetcher')


class MyCurlAsyncHTTPClient(CurlAsyncHTTPClient):

    def free_size(self):
        return len(self._free_list)

    def size(self):
        return len(self._curls) - self.free_size()


class MySimpleAsyncHTTPClient(SimpleAsyncHTTPClient):

    def free_size(self):
        return self.max_clients - self.size()

    def size(self):
        return len(self.active)

fe
            try:
                self.outqueue.put((task, result))
            except Exception as e:
                logger.exception(e)

    def fetch(self, task, callback=None):
        if self.async:
            return self.async_fetch(task, callback)
        else:
            return self.async_fetch(task, callback).result()

        # etag
        if task_fetch.get('etag', True):
            _t = None
            if isinstance(task_fetch.get('etag'), six.string_types):
                _t = task_fetch.get('etag')
            elif track_ok:
                _t = track_headers.get('etag')
            if _t and 'If-None-Match' not in fetch['headers']:
                fetch['headers']['If-None-Match'] = _t
        # last modifed
        if task_fetch.get('last_modified', task_fetch.get('last_modifed', True)):
            last_modified = task_fetch.get('last_modified', task_fetch.get('last_modifed', True))
            _t = None
            if isinstance(last_modified, six.string_types):
                _t = last_modified
            elif track_ok:
                _t = track_headers.get('last-modified')
            if _t and 'If-Modified-Since' not in fetch['headers']:
                fetch['headers']['If-Modified-Since'] = _t
        # timeout
        if 'timeout' in fetch:
            fetch['request_timeout'] = fetch['timeout']
            del fetch['timeout']
        # data rename to body
        if 'data' in fetch:
            fetch['body'] = fetch['data']
            del fetch['data']

        return fetch

    @gen.coroutine
    def can_fetch(self, user_agent, url):
        parsed = urlsplit(url)
      

   
    def xmlrpc_run(self, port=24444, bind='127.0.0.1', logRequests=False):
        '''Run xmlrpc server'''
        import umsgpack
        from pyspider.libs.wsgi_xmlrpc import WSGIXMLRPCApplication
        try:
            from xmlrpc.client import Binary
        except ImportError:
            from xmlrpclib import Binary

        application = WSGIXMLRPCApplication()

        application.register_function(self.quit, '_quit')
        application.register_function(self.size)

        def sync_fetch(task):
            result = self.sync_fetch(task)
            result = Binary(umsgpack.packb(result))
            return result
        application.register_function(sync_fetch, 'fetch')

        def dump_counter(_time, _type):
            return self._cnt[_time].to_dict(_type)
        application.register_function(dump_counter, 'counter')

        

        container = tornado.wsgi.WSGIContainer(application)
        self.xmlrpc_ioloop = tornado.ioloop.IOLoop()
        self.xmlrpc_server = tornado.httpserver.HTTPServer(container, io_loop=self.xmlrpc_ioloop)
        self.xmlrpc_server.listen(port=port, address=bind)
        logger.info('fetcher.xmlrpc listening on %s:%s', bind, port)
        self.xmlrpc_ioloop.start()

    def on_fetch(self, type, task):
        '''Called before task fetch'''
        pass

    def on_result(self, type, task, result):
        '''Called after task fetched'''
        status_code = result.get('status_code', 599)
        if status_code != 599:
            status_code = (int(status_code) / 100 * 100)
        self._cnt['5m'].event((task.get('project'), status_code), +1)
        self._cnt['1h'].event((task.get('project'), status_code), +1)

        if type in ('http', 'phantomjs') and result.get('time'):
            content_len = len(result.get('content', ''))
            self._cnt['5m'].event((task.get('project'), 'speed'),
                                  float(content_len) / result.get('time'))
            self._cnt['1h'].event((task.get('project'), 'speed'),
                                  float(content_len) / result.get('time'))
            self._cnt['5m'].event((task.get('project'), 'time'), result.get('time'))
            self._cnt['1h'].event((task.get('project'), 'time'), result.get('time'))
