from alerting import ifttt

from flask import request, jsonify
import threading, json, uuid

class ConsoleIO(object):
    def __init__(self, v=True):
        self.v = v

    def info(self, *args, **kwargs):
        print("[*]",' '.join(map(str,args)), **kwargs) if self.v else None
    def error(self, *args, **kwargs):
        print("[!]",' '.join(map(str,args)), **kwargs)
    def show(self, *args, **kwargs):
        print(' '.join(map(str,args)), **kwargs)
    def get(self, *args, **kwargs):
        return input(' '.join(map(str,args)) + ": ")

class MobileDevIO(object):
    def __init__(self, v=True):
        self.v = v
        self.alert = ifttt.alert
    
    def info(self, *args, **kwargs):
        self.alert("[*] " + ' '.join(map(str,args)), **kwargs) if self.v else None
    def error(self, *args, **kwargs):
        self.alert("[!] " + ' '.join(map(str,args)), **kwargs)
    def show(self, *args, **kwargs):
        self.alert(' '.join(map(str,args)), **kwargs)
    def get(self, *args, **kwargs):
        self.alert("INPUT NEEDED AT CONSOLE", **kwargs)
        return input(' '.join(map(str,args)) + ": ")

class FlaskIO(object):
    def __init__(self, app, base, uri="/io", v=True):
        self.app = app
        self.v = v
        self.base = base
        self.uri = uri
        self.send_notification = ifttt.alert
        self.log = []
        self.errors = []
        self.out = []
        self.tmp = {}
    
        self._configure_routes()
    
    def _url(self, path):
        return self.base + self.uri + path    
    def _configure_routes(self):
        self.app.add_url_rule(self.uri + "/log", "_flaskio_log", view_func=self.view_log)
        self.app.add_url_rule(self.uri + "/input/<uid>", "_flaskio_input", view_func=self.do_input)
        self.app.add_url_rule(self.uri + "/errors", "_flaskio_errors", view_func=self.view_errors)
        self.app.add_url_rule(self.uri + "/output", "_flaskio_output", view_func=self.view_out)
    
    def view_log(self):
        return jsonify({'data':self.log})
    def view_errors(self):
        return jsonify({'data':self.errors})
    def view_out(self):
        return jsonify({'data':self.out})
    def do_input(self, uid):
        if (res:=request.args.get("res")):
            self.tmp[uid]['input'] = res
            return "ok"
        msg = self.tmp.get(uid, {'msg':"not found"})['msg']
        return "<script>window.location.replace('%s' + prompt('%s'))</script>" % (
            self._url("/input/%s?res=" % uid),
            msg,
        )
    
    def notify(self, msg, url=None, override=False):
        if self.v or override:
            self.send_notification(msg, url=url)
    
    def info(self, *args, **kwargs):
        self.log.append({'type':'info', 'msg':' '.join(map(str,args)), 'kwargs':kwargs})
    def error(self, *args, **kwargs):
        msg = {'type':'error', 'msg':' '.join(map(str,args)), 'kwargs':kwargs}
        self.errors.append(msg)
        self.log.append(msg)
        self.notify(' '.join(map(str,args)), **kwargs)
    def show(self, *args, **kwargs):
        msg = {'type':'show', 'msg':' '.join(map(str,args)), 'kwargs':kwargs}
        self.out.append(msg)
        self.log.append(msg)
        self.notify(' '.join(map(str,args)), url=kwargs.get("url"))
    def get(self, *args, **kwargs):
        uid = str(uuid.uuid4())
        self.tmp[uid] = {'msg':' '.join(map(str,args)), 'input':False}
        self.notify("[INPUT]: " + self.tmp[uid]['msg'], url=self._url("/input/%s" % uid))
        
        while True:
            if (res:=self.tmp[uid]['input']):
                del self.tmp[uid]
                return res