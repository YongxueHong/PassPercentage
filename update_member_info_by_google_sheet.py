from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dashboard.settings')

import django
django.setup()


try:
    input = raw_input
except NameError:
    pass

from PassPercentage.models import MemberInfo

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1CXbH8TNno5RXh2K30BY9H1IZ9xmerghyaNL6Th5b8a8'
SAMPLE_RANGE_NAME = 'A2:E500'


def get_member_info():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8081)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    def get_row_info(row, index):
        try:
            return row[index] if row[index] else 'null'
        except IndexError:
            return 'null'

    if not values:
        print('No data found.')
    else:
        member_info = {}
        cnt = 1
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            member_name = get_row_info(row, 0)
            kerbose_id = get_row_info(row, 1)
            github_account = get_row_info(row, 2)
            leader_eamil = get_row_info(row, 3)
            manager_eamil = get_row_info(row, 4)
            print("%d. Member Name: %s; Kerbose ID: %s; Github account: %s; "
                  "Leader email: %s; Manager email: %s" % (cnt, member_name,
                                                           kerbose_id,
                                                           github_account,
                                                           leader_eamil,
                                                           manager_eamil))
            cnt = cnt + 1
            member_info[kerbose_id] = (member_name, github_account,
                                       leader_eamil, manager_eamil)
    return member_info

#pip3 install --upgrade google-api-python-client
#pip3 install --upgrade google-auth-oauthlib


print("Getting member info from google sheet...")
member_info = get_member_info()

while 1:
    to_move = input("Update member info, yes or no: ")
    if to_move == 'yes':
        cnt = 1
        for kerbose_id in member_info:
            print("%d. Creating member %s" % (cnt, member_info[kerbose_id][0]))
            member = MemberInfo.objects.create(
                    member_name=member_info[kerbose_id][0],
                    kerbose_id=kerbose_id,
                    member_email=kerbose_id + "@redhat.com",
                    leader_email=member_info[kerbose_id][2], manager_email=member_info[kerbose_id][3])
            member.save()
            cnt = cnt + 1
        print("All updated.")
        break
    elif to_move == 'no':
        print("Cancel to update.")
        break
    else:
        print('Please input "yes" or "no".')
