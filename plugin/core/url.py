from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import pathname2url
from urllib.request import url2pathname


def filename_to_uri(path: str) -> str:
    return urljoin('file:', pathname2url(path))


def uri_to_filename(uri: str) -> str:
    # Sending extra slash on URI on Windows with MSYS2
    # https://github.com/cquery-project/cquery/issues/492
    # print("'uri': '%s'" % urlparse(uri).path )
    # print("urlparse(uri).path:               %s" % urlparse(uri).path )
    # print("url2pathname(urlparse(uri).path): %s" % url2pathname(urlparse(uri).path) )
    return url2pathname(urlparse(uri).path).strip('\\')
