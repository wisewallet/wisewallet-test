import requests
import codecs
import ConfigParser
import os

here = os.path.dirname(os.path.abspath(__file__))
ini = os.path.normpath(os.path.join(here, 'mail_api.ini'))
htmls = os.path.normpath(os.path.join(here, 'users_final.html'))

class MailAPI(object):

    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(ini)
        self.get_config()
        self.get_default_content()

    def get_config(self):
        self.from_email = self.config.get('mail','FROM_EMAIL')
        self.to_email = self.config.get('mail','TO_EMAIL')
        self.api_key = self.config.get('mail','API_KEY')
        self.domain = self.config.get('mail','DOMAIN')

    def get_default_content(self):
        file_html = codecs.open(htmls,'r')
        self.content  = file_html.read()

    def send_simple_message(
        self, to_email=None, from_email=None, content=None):
        if to_email is None:
            to_email = self.to_email
        if from_email is None:
            from_email = self.from_email
        if content is None:
            content = self.content
        print(self.from_email)
        print(self.to_email)
        print(self.api_key == 'cae2ea3cf2b4b90bf12edcd44683b54a-4412457b-8ad16907')
        print(self.domain)
        return requests.post(
            "https://api.mailgun.net/v3/"+self.domain+"/messages",
            auth=("api", self.api_key),
            data={"from": self.from_email,
            "to": self.to_email,
            "subject": "Welcome to wisewallet",
            "html": content})
