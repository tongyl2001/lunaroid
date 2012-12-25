# -*- coding: utf-8 -*-
from domain.qq import QQ
from protocol import client
from source.protocol import database


def start():
    database.initialize()

    qq_client = client.create_client('2519749218', 'lichking123')
    qq = QQ(qq_client.login())
    qq.load_groups()
    qq.handle_message()

    print 'Lunaroid was exited'