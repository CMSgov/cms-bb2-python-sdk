"""
Blue Button 2.0 SDK Class

"""

BB2_CONFIG = {
    "base_url": "https://sandbox.bluebutton.cms.gov",
    "client_id": "7OaeX8qr7toQZJnc1YQk8TBSt4KXOnXTHm7UtwB0",
    "client_secret": "DOy1nsLtwWYcsFOwRqOWnwKP5MzLfpt6krrWHdmDk0j7asCmbLq2u6oPazcJlF5PqOjYgftaifcbpeVmwZUBgqNkw5osn7qQIMUOFflb1OyJ8hhHrrMqCtWrnJHSqlCp",
    "callback_url": "http://localhost:3001/api/bluebutton/callback/",
    "version": "1",
    "pkce": True,
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
