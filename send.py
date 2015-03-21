import urllib2
import json 
import sys
import time
import subprocess
from flask import Flask, request, render_template, redirect

# Load the config file.
_cfg = json.load(file('./config.json'))
api_key = _cfg['api_key']
_reg_ids = _cfg['reg_ids']

def save_config():
    global _reg_ids
    _cfg['reg_ids'] = _reg_ids
    json.dump(_cfg, file('./config.json', 'w'))

def send_cancel(reg_ids):
    data = { 
        'registration_ids': reg_ids,
        'data': {
            'type': 'cancel'
        }}
    request = urllib2.Request('https://android.googleapis.com/gcm/send', data=json.dumps(data), headers={'Authorization': 'key='+api_key, 'Content-Type': 'application/json'})
    return urllib2.urlopen(request).read()

def send(reg_ids, icon, title, msg):
    print 'To:', reg_ids
    data = {
        'registration_ids': reg_ids,
        'data': {
            'title': title,
            'icon': icon,
            'msg': msg
        }
    }
    print json.dumps(data)
    request = urllib2.Request('https://android.googleapis.com/gcm/send', data=json.dumps(data), headers={'Authorization': 'key='+api_key, 'Content-Type': 'application/json'})
    return urllib2.urlopen(request).read()

msg_id = 1
topic = '/user/Wv5mtEpARNq16ZasKDIFqA'

def send_mosquitto(icon, title, msg):
    global msg_id
    data = {
	    'id': 'msg' + str(msg_id),
        'from': 'C2I_cMf-S8O2LrUVKOWgzA',
        't':'msg',
        'd': {
            'title': title,
            'text': msg,
            'icon': icon,
        }
    }
    subprocess.call(['mosquitto_pub', 
        '-t', topic, 
        '-m', json.dumps(data),
        '-q', '1' ])
    msg_id += 1
    
def cancel_mosquitto():
    data = {
        'id': 'cancel' + str(msg_id - 1),
        'from': 'C2I_cMf-S8O2LrUVKOWgzA',
        't': 'cancel',
        'd': { 'id': 'msg' + str(msg_id - 1) }
    }
    subprocess.call(['mosquitto_pub', 
        '-t', topic, 
        '-m', json.dumps(data),
        '-q', '1' ])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', reg_ids=_reg_ids)

@app.route('/send')
def web_send():
    reg_ids = request.args.get('reg_ids').split(',')
    icon = request.args.get('icon')
    title = request.args.get('title')
    msg = request.args.get('msg')
    print send(reg_ids, icon, title, msg)
    return 'ok'

@app.route('/cancel')
def web_cancel():
    reg_ids = request.args.get('reg_ids').split(',')
    print send_cancel(reg_ids)
    return 'ok'

@app.route('/mosq_send')
def web_mosq_send():
    icon = request.args.get('icon')
    title = request.args.get('title')
    msg = request.args.get('msg')
    send_mosquitto(icon, title, msg)
    return 'ok'

@app.route('/mosq_cancel')
def web_mosq_cancel():
    cancel_mosquitto()
    return 'ok'

@app.route('/add_reg_id')
def add_reg_id():
    reg_id = request.args.get('reg_id')
    if len(reg_id):
        if reg_id not in _reg_ids:
            _reg_ids.append(reg_id)
            save_config()
    return 'ok'

if __name__ == '__main__':
    print 'Go to http://localhost:5000/ to send notifications.'
    app.run(host="0.0.0.0", port=5000)
