# -*- coding: utf-8 -*-

message_handler = list()


def dispatch(messages_data, qq):
    if messages_data['retcode'] == 0:
        polls = messages_data['result']
        for poll in polls:
            message = create_message(poll)
            for handler in message_handler:
                handler.handle(message, qq)
    else:
        print messages_data


def create_message(poll):
    if poll['poll_type'] == 'group_message':
        value = poll['value']
        message = GroupMessage()
        message.reply_ip = value['reply_ip']
        message.group_code = value['group_code']
        message.seq = value['seq']
        message.send_uin = value['send_uin']
        message.from_uin = value['from_uin']
        message.to_uin = value['to_uin']
        message.info_seq = value['info_seq']
        message.msg_id = value['msg_id']
        message.time = value['time']
        message.font = create_front(value['content'][0])
        message.contents = create_content(value['content'])
        return message


class GroupMessage:
    def __init__(self):
        self.reply_ip = None
        self.group_code = None
        self.seq = None
        self.send_uin = None
        self.from_uin = None
        self.to_uin = None
        self.info_seq = None
        self.msg_id = None
        self.time = None
        self.font = None
        self.content = None


def create_content(contents):
    message_contents = list()
    for content in contents:
        if type(content) == list:
            continue
        message_contents.append(content.strip())
    return message_contents


def create_front(font):
    if font[0] == 'font':
        font_data = font[1]
        return Font(font_data['color'], font_data['style'], font_data['name'], font_data['size'])
    else:
        return Font()


class Font:
    def __init__(self, color='000000', style=[0, 0, 0], name='宋体', size=9):
        self.color = color
        self.style = style
        self.name = name
        self.size = size

