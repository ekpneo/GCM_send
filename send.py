import urllib2
import json 
import sys
from flask import Flask, request, render_template, redirect

# Load the config file.
_cfg = json.load(file('./config.json'))
api_key = _cfg['api_key']
_reg_ids = _cfg['reg_ids']

def save_config():
    global _reg_ids
    _cfg['reg_ids'] = _reg_ids
    json.dump(_cfg, file('./config.json', 'w'))

def send(reg_ids, icon, msg):
    print 'To:', reg_ids
    data = {
        'registration_ids': reg_ids,
        'data': {
            'icon': icon,
            'msg': msg
        }
    }
    request = urllib2.Request('https://android.googleapis.com/gcm/send', data=json.dumps(data), headers={'Authorization': 'key='+api_key, 'Content-Type': 'application/json'})
    return urllib2.urlopen(request).read()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', reg_ids=_reg_ids)

@app.route('/send')
def web_send():
    reg_ids = request.args.get('reg_ids').split(',')
    icon = request.args.get('icon')
    msg = request.args.get('msg')
    print send(reg_ids, icon, msg)
    return redirect('/')

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
