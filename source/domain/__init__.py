# -*- coding: utf-8 -*-
from source.domain import message
from source.handle import joke_handler, learn_handler

message.message_handler.append(joke_handler)
message.message_handler.append(learn_handler)