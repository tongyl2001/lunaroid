# -*- coding: utf-8 -*-
import sys

from domain.qq import QQ
from protocol.client import Client


def start():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    print 'System Encoding: ' + sys.getdefaultencoding()

    client_logon = Client('2519749218', 'lichking123').login()

    qq = QQ(client_logon)
    qq.load_groups()
    qq.handle_message()

    print 'Lunaroid was exited'