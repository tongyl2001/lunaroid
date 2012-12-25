# -*- coding: utf-8 -*-
import re
import sqlite3


def handle(message, qq):
    for content in message.contents:
        print content
        re_match = re.match('\@luna (.*) (.*)', content)
        if re_match:
            match_groups = re_match.groups()
            context = sqlite3.connect('learn.db')
            cursor = context.cursor()
            cursor.execute('''insert into talk (question, answer) values('%(question)s','%(answer)s')''' % {'question': match_groups[0], 'answer': match_groups[1]})
            context.commit()
            print 'Q&A updated'
        else:
            context = sqlite3.connect('learn.db')
            cursor = context.cursor()
            cursor.execute('''select answer from talk where question = '%(question)s' ''' % {'question': content})
            cursor_fetchone = cursor.fetchone()
            if cursor_fetchone is not None:
                qq.groups[message.from_uin].message(cursor_fetchone[0])
            else:
                print 'Q&A not found'
