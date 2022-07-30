class ZTE(object):
    def __init__(self, agents, workers=["omen"]):
        self.agents = agents
        self.workers = workers
    
    def _sh(self, cmd):
        return self.agents.cmd_now(self.workers, "adb_sh", args=[cmd])
    
    def leds(self, c=1):
        for led in ['green','red','button-backlight']:
            self._sh('su -c "echo %i > /sys/class/leds/%s/brightness"' % (c, led))
        return str(c)
    
    def photo(self):
        return self.agents.cmd_now(self.workers, "adb_photo")

