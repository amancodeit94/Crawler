
import cgi
import re
import six
import json
import chardet
import lxml.html
import lxml.etree
from tblib import Traceback
from pyquery import PyQuery
from requests.structures import CaseInsensitiveDict
from requests import HTTPError
from pyspider.libs import utils


class Response(object):

    def __init__(self, status_code=None, url=None, orig_url=None, headers=CaseInsensitiveDict(),
                 content='', cookies=None, error=None, traceback=None, save=None, js_script_result=None, time=0):
        if cookies is None:
            cookies = {}
        self.status_code = status_code
        self.url = url
        self.orig_url = orig_url
        self.headers = headers
        self.content = content
        self.cookies = cookies
        self.error = error
        self.traceback = traceback
        self.save = save
        self.js_script_result = js_script_result
        self.time = time

    def __repr__(self):
        return u'<Response [%d]>' % self.status_code

    def __bool__(self):
        """Returns true if `status_code` is 200 and no error"""
        return self.ok

    def __nonzero__(self):
        """Returns true if `status_code` is 200 and no error."""
        return self.ok

    @property
    def ok(self):
        """Return true if `status_code` is 200 and no error."""
        try:
            self.raise_for_status()
        except:
            return False
        return True

    @property
    def encoding(self):
        """
        encoding of Response.content.

        if Response.encoding is None, encoding will be guessed
        
