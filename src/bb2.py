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

    def get_config(self):
        return self.config

    def hello(self):
        mesg = "Hello from BB2 SDK Class method!!!"
        print(mesg)
        return mesg
