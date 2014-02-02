#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @author:   hty0807@gmail.com
"""
from eweb.client import EWebClient

cli = EWebClient()

if not cli.login('/* UID */', '/* PASSWORD */'):
    raise Exception("failed to log in")

print cli.userinfo()
