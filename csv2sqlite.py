#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Imports csv file to sqlite db

@author: ketil
"""
import sys
import csv
import sqlite3


def usage():
    app = sys.argv[0].split("/")[-1]
    print(f'Usage {app} filename.csv filename.sqlite')
    print('The tablename inferred from filename is not safe against '
          'SQL-injections')


def main(csv_f, sqlite_f):
    conn = sqlite3.connect(sqlite_f)
    cursor = conn.cursor()

    tablename = csv_f.split('/')[-1].split('.')[0]
    with open(csv_f) as f:
        c = csv.reader(f)
        col = next(c)
        question = ','.join(['?'] * len(col))
        column_names = ','.join(col)

        sql = f'CREATE TABLE  IF NOT EXISTS {tablename} ({column_names})'
        cursor.execute(sql)

        for line in c:
            sql = f'INSERT INTO {tablename} VALUES ({question})'
            cursor.execute(sql, line)
        conn.commit()
        conn.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
    else:
        main(sys.argv[1], sys.argv[2])
