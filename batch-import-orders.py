#!/usr/bin/python
# coding:utf-8
import sys
import os
import json
import requests
import csv


# check input values below
base_url = 'http://localhost:4000'
login_email = 'yojee@development.com'
login_password = 'yojeedevelopment'
# this is the company slug of the sender
company_slug = 'yojee'
# this is the sender id
uploader_id = '515'
# this is the organisation id
company_id = '621'
# this is the user_profile_id for organisation senders
placed_by_user_profile_id = '1909'

# repository_id = raw_input('Enter repository_id to load into: ')
request_folder_name = raw_input('Enter request_folder_name to load from: ')

# check for request folder
if not os.path.exists(request_folder_name):
    print('Error! Folder ' + request_folder_name + ' does not exist. Exiting..')
    exit()

# check for csv folder
# csv_folder_name = 'csv'
# csv_folder_path = request_folder_name + '/' + csv_folder_name
csv_folder_path = request_folder_name
if not os.path.exists(csv_folder_path):
    print('Error! Folder ' + csv_folder_path + ' does not exist. Exiting..')
    exit()

# first login to get access token
request_url = base_url + '/api/v3/auth/signin'
headers = {'Content-Type': 'application/json'}
body = {'password': login_password, 'email': login_email}
response = requests.post(request_url, headers=headers, data=json.dumps(body))
# print(response.status_code, response.reason) #HTTP
# print(response.text) #RESPONSEBODY

response_json = json.loads(response.text)
if (response.status_code != 200):
    print('... error found! exiting program..')
    print(response.text)
    sys.exit()
access_token = response_json['data']['access_token']
print('... access_token (result) found: ' + access_token)

count = 0

def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]

for csv_file_name in mylistdir(csv_folder_path):
    count += 1
    #external_id = 'new'
    #container_no = 'test'
    file_name = os.path.splitext(csv_file_name)[0]
    external_id = file_name.split('-')[0]
    container_no = file_name.split('-')[1]
    print('### Processing item #' + str(count) + ' ' + csv_file_name + '.. ###')
    csv_path = csv_folder_path + '/' + csv_file_name
    if not os.path.exists(csv_path):
        print('Error! CSV file ' + csv_path +
              ' does not exist. Skipping item..')
        continue

    up = {'file': (csv_path, open(csv_path, 'rb'), "multipart/form-data")}
    site = base_url + '/api/v3/dispatcher/batches'
    params = {
        'uploader_id': uploader_id,
        'company_id': company_id,
        'placed_by_user_profile_id': placed_by_user_profile_id,
        'external_id': external_id,
        'container_no': container_no
    }
    headers = {
        'Accept': 'application/json',
        'access_token': access_token,
        'company_slug': company_slug,
    }
    # next send the import staff API request to the FP server
    response = requests.post(site, params=params, headers=headers, files=up)
    response_json = json.loads(response.text)
    if (response.status_code != 200):
        #print('... error found! Exiting program..')
        print('... error found! ')
        #sys.exit()
    print(response_json)
