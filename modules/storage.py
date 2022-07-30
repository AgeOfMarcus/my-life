import dropbox, os, requests

class Dropbox(object):
    def __init__(self, token=os.getenv("dropbox")):
        self.client = dropbox.Dropbox(token)
    
    def get(self, fn):
        return requests.get(self.client.files_get_temporary_link(fn).link).content
    def put(self, fn, data):
        return self.client.files_upload(data, fn).content_hash