#!/usr/bin/env python2

import json
import sys
import urllib
import pprint
from sheets_typeform import Sheets

TYPEFORM_JSON_API = 'https://api.typeform.com/v1/form/njxhSJ?key=cd3c5967bd6331d8fdbe134f81cc9accfdeecfc4'

def tf_load_data(json_file_path):
    '''
        Row structure:
        B. #
        C. Email
        D. Date of birth
        E. Expected age of retirement
        F. Pension Provider
        // groups start
        G. Investment name
        H. Investment value
        I. Value date
        J. Annual fee on pension
        K. Would you like to add additional...?
        // group end x 5
        AF. Do you have additional pensions you wish to include in the projection?
        AG. Pension provider
        // second groups
        AH. Investment name
        AI. Investment value
        AJ. Value date
        AK. Annual fee on pension
        AL. Would you like to add additional...?
        // second groups end x 5
        BG. Pension fund you intend to contribute to over this time period
        BH. Amount you intend to contrivute to over this time period
        BI. Date you intend those contributions to start
        BJ. Annual fee on pension
        BK. Include my basic rate tax relief in the contribution projections
        BL. Please click the tick box to agree to our terms and conditions
        BM. Start Date (UTC)
        BN. Submit Date (UTC)
        BO. Network ID
    '''

    def get_group_col_pos(question):
        if 'Investment name' in question:
            return 0    
        elif 'Investment value' in question:
            return 1
        elif 'Value date' in question:
            return 2
        elif 'Annual fee' in question:
            return 3
        elif 'Would you like to' in question:
            return 4
        else:
            return -1

    def get_end_pos(question):
        if 'Pension fund you intend' in question:
            return 0
        elif 'Amount you intend to' in question:
            return 1
        elif 'Date you intend' in question:
            return 2
        elif 'Annual fee on pension' in question:
            return 3
        elif 'Include my basic rate' in question:
            return 4
        else:
            return -1

    with open(json_file_path, 'r') as json_file:
        answers_json = json.load(json_file)

    typeform_json = get_typeform_data()
    answers = dict( (int(answer['field']['id']), answer) for answer in answers_json['form_response']['answers'] )
    field_titles = dict( (question['field_id'], question['question']) for question in typeform_json['questions'] )

    labeled_answers = dict()
    for question in typeform_json['questions']:
        t = dict() 
        t['id'] = question['field_id']
        t['other_id'] = question['id']
        t['question'] = field_titles[question['field_id']]
        t['group'] = 0 if 'group' not in question.keys() else question['group']
        
        if t['id'] in answers.keys():
            answer = answers[t['id']]
            datatype = answer['type']
            if datatype in ['text', 'number', 'email']:
                t['value'] = answer[datatype]
            elif datatype == 'boolean':
                t['value'] = int(answer[datatype])
            elif datatype == 'choice':
                t['value'] = answer['choice']['label']
            elif datatype == 'date':
                t['value'] = answer['text'].split('T')[0]
        else:
            t['value'] = ''

        labeled_answers[t['id']] = t

    pension_providers = sorted([ question for question in labeled_answers.values() if 'Pension' in question['question'] and 'textfield_' in question['other_id'] ], key=lambda x: x['id'])

    # constructing the rows:

    groups = sorted([ sorted([question for question in labeled_answers.values() \
            if question['group'] == g ], key=lambda x: x['id']) \
            for g in set( ans['group'] for ans in labeled_answers.values() \
            if ans['group'] != 0 ) ], key=lambda x: x[0]['group'])

    investments_for_p1 = list()
    investments_for_p2 = list()
    end_ques = list()

    for group in groups:
        question = [ question['question'] for question in group if 'Would you like to ' in question['question'] ]
        if len(question) != 1:
            end_ques.append(group)
            continue
        else:
            question = question[0]
        
        if str(pension_providers[0]['id']) in question:
            investments_for_p1.append(group)
        elif str(pension_providers[1]['id']) in question:
            investments_for_p2.append(group)
            
#    pprint.PrettyPrinter().pprint([len(group) for group in investments_for_p1])
#    pprint.PrettyPrinter().pprint(investments_for_p2)

    row = []
    row.append( answers_json['form_response']['token'] )
#    print( labeled_answers[20699463]['question'] )
    row.append( labeled_answers[20699463]['value'] ) # email
#    print( labeled_answers[20699464]['question'] )
    row.append( labeled_answers[20699464]['value'] ) # dob
#    print( labeled_answers[20699465]['question'] )
    row.append( labeled_answers[20699465]['value'] ) # exp age of ret

#    print( pension_providers[0]['question'] )
    row.append( pension_providers[0]['value'] ) # pension provider
    for investment_group in investments_for_p1:
        sub_row = [''] * 5
        for question in investment_group:
            pos = get_group_col_pos(question['question'])
            if(pos == -1):
                continue
            sub_row[pos] = question['value']
        row += sub_row

#    print( labeled_answers[20702491]['question'] )
    row.append( labeled_answers[20702491]['value'] ) # next pension provider

#    print( pension_providers[1]['question'] )
    row.append( pension_providers[1]['value'] ) # pension provider
    for investment_group in investments_for_p2:
        sub_row = [''] * 5
        for question in investment_group:
            pos = get_group_col_pos(question['question'])
            if(pos == -1):
                continue
            sub_row[pos] = question['value']
        row += sub_row

    for q in end_ques:
        sub_row = [''] * 5
        for question in q:
            pos = get_end_pos(question['question']) 
            if pos == -1:
                continue
            sub_row[pos] = question['value']
        row += sub_row

    row.append( labeled_answers[21247735]['value'] ) # please click the tick box
    row.append( '' ) # start date
    row.append( answers_json['form_response']['submitted_at'].replace('Z','').replace('T',' ') ) # submit date
    row.append( answers_json['event_id'] ) # network id

    print(row)
    print(len(row))

    sheet = Sheets(spreadsheetId = '1brAVs0c-Vzm5AEVBNaEWe3O4_9JfuIImv0XVIrbFt74', 
            client_secret_file = 'client_secret.json',
            application_name = 'FinancialData',
            sheet_name = 'TF data')

    sheet.append_row(row)

def get_typeform_data(grouped = False):
    try:
        response = urllib.urlopen(TYPEFORM_JSON_API) 
        data = json.loads(response.read())
    except:
        print('no internet. trying to load local file')
        try:
            with open('form_questions_data.json') as f:
                data = json.load(f)
        except:
            prinf('no file as well')

    if not grouped:
        return data

    d = dict()
    for question in data['questions']:
        if 'group' in question.keys():
            if question['group'] not in d.keys():
                d[question['group']] = list()
            d[question['group']].append(question)
        else:
            if 0 not in d.keys():
                d[0] = list()
            d[0].append(question)
    
    return d


if __name__=='__main__':
    if(len(sys.argv) != 2):
        print('Invalid usage')
        sys.exit(1)

    json_file_path = sys.argv[1]
    tf_load_data(json_file_path)
#    pp = pprint.PrettyPrinter()
#    pp.pprint(get_typeform_data(True))
