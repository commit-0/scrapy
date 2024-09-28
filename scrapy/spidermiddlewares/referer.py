"""
RefererMiddleware: populates Request referer field, based on the Response which
originated it.
"""
import warnings
from typing import Tuple
from urllib.parse import urlparse
from w3lib.url import safe_url_string
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import Request, Response
from scrapy.utils.misc import load_object
from scrapy.utils.python import to_unicode
from scrapy.utils.url import strip_url
LOCAL_SCHEMES = ('about', 'blob', 'data', 'filesystem')
POLICY_NO_REFERRER = 'no-referrer'
POLICY_NO_REFERRER_WHEN_DOWNGRADE = 'no-referrer-when-downgrade'
POLICY_SAME_ORIGIN = 'same-origin'
POLICY_ORIGIN = 'origin'
POLICY_STRICT_ORIGIN = 'strict-origin'
POLICY_ORIGIN_WHEN_CROSS_ORIGIN = 'origin-when-cross-origin'
POLICY_STRICT_ORIGIN_WHEN_CROSS_ORIGIN = 'strict-origin-when-cross-origin'
POLICY_UNSAFE_URL = 'unsafe-url'
POLICY_SCRAPY_DEFAULT = 'scrapy-default'

class ReferrerPolicy:
    NOREFERRER_SCHEMES: Tuple[str, ...] = LOCAL_SCHEMES
    name: str

    def strip_url(self, url, origin_only=False):
        """
        https://www.w3.org/TR/referrer-policy/#strip-url

        If url is null, return no referrer.
        If url's scheme is a local scheme, then return no referrer.
        Set url's username to the empty string.
        Set url's password to null.
        Set url's fragment to null.
        If the origin-only flag is true, then:
            Set url's path to null.
            Set url's query to null.
        Return url.
        """
        pass

    def origin(self, url):
        """Return serialized origin (scheme, host, path) for a request or response URL."""
        pass

class NoReferrerPolicy(ReferrerPolicy):
    """
    https://www.w3.org/TR/referrer-policy/#referrer-policy-no-referrer

    The simplest policy is "no-referrer", which specifies that no referrer information
    is to be sent along with requests made from a particular request client to any origin.
    The header will be omitted entirely.
    """
    name: str = POLICY_NO_REFERRER

class NoReferrerWhenDowngradePolicy(ReferrerPolicy):
    """
    https://www.w3.org/TR/referrer-policy/#referrer-policy-no-referrer-when-downgrade

    The "no-referrer-when-downgrade" policy sends a full URL along with requests
    from a TLS-protected environment settings object to a potentially trustworthy URL,
    and requests from clients which are not TLS-protected to any origin.

    Requests from TLS-protected clients to non-potentially trustworthy URLs,
    on the other hand, will contain no referrer information.
    A Referer HTTP header will not be sent.

    This is a user agent's default behavior, if no policy is otherwise specified.
    """
    name: str = POLICY_NO_REFERRER_WHEN_DOWNGRADE

class SameOriginPolicy(ReferrerPolicy):
    """
    https://www.w3.org/TR/referrer-policy/#referrer-policy-same-origin

    The "same-origin" policy specifies that a full URL, stripped for use as a referrer,
    is sent as referrer information when making same-origin requests from a particular request client.

    Cross-origin requests, on the other hand, will contain no referrer information.
    A Referer HTTP header will not be sent.
    """
    name: str = POLICY_SAME_ORIGIN

class OriginPolicy(ReferrerPolicy):
    """
    https://www.w3.org/TR/referrer-policy/#referrer-policy-origin

    The "origin" policy specifies that only the ASCII serialization
    of the origin of the request client is sent as referrer information
    when making both same-origin requests and cross-origin requests
    from a particular request client.
    """
    name: str = POLICY_ORIGIN

