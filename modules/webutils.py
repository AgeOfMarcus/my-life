from flask import request, jsonify, send_file

class WebUtils(object):
    def __init__(self, app, io, uri="/utils", url="https://command.marcusweinberger.repl.co"):
        self.app = app
        self.io = io
        self.uri = uri
        self.base = url
    
    def url(self, path):
        return self.base + self.uri + path
    
    def web_io(self, fn="show"):
        getattr(self.io, fn)(request.form.get("text", request.args.get("text")), url=request.form.get("url", request.args.get("url")))
        return "sent"
    
    def echo(self):
        return request.args['text']

    def init(self):
        self.app.add_url_rule(self.uri + "/io/<fn>", "webutil_io", view_func=self.web_io)
        self.app.add_url_rule(self.uri + "/echo", "webutil_echo", view_func=self.echo)