import json

class DB(object):
    def __init__(self, dbfile="db.json"):
        self.dbfile = dbfile
        try:
            self.db = json.loads(open(self.dbfile, "r").read())
        except:
            self.db = {}
            with open(self.dbfile, "w") as f:
                f.write(json.dumps(self.db))

    
    def _save(self):
        with open(self.dbfile, "w") as f:
            f.write(json.dumps(self.db))
    
    def __setitem__(self, item, value):
        self.db[item] = value
        self._save()
    def __getitem__(self, item):
        return self.db.get(item)
    
    def get(self, attr, res=None):
        return self.db.get(attr, res)