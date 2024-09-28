import argparse
import warnings
from http.cookies import SimpleCookie
from shlex import split
from urllib.parse import urlparse
from w3lib.http import basic_auth_header

class DataAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        value = str(values)
        if value.startswith('$'):
            value = value[1:]
        setattr(namespace, self.dest, value)

class CurlParser(argparse.ArgumentParser):
    pass
curl_parser = CurlParser()
curl_parser.add_argument('url')
curl_parser.add_argument('-H', '--header', dest='headers', action='append')
curl_parser.add_argument('-X', '--request', dest='method')
curl_parser.add_argument('-d', '--data', '--data-raw', dest='data', action=DataAction)
curl_parser.add_argument('-u', '--user', dest='auth')
safe_to_ignore_arguments = [['--compressed'], ['-s', '--silent'], ['-v', '--verbose'], ['-#', '--progress-bar']]
for argument in safe_to_ignore_arguments:
    curl_parser.add_argument(*argument, action='store_true')

def curl_to_request_kwargs(curl_command: str, ignore_unknown_options: bool=True) -> dict:
    """Convert a cURL command syntax to Request kwargs.

    :param str curl_command: string containing the curl command
    :param bool ignore_unknown_options: If true, only a warning is emitted when
                                        cURL options are unknown. Otherwise
                                        raises an error. (default: True)
    :return: dictionary of Request kwargs
    """
    pass