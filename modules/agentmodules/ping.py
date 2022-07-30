import json, threading
from datetime import datetime

class Ping(object):
    def __init__(self, agents, io, ips={}, dbfile="ping.json", workers=[]):
        self.agents = agents
        self.io = io
        self.dbfile = dbfile
        self.ips = ips
        self.workers = workers
        
        try:
            self.db = json.loads(open(self.dbfile, "r").read())
        except:
            self.db = {'data':{}}
            with open(self.dbfile, "w") as f:
                f.write(json.dumps(self.db))
        
    def _save(self):
        with open(self.dbfile, "w") as f:
            f.write(json.dumps(self.db))
    
    def ping(self):
        res = {}
        for ip in self.ips:
            outs = self.agents.cmd_now(self.workers, 'shell', args=['ping -c 1 %s' % ip])
            for name in outs:
                outs[name] = "1 received" in outs[name]
            res[ip] = outs
        return res
    
    def pingany(self, pd):
        res = {}
        for ip in pd:
            res[ip] = any(list(pd[ip].values()))
        return res
    
    def _start(self):
        while self.t_running:
            data = self.ping()
            res = self.pingany(data)

            self.db['data'][str(datetime.now())] = data
            for ip in res:
                if not (p:=self.db.get("lastactive", {}).get(ip)) == res[ip]:
                    #self.io.show("[ping] %s@%s is now %s (reachable from [%s])" % (
                    #    self.ips.get(ip,"unknown"), ip,
                    #    "online" if res[ip] else "offline",
                    #    ', '.join([name for name in data[ip] if data[ip][name]]),
                    #))
                    if not 'lastactive' in self.db: self.db['lastactive'] = {}
                    self.db['lastactive'][ip] = res[ip]
            
            self._save()
    
    def start(self):
        self.t_running = True
        self.t = threading.Thread(target=self._start)
        self.t.start()
    
    def stop(self):
        self.t_running = False
        self.t.join()