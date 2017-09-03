#!/usr/bin/env python
import requests
import sys

### BGUG
import logging
import contextlib
try:
    from http.client import HTTPConnection # py3
except ImportError:
    from httplib import HTTPConnection # py2

def debug_requests_on():
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def debug_requests_off():
    '''Switches off logging of the requests module, might be some side-effects'''
    HTTPConnection.debuglevel = 0

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False

@contextlib.contextmanager
def debug_requests():
    '''Use with 'with'!'''
    debug_requests_on()
    yield
    debug_requests_off()
### DEBUG



DEBUG=1
APNIC_ECON_URL="http://data.labs.apnic.net/ipv6-measurement/Economies/%s/%s.asns.json?m=1" % ( sys.argv[1], sys.argv[1] )

def deb( text ):
	if DEBUG==1:
		print >>sys.stdout, text

r = requests.get( APNIC_ECON_URL )
for thing in r.json():
	pct = thing['percent']
	asn = thing['as']
	name = thing['autnum']
	deb("processing %s" % name )
	deb("processing %s" % asn )
	debug_requests_on()
	ro = requests.get( "http://stat.ripe.net/data/prefix-count/data.json?resolution=8h&resource=AS%s" % asn )
	deb( ro.text )
	j = ro.json()
	v4_series = j['data']['ipv4']
	if v4_series[0]['prefixes'] == 0:
		v4_series = v4_series[1:]
	if v4_series[-1]['prefixes'] == 0:
		v4_series = v4_series[:-1]
	for idx,data in enumerate( v4_series ):
		print idx, data
		


