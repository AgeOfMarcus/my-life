import json

def object_info(o):
    res = {}
    for x in dir(o):
        if not x.startswith("_"):
            a = getattr(o, x)
            try:
                a = a()
            except:
                pass
            res[x] = str(a)
    return res

def getconfig(name):
    return json.loads(open("config/5s.json" % name, "r").read())