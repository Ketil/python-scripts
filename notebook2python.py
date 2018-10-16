#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module/script to convert convert jupyter notebook v4 to a python script.

@author: ketil
"""

import json

def export(infile, outfile='outfile.py'):
    '''Saves the codeblocks from a ipynb v4 document to outfile.'''
    with open(infile, 'r') as stream:
        data = json.load(stream)

    with open(outfile, 'w') as stream:
        for i, cell in enumerate([i['source'] for i in data['cells']
                                  if i['cell_type'] == 'code']):
            stream.write(f'# block {i}\n')
            stream.writelines(cell)
            stream.write('\n\n')


if __name__ == '__main__':
    import sys

    ARGC = len(sys.argv)
    if ARGC == 1:
        print(f'usage: sys.argv[0] infile [outfile]')
    else:
        INFILE = sys.argv[1]
        OUTFILE = 'outfile.py'
        if ARGC >= 3:
            OUTFILE = sys.argv[2]
        export(INFILE, OUTFILE)
        sys.exit(0)
