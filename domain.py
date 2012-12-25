# -*- coding: utf-8 -*-
import json
import random
import re
import time


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
            if messages_data['result']:
                for message_data in messages_data['result']:
                    if message_data['poll_type'] == 'group_message':
                        content = message_data['value']['content']
                        print content
                        joke_request_matches = re.match('(.{0,5})是什么\?'.decode('utf-8'), content[len(content)-1])
                        if joke_request_matches:
                            target_name = joke_request_matches.group(1)
                            jokes_data = json.loads(open('json/jokes.json').read())
                            jokes = jokes_data['jokes']
                            joke = jokes[random.randint(0, len(jokes) - 1)]
                            random.seed()
                            print joke
                            self.groups[message_data['value']['from_uin']].message(joke % {'name': target_name})
            else:
                print messages_data


class Group:
    def __init__(self, group_data, token, client):
        self.id = group_data['gid']
        self.name = group_data['name']
        self.client = client
        self.token = token.copy()

    def message(self, message):
        self.token['message'] = message
        self.token['group_id'] = self.id
        headers = {'Referer': 'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=3'}
        data = {
            'r': open('json/send_group_message.json').read() % self.token,
            'clientid': self.token['client_id'],
            'psessionid': self.token['session_id']
        }
        print data
        response_for_send_group_message = self.client.post('http://d.web2.qq.com/channel/send_qun_msg2', data=data, headers=headers)
        print response_for_send_group_message.text