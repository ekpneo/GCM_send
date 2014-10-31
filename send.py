import urllib2
import json 
import sys

if len(sys.argv) < 2: 
    print 'Usage: python send.py [msg]'
    sys.exit()

cfg = json.load(file('./config.json'))
api_key = cfg['api_key']
regId = cfg['reg_id']

data = {
    'registration_ids': [regId],
    'data': {
        'msg': sys.argv[1]
    }
}

request = urllib2.Request('https://android.googleapis.com/gcm/send', data=json.dumps(data), headers={'Authorization': 'key='+api_key, 'Content-Type': 'application/json'})

print urllib2.urlopen(request).read()

