from flask import jsonify

class WebDisplay(object):
    def __init__(self, app, uri="/displays", url="https://command.marcusweinberger.repl.co", scripts=[]):
        self.app = app
        self.uri = uri
        self.base = url
        self.utils = lambda: open("script.js","r").read()
        self.display = lambda: open("webdisplay.html","r").read()
        try:
            self.utils()
            self.display()
        except:
            self.utils = lambda: open("modules/script.js","r").read()
            self.display = lambda: open("modules/webdisplay.html","r").read()
        self.scripts = scripts
    
    def _url(self, path):
        return self.base + self.uri + path
    
    def displays_update(self):
        return jsonify({'scripts':self.scripts})
    
    def start(self):
        self.app.add_url_rule(self.uri + "/update", "webdisplay_update", view_func=self.displays_update)
        self.app.add_url_rule(self.uri, "webdisplay_display", view_func=self.display)
        self.app.add_url_rule(self.uri + "/script.js", "webdisplay_script", view_func=self.utils)