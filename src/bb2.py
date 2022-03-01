"""
Blue Button 2.0 SDK Class

"""

BB2_CONFIG = {
    "baseUrl": "https://sandbox.bluebutton.cms.gov",
    "clientId": "foo",
    "clientSecret": "bar",
    "callbackUrl": "https://www.fake.com/",
    "version": "1",
    "pkce": True,
    "environment": "PRODUCTION"
}

class Bb2:
    name = "bb2"
    verbose_name = "Blue Button 2.0 SDK Package"
    
    def hello(self):
        mesg = "Hello from BB2 SDK Class method!!!"
        print(mesg)
        return mesg