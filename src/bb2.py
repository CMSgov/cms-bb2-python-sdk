"""
Blue Button 2.0 SDK Class

"""

BB2_CONFIG = {
    "base_url": "https://sandbox.bluebutton.cms.gov",
    "client_id": "foo",
    "client_secret": "bar",
    "callback_url": "http://localhost:3001/api/bluebutton/callback/",
    "version": "1",
    "environment": "PRODUCTION"
}


class Bb2:
    name = "bb2"
    verbose_name = "Blue Button 2.0 SDK Package"

    def __init__(self, config):
        self.config = config
        self.client_id = config['client_id']
        self.client_secret = config['client_secret']
        self.callback_url = config['callback_url']
        self.version = config['version']
        self.base_url = config['base_url']

    def get_config(self):
        return self.config

    def hello(self):
        mesg = "Hello from BB2 SDK Class method!!!"
        print(mesg)
        return mesg
