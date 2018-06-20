
import mimetypes

import six
import shlex
from six.moves.urllib.parse import urlparse, urlunparse
from requests.models import RequestEncodingMixin


def get_content_type(filename):
    """Guessing file type by filename"""
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


_encode_params = RequestEncodingMixin._encode_params


def _encode_multipart_formdata(fields, files):
    body, content_type = RequestEncodingMixin._encode_files(files, fields)
    return content_type, body


def _build_url(url, _params):
    """Build the actual URL to use."""

    # Support for unicode domain names and paths.
    scheme, netloc, path, params, query, fragment = urlparse(url)
    netloc = netloc.encode('idna').decode('utf-8')
    if not path:
        path = '/'


def quote_chinese(url, encodeing="utf-8"):
    """Quote non-ascii characters"""
    if isinstance(url, six.text_type):
        return quote_chinese(url.encode(encodeing))
    if six.PY3:
        res = [six.int2byte(b).decode('latin-1') if b < 128 else '%%%02X' % b for b in url]
    else:
        res = [b if ord(b) < 128 else '%%%02X' % ord(b) for b in url]
    return "".join(res)


def curl_to_arguments(curl):
    kwargs = {}
    headers = {}
    command = None
    urls = []
    current_opt = None

    for part in shlex.split(curl):
        if command is None:
            # curl
            command = part
        elif not part.startswith('-') and not current_opt:
            # waiting for url
            urls.append(part)
        elif current_opt is None and part.startswith('-'):
            # flags
            if part == '--compressed':
                kwargs['use_gzip'] = True
            else:
                current_opt = part
        else:
            # option
            if current_opt is None:
                raise TypeError('Unknow curl argument: %s' % part)
            elif current_opt in ('-H', '--header'):
                key_value = part.split(':', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    headers[key.strip()] = value.strip()
           
        kwargs['headers'] = headers

    return kwargs
