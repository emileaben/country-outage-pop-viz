#!/usr/bin/env python
import requests
import sys
import json
import arrow

DEBUG=1
APNIC_ECON_URL="http://data1.labs.apnic.net/ipv6-measurement/Economies/%s/%s.asns.json?m=1" % ( sys.argv[1], sys.argv[1] )
START=arrow.get( sys.argv[2] )

def deb( text ):
	if DEBUG==1:
		print >>sys.stderr, text

out = {
	'meta': {},
   'isps': []
} 

out['meta']['country'] = sys.argv[1]
out['meta']['start'] = START.strftime("%Y-%m-%dT%H:%M:%S")
out['meta']['stop'] = arrow.get( arrow.now() ).strftime("%Y-%m-%dT%H:%M:%S")


r = requests.get( APNIC_ECON_URL )
for thing in r.json():
	pct = thing['percent']
	asn = thing['as']
	name = thing['autnum']
	outages = []
	deb("processing %s" % name )
	deb("processing %s" % asn )
	ro = requests.get( "http://stat.ripe.net/data/prefix-count/data.json?resolution=8h&resource=AS%s&starttime=%s" % (asn, START.strftime("%Y-%m-%dT%H:%M:%S") ) )
	j = ro.json()
	v4_series = j['data']['ipv4']
	if v4_series[0]['prefixes'] == 0:
		v4_series = v4_series[1:]
	#if v4_series[-1]['prefixes'] == 0:
	#	v4_series = v4_series[:-1]
	for idx,data in enumerate( v4_series ):
		# 50 {u'prefixes': 16, u'timestamp': u'2017-06-24T16:00:00', u'address-space': 141}
		if data['prefixes'] == 0:
			if len( v4_series ) > idx+1:
				outages.append( [data['timestamp'] , v4_series[idx+1]['timestamp']] )
	out['isps'].append({
		'asn': asn,
		'pct': pct,
		'name': name,
		'outages': outages
	})

print json.dumps( out, indent=2 )
