import requests
import codecs
import ConfigParser

class MailAPI(object):

    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        configFilePath = r'mail_api.ini'
        self.config.read(configFilePath)
        self.get_config()
        self.get_default_content()

    def get_config(self):
        self.from_email = self.config.get('mail','FROM_EMAIL')
        self.to_email = self.config.get('mail','TO_EMAIL')
        self.api_key = self.config.get('mail','API_KEY')
        self.domain = self.config.get('mail','DOMAIN')

    def get_default_content(self):
        file_html = codecs.open("users_final.html",'r')
        self.content  = file_html.read()

    def send_simple_message(
<<<<<<< HEAD
        self, to_email=None, from_email=None, content=None):
        if to_email is None:
            to_email = self.to_email
        if from_email is None:
            from_email = self.from_email
        if content is None:
            content = self.content
=======
        self, to_email=self.to_email, from_email=self.from_email, content=self.content):

>>>>>>> 9a9ad29ba310f6ab3144e9e9134ab2a44a75bda6
        return requests.post(
            "https://api.mailgun.net/v3/"+self.domain+"/messages",
            auth=("api", self.api_key),
            data={"from": from_email,
            "to": to_email,
            "subject": "Welcome to wisewallet",
            "html": content})





# print(send_simple_message("vmehta342@gmail.com","WiseWallet <welcome@mywisewallet.com>"))
