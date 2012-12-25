# -*- coding: utf-8 -*-
import execjs


class QQEncryptHelper:
    def __init__(self):
        self.qq_javascript = execjs.compile(open('javascript/qq.js').read())

    def calculate_password(self, login_token):
        md5_password = self.md5(login_token['password'])
        bin_password = self.hex_bin(md5_password)
        replace_ = bin_password + unicode(login_token['uin'].decode('iso-8859-1'))
        combined_password = self.md5(replace_)
        final_password = self.md5(combined_password + login_token['verify'].upper())
        return final_password

    def uin_hex(self, uin):
        return eval('\'' + uin + '\'')

    def hex_bin(self, hex):
        return self.qq_javascript.call('hexchar2bin', hex)

    def md5(self, to_be_md5):
        return self.qq_javascript.call('md5', to_be_md5)