class StrictOriginPolicy(ReferrerPolicy):
    """
    https://www.w3.org/TR/referrer-policy/#referrer-policy-strict-origin

    The "strict-origin" policy sends the ASCII serialization
    of the origin of the request client when making requests:
    - from a TLS-protected environment settings object to a potentially trustworthy URL, and
    - from non-TLS-protected environment settings objects to any origin.

    Requests from TLS-protected request clients to non- potentially trustworthy URLs,
    on the other hand, will contain no referrer information.
    A Referer HTTP header will not be sent.
    """
    name: str = POLICY_STRICT_ORIGIN

class OriginWhenCrossOriginPolicy(ReferrerPolicy):
    """
    https://www.w3.org/TR/referrer-policy/#referrer-policy-origin-when-cross-origin

    The "origin-when-cross-origin" policy specifies that a full URL,
    stripped for use as a referrer, is sent as referrer information
    when making same-origin requests from a particular request client,
    and only the ASCII serialization of the origin of the request client
    is sent as referrer information when making cross-origin requests
    from a particular request client.
    """
    name: str = POLICY_ORIGIN_WHEN_CROSS_ORIGIN

class StrictOriginWhenCrossOriginPolicy(ReferrerPolicy):
    """
    https://www.w3.org/TR/referrer-policy/#referrer-policy-strict-origin-when-cross-origin

    The "strict-origin-when-cross-origin" policy specifies that a full URL,
    stripped for use as a referrer, is sent as referrer information
    when making same-origin requests from a particular request client,
    and only the ASCII serialization of the origin of the request client
    when making cross-origin requests:

    - from a TLS-protected environment settings object to a potentially trustworthy URL, and
    - from non-TLS-protected environment settings objects to any origin.

    Requests from TLS-protected clients to non- potentially trustworthy URLs,
    on the other hand, will contain no referrer information.
    A Referer HTTP header will not be sent.
    """
    name: str = POLICY_STRICT_ORIGIN_WHEN_CROSS_ORIGIN

class UnsafeUrlPolicy(ReferrerPolicy):
    """
    https://www.w3.org/TR/referrer-policy/#referrer-policy-unsafe-url

    The "unsafe-url" policy specifies that a full URL, stripped for use as a referrer,
    is sent along with both cross-origin requests
    and same-origin requests made from a particular request client.

    Note: The policy's name doesn't lie; it is unsafe.
    This policy will leak origins and paths from TLS-protected resources
    to insecure origins.
    Carefully consider the impact of setting such a policy for potentially sensitive documents.
    """
    name: str = POLICY_UNSAFE_URL

class DefaultReferrerPolicy(NoReferrerWhenDowngradePolicy):
    """
    A variant of "no-referrer-when-downgrade",
    with the addition that "Referer" is not sent if the parent request was
    using ``file://`` or ``s3://`` scheme.
    """
    NOREFERRER_SCHEMES: Tuple[str, ...] = LOCAL_SCHEMES + ('file', 's3')
    name: str = POLICY_SCRAPY_DEFAULT
_policy_classes = {p.name: p for p in (NoReferrerPolicy, NoReferrerWhenDowngradePolicy, SameOriginPolicy, OriginPolicy, StrictOriginPolicy, OriginWhenCrossOriginPolicy, StrictOriginWhenCrossOriginPolicy, UnsafeUrlPolicy, DefaultReferrerPolicy)}
_policy_classes[''] = NoReferrerWhenDowngradePolicy

def _load_policy_class(policy, warning_only=False):
    """
    Expect a string for the path to the policy class,
    otherwise try to interpret the string as a standard value
    from https://www.w3.org/TR/referrer-policy/#referrer-policies
    """
    pass

class RefererMiddleware:

    def __init__(self, settings=None):
        self.default_policy = DefaultReferrerPolicy
        if settings is not None:
            self.default_policy = _load_policy_class(settings.get('REFERRER_POLICY'))

    def policy(self, resp_or_url, request):
        """
        Determine Referrer-Policy to use from a parent Response (or URL),
        and a Request to be sent.

        - if a valid policy is set in Request meta, it is used.
        - if the policy is set in meta but is wrong (e.g. a typo error),
          the policy from settings is used
        - if the policy is not set in Request meta,
          but there is a Referrer-policy header in the parent response,
          it is used if valid
        - otherwise, the policy from settings is used.
        """
        pass