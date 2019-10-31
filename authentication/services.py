from . import queries as q
from collections import OrderedDict
from app import db as conn
from app import app
import shared.sharedservices as services

import os
# Fetch the data from the DB by user name
# Check and validate the data
# Send the unformatted data to the function to convert into formatted json
def fetchdata(username):
    #     data = []
    params = {
        'var_username': username
    }
    data = services.generic_database_connect(q.selectuserprofile, params)
    if data is not None:
        if len(data) == 0:
            return 401
        else:
            return data_compression(data)
    else:
        return 401

# Generate the new password for the user by sending  email and password
def createPassword(Email, password):
    params = {
        'var_email_add': Email,
        'var_password': password
    }
    return services.generic_database_update(q.UpdatePassword, params)


# Replace HTML Variables from the keyvaluepair Dictionary
def get_email_text(keyvaluepair, filename):
    try:
        f = open('/opt/temp' + filename, 'rU')
        emailtext = ""

        for line in f:
            emailtext += line

        for key, value in keyvaluepair.items():
            emailtext = emailtext.replace(key, value)

        return emailtext
    except Exception as e:
        print(str(e))
        return ""

def getRequestedUserData(id):
    params = {
        'var_user_id': id
    }

    return services.generic_database_connect(q.fetchDataByUserID, params)

# Create the JSON object of user data and returns
def data_compression(data):
    email_address = data[0]['email_address']
    username = data[0]['username']
    name = data[0]['name']
    password = data[0]['password']
    JsonData = {}
    
    JsonData['password'] = password
    JsonData['email_address'] = email_address
    JsonData['name'] = name
    JsonData['user_name'] = username
    return JsonData


# To serialize the return values in JSON
def getJson():
    with conn.cursor() as cursor:
        return [dict((cursor.description[i][0], value)
                     for i, value in enumerate(row)) for row in cursor.fetchall()]
