tju-eweb
========

Client library for e.tju.edu.cn (tju-eweb) in Python.

## Install

### 从 python-pip 安装 (推荐)
``python-pip install tjueweb`` 或 ``pip install tjueweb``

### 从 source 安装
``python setup.py install``

## Supported

* Logging (登录)
* Achv (成绩查询)
* User info (用户信息)
* Evaluate (教学评价)
* Enroll Result (选课结果)
* A comannd line tool (命令行工具)

## Todo
* Enroll (选课)
* Schedule (课表)
* ...

## Example
```
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
```

## Cli

``python eweb_cli.py``

Menu:

```
# uid: 
# password: 
== EWebClient cli menu ==
* 1. User info
* 2. Enroll result
* 3. Evaluate list
* 4. Evaluate
* 5. Achv terms
* 6. Achv
* 0. Exit
# Type [0-6]: 
```