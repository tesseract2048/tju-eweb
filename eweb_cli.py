#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @author:   hty0807@gmail.com
"""
import sys
from tjueweb.client import EWebClient

def printelem(ele):
    if isinstance(ele, dict):
        for key in ele:
            print '%s: %s' % (key, ele[key])
    elif isinstance(ele, list):
        for ele in ele:
            print '%s' % ele
    else:
        print '%s' % ele

def printarr(arr):
    i = 0
    for row in arr:
        print '=== Row %d ===' % i
        printelem(row)
        i += 1

def printr(arr):
    i = 0
    if not isinstance(arr, list):
        printelem(arr)
        return
    printarr(arr)

def readargument(prompt):
    sys.stdout.write('# %s: ' % prompt)
    return read()

def read():
    return sys.stdin.readline().strip()

def logout():
    cli.logoff()
    exit(0)

def menu():
    print '== EWebClient cli menu =='
    print '* 1. User info'
    print '* 2. Enroll result'
    print '* 3. Evaluate list'
    print '* 4. Evaluate'
    print '* 5. Achv terms'
    print '* 6. Achv'
    print '* 0. Exit'
    actions = {
        '1': lambda: cli.userinfo(),
        '2': lambda: cli.enrollresult(),
        '3': lambda: cli.evaluatelist(),
        '5': lambda: cli.evaluate(readargument('lessonid'), readargument('courseid'), readargument('unioncode'), readargument('score'), readargument('content')),
        '5': lambda: cli.achvterms(),
        '6': lambda: cli.achv(readargument('term')),
        '0': lambda: logout()
    }
    printr(actions[readargument("Type [0-6]")]())
    menu()

cli = EWebClient()

if not cli.login(readargument('uid'), readargument('password')):
    raise Exception("failed to log in")

menu()
