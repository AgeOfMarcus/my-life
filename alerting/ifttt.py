import os, requests

def alert(msg, url=None, event="command_alert", key=None):
    r = requests.get(
        "https://maker.ifttt.com/trigger/%s/with/key/%s" % (
            event,
            key or os.getenv("IFTTT"),
        ),
        data={
            'value1': msg,
            'value2': url or "",
        },
    )
    try:
        return r.json()
    except:
        return r.content.decode()