from myio import FlaskIO
from modules import Ring, Hooks, Agents, DB, WebUtils, WebDisplay, Whatsapp
import config

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO
import hashlib, os, threading, code, uuid

app = Flask(__name__)
CORS(app)

db = DB()
fio = FlaskIO(app, "https://command.marcusweinberger.repl.co")

ring = Ring(app, fio)
hooks = Hooks(app, fio)
webutils = WebUtils(app, fio)
webdisplay = WebDisplay(app)
agents = Agents(app, fio)
whatsapp = Whatsapp(app, fio)



def dohash(string):
    return hashlib.sha256(
        hashlib.sha256(string.encode()).digest() + b"lolsalt"
    ).hexdigest()

@app.before_request
def app_before_request():
    if request.path.startswith("/api"):
        if not dohash(request.form.get("token") or request.args.get("token") or "") in [dohash(x) for x in os.getenv("apikeys").split(":")]:
            return "invalid token", 403

server_id = str(uuid.uuid4())
@app.route("/")
def app_index():
    return server_id

@app.route("/api/cmd", methods=['GET','POST'])
def app_api_do_cmd():
    res = agents.cmd_now(request.form.get('agents',request.args.get("agents")), request.form.get('fn',request.args.get("fn")), args=request.form.get("args", []), kwargs=request.form.get("kwargs", {}))
    return jsonify({'res':res})

@app.route("/api/agents")
def app_api_agents():
    return jsonify(agents.agents)

@app.route("/api/agents/pic/<name>", methods=['GET','POST'])
@app.route("/api/agents/pic/<name>/<camera_id>", methods=['GET','POST'])
def app_api_agents_pic(name, camera_id=0):
    fn = agents.cmd_now([name], "take_photo", kwargs={'camera_id':camera_id})[name]
    print("fn = " + str(fn))
    fd = agents.download(name, fn)
    
    return send_file(
        BytesIO(fd),
        mimetype="image/png",
        as_attachment=False,
        attachment_filename=fn.split("/")[-1],
    )

@app.route("/api/torches")
@app.route("/api/torches/<setting>")
def app_api_torches(setting="toggle"):
    setting = setting or "toggle"
    if setting == "toggle":
        sett = not db.get("torches", False)
        db['torches'] = sett
    else:
        sett = setting == "on"
        db['torches'] = sett
    return agents.add_cmd(request.form.get("agents","all"),"torch", args=[sett])

def run():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    webutils.init()

    ring.start()
    webdisplay.start()
    t = threading.Thread(target=run)
    t.start()
    fio.info("[main] command up")

    code.interact(local=globals())
    ring.stop()
    t.join()