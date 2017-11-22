#!/usr/bin/env python

import os
from random import randrange as rrange

COLSIZ = 10
RDBMSs = {'s': 'sqlite', 'm': 'mysql', 'p': 'postgresql'}
DB_EXC = None


def setup():
    return RDBMSs[input('''
    Chose a database system:

    (M)ySQL
    (P)ostgreSQL
    (S)QLite

    Enter choice: ''').strip().lower()[0]]


def connect(db, dbName):
    global DB_EXC
    dbDir = '{0}_{1}'.format(db, dbName)

    if db == 'sqlite':
        try:
            import sqlite3
        except ImportError as e:
            print(e)
            return None

        DB_EXC = sqlite3
        if not os.path.isdir(dbDir):
            # 在当前文件夹下创建目录
            os.mkdir(dbDir)
        # 如果文件不存在，会自动在当前目录创建
        print(os.path.join(dbDir, dbName))
        # 相对路径
        conn = sqlite3.connect(os.path.join(dbDir, dbName))

    elif db == 'mysql':
        try:
            import pymysql
            DB_EXC = pymysql
        except ImportError as e:
            print('mysql:{}'.format(e))
            return None

        try:
            conn = pymysql.connect(host='localhost', port=3306,
                                   user='root', password='110',
                                   database=dbName)
        except DB_EXC.OperationalError as e:
            print('mysql:{}'.format(str(e)))
            conn = pymysql.connect(host='localhost', port=3306,
                                   user='root', password='110')
            cur = conn.cursor()
            try:
                cur.execute('drop database {}'.format(dbName))
            except Exception as e:
                pass
            cur.execute('crate database %s' % dbName)
            cur.execute("grant all on {0}.* to '{1}'@'localhost'".format(dbName, 'root)'))
            cur.commit()
            cur.close()
            conn.close()
            conn = pymysql.connect(host='localhost', port=3306,
                                   user='root', password='110',
                                   database=dbName)

    elif db == 'postgresql':
        try:
            import psycopg2
            DB_EXC = psycopg2
        except ImportError as e:
            return None

        try:
            conn = psycopg2.connect(host='localhost', port=5432,
                                    user='postgres', password='110',
                                    database=dbName)
        except DB_EXC.OperationalError as e:
            print('postgresql:{}'.format(str(e)))
            conn = psycopg2.connect(host='localhost', port=5432,
                                    user='postgres', password='110')
            # 不加这个就会有
            conn.autocommit = True
            cur = conn.cursor()
            try:
                cur.execute('drop database {}'.format(dbName))
            except DB_EXC.InternalError:
                pass
            cur.execute('create database {}'.format(dbName))
            cur.execute('grant all privileges on %s to %s' % (dbName, 'postgres'))
            # cur.commit()
            cur.close()
            conn.close()
            conn = psycopg2.connect(host='localhost', port=5432,
                                    user='postgres', password='110',
                                    database=dbName)

    else:
        return None
    return conn


def create(cur):
    try:
        cur.execute('''
            create table users (
            login varchar(8),
            uid integer,
            prid integer
            )
        ''')
    except DB_EXC.OperationalError as e:
        print(DB_EXC, str(e))
        drop(cur)
        create(cur)

drop = lambda cur: cur.execute('drop table users')

NAMES = (
    ('aaron', 8312), ('angela', 7603), ('dave', 7306),
    ('davina',7902), ('elliot', 7911), ('ernie', 7410),
    ('jess', 7912), ('jim', 7512), ('larry', 7311),
    ('leslie', 7808), ('melissa', 8602), ('pat', 7711),
    ('serena', 7003), ('stan', 7607), ('faye', 6812),
    ('amy', 7209),
)


def readName():
    pick = list(NAMES)

def main():
    db = setup()
    print("*** Connecting to %r database" % db)
    conn = connect(db, 'test')
    if not conn:
        print("\nERROR: %r not supported, exiting" % db)
        return None
    cur = conn.cursor()

    print("\n*** Creating users table")
    create(cur)


if __name__ == '__main__':
    main()
