# -*- coding: utf-8 -*-
import json
import random
import re


def handle(message, qq):
    if message is None:
        return
    for content in message.contents:
        joke_request_matches = re.match('(.{0,5})是什么\?'.decode('utf-8'), content)
        if joke_request_matches:
            target_name = joke_request_matches.group(1)
            jokes_data = json.loads(open('json/jokes.json').read())
            jokes = jokes_data['jokes']
            joke = jokes[random.randint(0, len(jokes) - 1)]
            random.seed()
            print joke
            qq.groups[message.from_uin].message(joke % {'name': target_name})