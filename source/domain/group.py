# -*- coding: utf-8 -*-


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