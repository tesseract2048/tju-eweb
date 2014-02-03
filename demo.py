#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @author:   hty0807@gmail.com
"""
from tjueweb.client import EWebClient

cli = EWebClient()

# 登录办公网
if not cli.login('/* UID */', '/* PASSWORD */'):
    raise Exception("failed to log in")

# 获取用户基本信息
print cli.userinfo()

# 获取选课结果
print cli.enrollresult()

# 获取待评价课程列表
for row in cli.evaluatelist():
    # 评价课程
    cli.evaluate(row['lessonid'], row['courseid'], row['unioncode'], 80, 'pretty good')

# 获取有成绩的学期列表
for term in cli.achvterms():
    # 获得成绩
    print cli.achv(term)

# 退出登录
cli.logoff()
