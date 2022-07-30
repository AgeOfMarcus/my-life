from twilio.rest import Client
import os

class Whatsapp(object):
    def __init__(self, app, io):
        self.app = app
        self.io = io
        self.from_ = 'whatsapp:+14155238886'

        self.client = Client(os.getenv("twilio_sid"), os.getenv("twilio_secret"))
    
    def send(self, to, msg):
        return self.client.messages.create(body=msg, from_=self.from_, to="whatsapp:"+to)
    
    def invite(self):
        return "whatsapp://send?phone=%s&text=join shout-comfortable" % self.from_.split(":")[-1]