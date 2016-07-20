#!/usr/bin/env python2

from __future__ import print_function
import httplib2
import os
import csv

from apiclient import discovery
import oauth2client 
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'FinancialData'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
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

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1mKAsY92nA3I6PhTkNd9aLIY8_SZMXERr2wg5WTYMk34'
    rangeName = 'A1:A'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName,
        majorDimension='COLUMNS').execute()
    values = result.get('values', [])
    values = values[0]

    if not values:
        print('No data found.')
    else:
        item_count = len(values)

    last_id = values[-1]
    
    body = {
        'data': [
            {
                'majorDimension' : 'ROWS',
                'values' : [],
                'range'  : 'A{}:P'.format(item_count+1)
            }
        ],
        'valueInputOption' : 'USER_ENTERED'
    }
    
    with open('data.csv', 'r') as csvfile:
        csvdata = csv.reader(csvfile)
        row_count = item_count + 1
        for row in csvdata:
            if row[0] in values or not row[0].isdigit():
                continue
            new_row = row[0:10] #A-J
            new_row.append('=left(G{},7)'.format(row_count)) #K
            new_row.append('') #L
            new_row.append('=I{}'.format(row_count)) #M
            new_row.append('=J{}'.format(row_count)) #N
            new_row.append('=if(J{}<50000,1000,0)'.format(row_count)) #O
            new_row.append('=N{0}-O{0}'.format(row_count)) #P
            body['data'][0]['values'].append(new_row)
            row_count += 1
    
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheetId, body=body).execute()
    print(result)


if __name__ == '__main__':
    main()

