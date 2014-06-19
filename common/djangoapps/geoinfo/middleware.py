"""
Middleware to identify the country of origin of page requests.

Middleware adds `country_code` in session.

Usage:

# To enable the Geoinfo feature on a per-view basis, use:
decorator `django.utils.decorators.decorator_from_middleware(middleware_class)`

"""

import logging
import pygeoip

from ipware.ip import get_ip
from django.conf import settings

log = logging.getLogger(__name__)


class CountryMiddleware(object):
    """
    Identify the country by IP address.
    """
    def process_request(self, request):
        """
        Identify the country by IP address.

        Store country code in session.
        """
        new_ip_address = get_ip(request)
        old_ip_address = request.session.get('ip_address', None)
        log.warning('Old IP: %s', old_ip_address)
        log.warning('New IP: %s', new_ip_address)

        if new_ip_address != old_ip_address:
            try:
                country_code = pygeoip.GeoIP(settings.GEOIP_PATH).country_code_by_addr(new_ip_address)
            except Exception as exc:
                log.warning('pygeoip exception: %s', str(exc))
                log.warning('geoippath is %s', settings.GEOIP_PATH)
            request.session['country_code'] = country_code
            request.session['ip_address'] = new_ip_address
            log.warning('Country code for IP: %s is set to %s', new_ip_address, country_code)
        else:
            log.warning('Geoinfo: no change.')
