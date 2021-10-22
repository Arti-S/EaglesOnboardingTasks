import base64, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from plugins import GooglePlugins
from datetime import datetime


class GmailApi(GooglePlugins):

    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    def __init__(self, client_secret_file, username = 'arti', user_id = 'me') -> None:
        print('please wait while initializing...')
        self.user_id = user_id
        self.service = self.Create_Service(client_secret_file, self.API_NAME, self.API_VERSION, username, self.SCOPES)
        self.email_address = self.service.users().getProfile(userId=self.user_id).execute()['emailAddress']
        self.present_history_id = self.get_present_history_id()
                
    def send_mail(self, email_id, msg_str) -> object:
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = email_id
        mimeMessage['subject'] = 'Fwd msg'
        mimeMessage.attach(MIMEText(msg_str, 'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        message = self.service.users().messages().send(userId=self.user_id, body={'raw': raw_string}).execute()
        print('message sent to %s ' % email_id)
        return message

    def get_message(self, msg_id, in_format = 'raw') -> object:
        return self.service.users().messages().get(userId=self.user_id, id=msg_id, format=in_format).execute()

    def get_messages(self) -> object:
        return self.service.users().messages().list(userId=self.user_id).execute()

    def get_present_history_id(self) -> str:
        profile_obj = self.service.users().getProfile(userId=self.user_id).execute()
        return profile_obj.get('historyId')
    
    def list_history_objects(self, history_id):
        return self.service.users().history().list(userId='me', startHistoryId=history_id).execute()

    @classmethod
    def get_msg_ids(cls, history_obj):
        msg_ids = list()
        for msg_obj in history_obj['history']:
            if msg_obj.get('messagesAdded'):
                for val in msg_obj['messagesAdded']:
                    msg_ids.append(val['message']['id'])
        return set(msg_ids)
    
def start_service(self_gmail_obj, client_gmail_objs, subject):
    while True:
        if self_gmail_obj.present_history_id != self_gmail_obj.get_present_history_id():
            print('changes detected')
            msg_ids = self_gmail_obj.get_msg_ids(self_gmail_obj.list_history_objects(self_gmail_obj.present_history_id))
            for msg_id in msg_ids:
                msg_obj = self_gmail_obj.get_message(msg_id, 'raw')
                full_msg_obj = self_gmail_obj.get_message(msg_id, 'full')
                mail_data = {i['name']:i['value'] for i in full_msg_obj['payload']['headers'] if i.get('name') == 'Subject'}
                if subject != mail_data['Subject']:continue
                for client_gmail_obj in client_gmail_objs:
                    _ = client_gmail_obj.service.users().messages().insert(userId='me', body={'raw': msg_obj['raw'], "labelIds": ["INBOX"]}).execute()
                    print(f'updated for {client_gmail_obj.email_address}')
                print('done')
            self_gmail_obj.present_history_id = self_gmail_obj.get_present_history_id()

        output_msg = '[HistoryId = {} Time stamp = {} retrying in {} seconds]'.format(self_gmail_obj.present_history_id, datetime.now(), self_gmail_obj.REFRESH_TIME)
        print(output_msg)
        time.sleep(self_gmail_obj.REFRESH_TIME)
