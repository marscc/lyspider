import random
from scrapy import log
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy.conf import settings


class RandomUserAgentMiddleware(UserAgentMiddleware):
    """
    user-agent pool
    """

    def process_request(self, request, spider):
        ua = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            print("*******Current UserAgent: %s*******" % ua)
            log.msg("Current UserAgent: " + ua)
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):
    """
    ip proxy
    """

    def process_requeat(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')
