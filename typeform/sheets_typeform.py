#!/usr/bin/env python2

from __future__ import print_function
import httplib2
import os
import csv

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

class Sheets():

    def __init__(self, spreadsheetId, client_secret_file, application_name, sheet_name):
        self.SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        self.CLIENT_SECRET_FILE = client_secret_file
        self.APPLICATION_NAME = application_name

        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        self.service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        self.spreadsheetId = spreadsheetId

        result = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()

        sheet = [ (sheet['properties']['sheetId'], sheet['properties']['title']) for sheet in result['sheets'] if sheet['properties']['title'] == sheet_name ]

        if not sheet:
            raise ValueError('No such sheet in this spreadsheet')

        self.sheet_name = sheet_name
        self.sheet_id = sheet[0][0]

        self.last_row = self.get_row(last=True)

    def get_credentials(self):
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
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def get_last_id(self, row_no = False):
        rangeName = self.sheet_name + '!'
        rangeName += 'B1:B'

        result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheetId, range=rangeName,
                majorDimension='COLUMNS').execute()
        values = result.get('values',[])
        
        last_id = values[0][-1]

        if row_no:
            return len(values[0])
        else:
            return last_id

    def get_row(self, row_no = None, last = False):
        if not row_no and not last:
            raise ValueError('Invalid usage')

        if last:
            row_no = self.get_last_id(row_no = True)

        rangeName = self.sheet_name + '!'
        rangeName += 'A{0}:BO{0}'.format(row_no)

        result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheetId, range=rangeName,
                majorDimension='ROWS').execute()

        values = result.get('values',[])

        row = values[0] 

        return row
    
    def append_row(self, row):
        if not type(row) is list:
            raise Exception('row is not a list')

        row_count = self.get_last_id(row_no=True) + 1

        new_row = row[0:66] 

        rangeName = self.sheet_name + '!'
        rangeName += 'B{0}:BO{0}'.format(row_count)

        body = {
            'range' : rangeName,
            'values' : [new_row],
            'majorDimension' : 'ROWS'
        }
        
        result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheetId, range=rangeName,
                valueInputOption='USER_ENTERED', body=body).execute()
        return result

    def sort_sheet(self):
        return

        sort_column_index = 2 # sort using 3rd column

        body = {
            'requests': [
                {
                    'sortRange': {
                        'range': {
                            'sheetId': self.sheet_id,
                            'startRowIndex': 27,
                            'startColumnIndex': 0
                        },
                        'sortSpecs': [
                            {
                                'dimensionIndex': sort_column_index,
                                'sortOrder': 'ASCENDING'
                            }
                        ]
                    }
                }
            ]
        }
        
        result = self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheetId, body=body).execute()
        
        return result

if __name__=='__main__':
    sheet = Sheets(spreadsheetId = '1brAVs0c-Vzm5AEVBNaEWe3O4_9JfuIImv0XVIrbFt74', 
            client_secret_file = 'client_secret.json',
            application_name = 'FinancialData',
            sheet_name = 'TF data')
    
    print(sheet.get_last_id())
    print(sheet.get_row(last=True))
