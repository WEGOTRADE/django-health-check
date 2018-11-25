from django.core.cache import CacheKeyWarning, cache

from health_check.backends import BaseHealthCheckBackend
from health_check.conf import HEALTH_CHECK
from health_check.exceptions import (
    ServiceReturnedUnexpectedResult, ServiceUnavailable
)

CRITICAL_CACHE = HEALTH_CHECK['CRITICAL_CACHE']


class CacheBackend(BaseHealthCheckBackend):
    critical_service = CRITICAL_CACHE

    def check_status(self):
        try:
            cache.set('djangohealtcheck_test', 'itworks', 1)
            if not cache.get("djangohealtcheck_test") == "itworks":
                raise ServiceUnavailable("Cache key does not match")
        except CacheKeyWarning as e:
            self.add_error(ServiceReturnedUnexpectedResult("Cache key warning"), e)
        except ValueError as e:
            self.add_error(ServiceReturnedUnexpectedResult("ValueError"), e)
        except ConnectionError as e:
            self.add_error(ServiceReturnedUnexpectedResult("Connection Error"), e)
