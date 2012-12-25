# -*- coding: utf-8 -*-
import json
import random
import re
from group import Group
import message


class QQ:
    def __init__(self, client_logon):
        self.token = client_logon['token']
        self.client = client_logon['client']
        self.groups = {}

    def load_groups(self):
        groups_url = 'http://s.web2.qq.com/api/get_group_name_list_mask2'
        data = {'r': open('json/load_groups.json').read() % self.token}
        headers = {"Referer": 'http://s.web2.qq.com/proxy.html?v=20110412001&callback=1&id=1'}
        response_of_load_group = self.client.post(groups_url, data=data, headers=headers)
        groups_data = json.loads(response_of_load_group.text)
        if groups_data['retcode'] == 0:
            for group_data in groups_data['result']['gnamelist']:
                group = Group(group_data, self.token, self.client)
                self.groups[group.id] = group
                print group_data
                group.message('闪亮登场!')

    def handle_message(self):
        while True:
            headers = {'Referer': 'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=3'}
            data = {
                'r': open('json/poll.json').read() % self.token,
                'clientid': self.token['client_id'],
                'psessionid': self.token['session_id']
            }
            response_of_poll = self.client.post('http://d.web2.qq.com/channel/poll2', data=data, headers=headers)
            messages_data = json.loads(response_of_poll.text)
            message.dispatch(messages_data, self)