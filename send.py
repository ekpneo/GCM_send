import urllib2
import json 

api_key = raw_input('API Key:')
regId = raw_input('Reg Id:')

data = {
    'registration_ids': [regId],
    'data': {
        'msg': 'Hello world!'
    }
}

request = urllib2.Request('https://android.googleapis.com/gcm/send', data=json.dumps(data), headers={'Authorization': 'key='+api_key, 'Content-Type': 'application/json'})

print urllib2.urlopen(request).read()

