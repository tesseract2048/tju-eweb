tju-eweb
========

Client for e.tju.edu.cn (eweb) in Python, including support for various modules

## Supported Modules

* Logging (登录)
* Achv (成绩查询)
* User info (用户信息)

## TODO
* Evaluate (教学评价)
* Enroll (选课)
* ...


## Demo
```
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @author:   hty0807@gmail.com
"""
from eweb.client import EWebClient

cli = EWebClient()

# 登录办公网
if not cli.login('/* UID */', '/* PASSWORD */'):
    raise Exception("failed to log in")

# 获取用户基本信息
print cli.userinfo()

```