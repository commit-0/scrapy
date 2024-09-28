import logging
from typing import Any, Dict
from OpenSSL import SSL
from service_identity.exceptions import CertificateError
from twisted.internet._sslverify import ClientTLSOptions, VerificationError, verifyHostname
from twisted.internet.ssl import AcceptableCiphers
from scrapy.utils.ssl import get_temp_key_info, x509name_to_string
logger = logging.getLogger(__name__)
METHOD_TLS = 'TLS'
METHOD_TLSv10 = 'TLSv1.0'
METHOD_TLSv11 = 'TLSv1.1'
METHOD_TLSv12 = 'TLSv1.2'
openssl_methods: Dict[str, int] = {METHOD_TLS: SSL.SSLv23_METHOD, METHOD_TLSv10: SSL.TLSv1_METHOD, METHOD_TLSv11: SSL.TLSv1_1_METHOD, METHOD_TLSv12: SSL.TLSv1_2_METHOD}

class ScrapyClientTLSOptions(ClientTLSOptions):
    """
    SSL Client connection creator ignoring certificate verification errors
    (for genuinely invalid certificates or bugs in verification code).

    Same as Twisted's private _sslverify.ClientTLSOptions,
    except that VerificationError, CertificateError and ValueError
    exceptions are caught, so that the connection is not closed, only
    logging warnings. Also, HTTPS connection parameters logging is added.
    """

    def __init__(self, hostname: str, ctx: SSL.Context, verbose_logging: bool=False):
        super().__init__(hostname, ctx)
        self.verbose_logging: bool = verbose_logging
DEFAULT_CIPHERS: AcceptableCiphers = AcceptableCiphers.fromOpenSSLCipherString('DEFAULT')