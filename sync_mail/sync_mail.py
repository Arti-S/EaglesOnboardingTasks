from helpers import GmailApi, start_service
from parameters import senders_name, secret_file_path, client_secret_info, subject

if __name__ == '__main__':

    self_gmail_obj = GmailApi(secret_file_path, username=senders_name)   # self
    client_gmail_objs = [GmailApi(client_secret_file_path,username) for username, client_secret_file_path in client_secret_info.items()]         # client
    start_service(self_gmail_obj, client_gmail_objs, subject)
