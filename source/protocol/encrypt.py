# -*- coding: utf-8 -*-
import execjs

qq_javascript = execjs.compile(open('javascript/qq.js').read())


def calculate_password(login_token):
    md5_password = md5(login_token['password'])
    bin_password = hex_bin(md5_password)
    replace_ = bin_password + unicode(login_token['uin'].decode('iso-8859-1'))
    combined_password = md5(replace_)
    final_password = md5(combined_password + login_token['verify'].upper())
    return final_password

def uin_hex(uin):
    return eval('\'' + uin + '\'')


def hex_bin(hex):
    return qq_javascript.call('hexchar2bin', hex)


def md5(to_be_md5):
    return qq_javascript.call('md5', to_be_md5)