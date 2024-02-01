import argparse


userData = {
    'postflag': '1',
    'cmd': 'login',
    'role': '0',
}

parser = argparse.ArgumentParser(description='Upate UserData.')
parser.add_argument('id', type=int, help="Your xuehao")
parser.add_argument('--passwd', type=str, default='123456', help="Your passwd")
parser.add_argument('--secretKey', default=r'%CC%E1%BD%BB', help="secretKey")
parser.add_argument('--secretValue', default='%B5%C7%C2%BC',
                    help="secretValue")
args = parser.parse_args()
user = args.__dict__
if len(str(user['id'])) != 10:
    raise Exception('学号不对！')
userData.update({'xuehao': user['id'], 'password': user['passwd']})
userData.update({user['secretKey']: user['secretValue']})
print(userData)
