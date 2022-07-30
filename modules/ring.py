from ring_doorbell import Ring, Auth
from oauthlib.oauth2 import MissingTokenError
from flask import jsonify
from pathlib import Path
import os, threading, json

cache_file = Path("token.cache")

class RingModule(object):
    def __init__(self, app, io, uri="/ring", *args, **kwargs):
        self.io = io
        self.app = app
        self.uri = uri

    def init(self):
        if cache_file.is_file():
            self.auth = Auth("MCommand2/1.0", json.loads(cache_file.read_text()), lambda t: cache_file.write_text(json.dumps(t)))
        else:
            self.auth = Auth("MCommand2/1.0", None, lambda t: cache_file.write_text(json.dumps(t)))
        try:
            self.auth.fetch_token(os.getenv("ring_user"), os.getenv("ring_pass"))
        except MissingTokenError:
            self.auth.fetch_token(os.getenv("ring_user"), os.getenv("ring_pass"), self.io.get("Ring 2FA Code"))
        self.ring = Ring(self.auth)
        self.ring.update_data()
        self.io.info("Ring initialised")
        self.app.add_url_rule(self.uri, "/ring_info", view_func=self.info)
    
    def device(self):
        d = self.ring.devices()['authorized_doorbots'][0]
        d.update()
        d.update_health_data()
        return d
    
    def info(self):
        door = self.device()
        res = {}
        for attr in dir(door):
            if not attr.startswith("_"):
                o = getattr(door, attr)
                try:
                    res[attr] = str(o())
                except:
                    res[attr] = str(o)
        return jsonify(res)
    
    def _start(self):
        self.init()
        door = self.device()
        events = [x for x in reversed(door.history(limit=100))]
        while self.t_running:
            latest = door.history()
            for event in reversed(latest):
                if not event in events:
                    if event['kind'] == 'ding':
                        self.io.show({'name':'ring', 'level':5, 'data':event, 'time':str(event['created_at'])})
                    else:
                        outfunc = self.io.show if event['cv_properties']['person_detected'] else self.io.info
                        outfunc({'name':'ring', 'level':2, 'data':event, 'time':str(event['created_at'])})
                    events.append(event)
    
    def last_event(self):
        return self.device().history(limit=1)[0]

    def start(self):
        self.t_running = True
        self.t = threading.Thread(target=self._start)
        self.t.start()
    def stop(self):
        self.t_running = False
        self.t.join()