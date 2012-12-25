# -*- coding: utf-8 -*-
import io
import json
import os
import random
import re
import requests
from encrypt import QQEncryptHelper

TEMP_VERIFY_JPG = 'temp_verify.jpg'

VERIFY_CODE_URL = 'http://captcha.qq.com/getimage?aid=1003903&r=0.7122716559097171&uin=%(account)s'

FIRST_LOGIN_URL = 'http://ptlogin2.qq.com/login?u=%(account)s@qq.com&p=%(password)s&verifycode=%(verify)s&webqq_type=10&remember_uin=1&login2qq=1&aid=1003903&u1=http%%3A%%2F%%2Fweb.qq.com%%2Floginproxy.html%%3Flogin2qq%%3D1%%26webqq_type%%3D10&h=1&ptredirect=0&ptlang=2052&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=3-13-32205&mibao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10014&login_sig=uv3TE9D1JTJx*lFE04oxa94oplHaRF9LlA*m7LtHYPjBlz6qQRei7GLrK2UODZqN'

VERIFIED_CHECK_RESPONSE_REGEX = '''ptui_checkVC\('1','(.*)','(.*)'\);'''

CHECK_RESPONSE_REGEX = r'''ptui_checkVC\('0','(.*)','(.*)'\);'''

LOGIN_CHECK_URL = 'http://check.ptlogin2.qq.com/check?uin=%(account)s&appid=1003903'


class Client:
    def __init__(self, account, password):
        self.login_token = {'client_id': random.randint(0, 100000), 'account': account, 'password': password}
        self.client = requests.session()
        self.encrypt = QQEncryptHelper()

    def login(self):
        login_check_url = LOGIN_CHECK_URL % self.login_token
        response_of_check = self.client.get(login_check_url)
        print self.login_token

        match_non_verified_picture = re.match(CHECK_RESPONSE_REGEX, response_of_check.text)
        if match_non_verified_picture:
            groups = match_non_verified_picture.groups()
            if groups:
                self.login_token['verify'] = groups[0]
                self.login_token['uin'] = self.encrypt.uin_hex(groups[1])

        match_non_verified_picture = re.match(VERIFIED_CHECK_RESPONSE_REGEX, response_of_check.text)
        if match_non_verified_picture:
            groups = match_non_verified_picture.groups()
            if groups:
                self.login_token['uin'] = self.encrypt.uin_hex(groups[1])
                response_of_verify_picture = self.client.get(VERIFY_CODE_URL % self.login_token, stream=True)
                self.show_verify_picture(response_of_verify_picture)
                self.login_token['verify'] = raw_input('Please input verify code:')

        self.login_token['password'] = self.encrypt.calculate_password(self.login_token)

        response_of_first_login = self.client.get(FIRST_LOGIN_URL % self.login_token)
        self.login_token['web_qq_id'] = response_of_first_login.cookies['ptwebqq']

        if response_of_first_login.text.startswith('''ptuiCB('0','0'''):
            headers = {'Referer': 'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=3'}
            data = {
                'r': open('json/login_request.json').read() % self.login_token,
                'clientid': self.login_token['client_id'],
                'psessionid': 'null'
            }
            response_of_second_login = self.client.post('http://d.web2.qq.com/channel/login2', data=data, headers=headers)

            login_data = json.loads(response_of_second_login.text)
            self.login_token['session_id'] = login_data['result']['psessionid']
            self.login_token['runtime_id'] = login_data['result']['vfwebqq']

            return {'token': self.login_token, 'client': self.client}


    def show_verify_picture(self, response_of_verify_picture):
        verify_picture = io.open(TEMP_VERIFY_JPG, 'wb')
        verify_picture.write(response_of_verify_picture.raw.data)
        verify_picture.close()
        os.popen('open ' + TEMP_VERIFY_JPG)


