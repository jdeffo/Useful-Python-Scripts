#Google imports
from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
#Additional Imports
from email.mime.text import MIMEText
import base64
from apiclient import errors
import random
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

#Scopes
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Python Gmail API'
#Get the credentials
def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
#Create Message
def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}
#Send message
def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
#Create a random subject
def create_subject():
    words = ['Once', 'you', 'have', 'the', 'domain', 'name', 'and', 'port', 'information', 'for', 'your', 'email', 'provider', 'tuple', 'contains', 'information', 'about', 'a', 'single']
    subject_len = random.randrange(1, 5)
    subject = ""
    for i in range(subject_len):
        subject += " "+words[random.randrange(0, len(words))]
    return subject.strip()
#Create a random body
def create_body():
    words = ['Once', 'you', 'have', 'the', 'domain', 'name', 'and', 'port', 'information', 'for', 'your', 'email', 'provider', 'tuple', 'contains', 'information', 'about', 'a', 'single']
    body_len = random.randrange(1, 10)
    body = ""
    for i in range(body_len):
        body += " "+words[random.randrange(0, len(words))]
    return body.strip()
#Main
def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    #Message sender and receiver
    sender = "JDeffoEmailServer@gmail.com"
    to = ""
    #Send messsage on random intervals
    for i in range(10):
        waiting = random.randrange(1, 10)
        print("waiting for {} seconds".format(waiting))
        time.sleep(waiting)
        subject = create_subject()
        message_text = create_body()
        msg = create_message(sender, to, subject, message_text)
        send_message(service, "me", msg)
        print("done")

if __name__ == '__main__':
    main()
