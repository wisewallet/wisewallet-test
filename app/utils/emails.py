import requests
import codecs
import ConfigParser
import os
import smtplib, ssl

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
        self.from_email = self.config.get('mail','from_email')
        self.to_email = self.config.get('mail','TO_EMAIL')
        # self.api_key = self.config.get('mail','API_KEY')
        # self.domain = self.config.get('mail','DOMAIN')
        self.smtp_server = self.config.get('mail', 'GMAIL_SERVER')
        self.port = self.config.get('mail', 'PORT')
        self.login = self.config.get('mail','USERNAME')
        self.password  = self.config.get('mail','PASSWORD')

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
        print(from_email)
        print(to_email)
        return requests.post(
            "https://api.mailgun.net/v3/"+self.domain+"/messages",
            auth=("api", self.api_key),
            data={"from": self.from_email,
            "to": self.to_email,
            "subject": "Welcome to wisewallet",
            "html": content})

    def sendemail(self, message, to_addr_list=None,
              subject="Welcome to wisewallet",
              smtpserver='smtp.gmail.com'):
      header  = 'From: %s' % self.from_email
      header += 'To: %s' % ','.join(self.to_email)
      header += 'Subject: %s' % subject
      message = header + message
      server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      server_ssl.ehlo()
      print(self.login)
      server_ssl.login(self.login,self.password)
      problems = server_ssl.sendmail(self.login, self.to_email, message)
      print(problems)
      server_ssl.quit()
