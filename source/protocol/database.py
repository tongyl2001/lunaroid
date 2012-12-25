# -*- coding: utf-8 -*-
import sqlite3


def initialize():
    context = sqlite3.connect('learn.db')
    cursor = context.cursor()
    cursor.execute("select count(*) from sqlite_master where name='talk'")
    cursor_fetchone = cursor.fetchone()
    print cursor_fetchone
    if cursor_fetchone[0] == 0:
        cursor.execute("create table talk(question,answer)")
        print 'Database created'
        context.commit()
    context.close()