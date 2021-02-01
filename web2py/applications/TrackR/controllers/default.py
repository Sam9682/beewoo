# -*- coding: utf-8 -*-
### required - do no delete
host_name = request.env['http_host']
host_name = host_name[:host_name.find(':')]
HTTPS_WEBSOCKET_URL = 'https://beewoo.fr:8888'
isCaller = False

def user(): return dict(form=auth())

def download(): return response.download(request,db)

def call(): return service()
### end requires

def index():
    return dict()

@auth.requires_login()
def manage_users():
    myquery = (db.auth_user.id != None)
    gridUsers = SQLFORM.grid(query=myquery)
    return locals()

def error():
    return dict()
# coding: utf8

def webrtc_master():
    import sha, random, base64
    key_gen = base64.b64encode(sha.sha(str(random.random())).hexdigest())[:8]
    db.rtc.insert(access_token = key_gen)
    return dict(isCaller=isCaller, host = host_name, access_token = key_gen, class_name=request.args[0])

def webrtc_slave():
    import sha, random, base64
    key_gen = base64.b64encode(sha.sha(str(random.random())).hexdigest())[:8]
    id = db.rtc.insert(access_token = key_gen)
    #relate_keys_db = db(db.rtc.id < id).select(db.rtc.access_token,limitby=(0, 2),orderby=~db.rtc.id)
    #relate_keys = [str(item.access_token) for item in relate_keys_db]
    relate_keys_db = db(db.rtc.id < id).select(db.rtc.access_token).first()
    relate_keys =[relate_keys_db.access_token,]
    return dict(isCaller=isCaller, host = host_name, access_token = key_gen, class_name=request.args[0], relate_keys= XML(relate_keys))

def connect_rtc():
   from gluon.contrib.websocket_messaging import websocket_send
   # MSG, KEY='rtc', GROUP='beewoo'
   websocket_send(HTTPS_WEBSOCKET_URL,request.vars.msg,'rtc',request.args[0])

def exec_webrtc():
    response.files.append(URL('static','js/adapter.js'))
    return dict()

def webrtc():
    response.files.append(URL('static','js/adapter.js'))
    return dict(isCaller=isCaller, host = host_name, access_token = key_gen, class_name=request.args[0])
