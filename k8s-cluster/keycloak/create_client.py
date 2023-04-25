import requests
import argparse
import ast

def get_token():

    url = 'http://217.28.220.13:32668/realms/master/protocol/openid-connect/token'

    params = {

        'client_id': 'admin-cli',
        'grant_type': 'password',
        'username' : 'admin',
        'password': 'admin'
    }
    x = requests.post(url, params, verify=False).content.decode('utf-8')
    print (x)
    print ('\n')
    return ast.literal_eval(x)['access_token']
    #return requests.post(url, params, verify=False).content.decode('utf-8')