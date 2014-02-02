#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @author:   hty0807@gmail.com
"""
from httputils import WebClient
import re

class EWebClient():

    def __init__(self):
        self.client = WebClient()

    ''' attempt to log in with specified authentication '''
    ''' returns true if succeed '''
    def login(self, uid, password):
        # logging in
        resp = self.client.request("http://e.tju.edu.cn/Main/logon.do", data={'uid':uid, 'password':password})
        # if logging is a success, page would contain uid
        if resp.find(uid) < 0:
            return False
        return True

    def logoff(self):
        self.client.request("http://e.tju.edu.cn/Main/logoff.do")
        return True

    def attr(self, attr, val):
        tbl = {'学号': ('id', lambda x: x), '姓名': ('name', lambda x: x), 
            '性别': ('gender', lambda x: 'Male' if x == '男' else 'Female'),
            '出生年月': ('bday', lambda x: x), '年级': ('year', lambda x: x), 
            '专业': ('major', lambda x: x), '班级': ('class', lambda x: x), 
            '身份证号': ('ssn', lambda x: x), '编号': ('id', lambda x: x), 
            '单位': ('depart', lambda x: x), '部门': ('staffroom', lambda x: x), 
            '办公电话': ('officetel', lambda x: x), '家庭电话': ('hometel', lambda x: x),
            '移动电话': ('mobile', lambda x: x), '电子邮件': ('email', lambda x: x)
        }
        if attr not in tbl:
            return attr, val
        entry = tbl[attr]
        return entry[0], entry[1](val)

    def userinfo(self):
        resp = self.client.request("http://e.tju.edu.cn/UserInfo/UserBasicInfo.do")
        p = re.compile("""<TR *>[^<]+<TD( height="30"){0,1}>&nbsp;([^<]+)：</TD>[^<]+<TD( height="30"){0,1}>([^<]+)</TD>[^<]+</TR>""", re.MULTILINE | re.DOTALL)
        info = {}
        for mch in p.findall(resp):
            attr = self.attr(mch[1].strip(), mch[3])
            info[attr[0]] = attr[1]
        return info

    ''' get a list of available terms '''
    def achvterms(self):
        resp = self.client.request("http://e.tju.edu.cn/Education/stuachv.do")
        p = re.compile("""<a class="titlelink" href="/Education/stuachv\\.do\\?todo=display&term=(\\d+)" >""")
        return p.findall(resp)

    ''' get course info of specified term '''
    def achvcourses(self, term):
        resp = self.client.request("http://e.tju.edu.cn/Education/stuachv.do?todo=display&term=%s" % term)
        p = re.compile("""<tr align="center" bgcolor="#FFFFFF" height="25" valign="bottom">([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>(\\d+)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>(\\d+)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="left"><font class=ContextText2>([^<]*)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="left"><font class=ContextText2>([^<]*)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>([^<]*)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>([^<]*)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>([^\\d]*)(\\d+)([^<]*)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>([^<]*)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>([^<]*)</font></td>([^<]*)</tr>""", re.MULTILINE | re.DOTALL)
        courses = []
        for mch in p.findall(resp):
            course = {"id": mch[5].strip(), 
                "name": mch[8].replace("&nbsp;", " ").strip(), 
                "coursetype": mch[11].strip(),
                "courseclass": mch[14].strip(),
                "credit": float(mch[17].strip()),
                "grading": float(mch[21].strip()),
                "gradingtype": mch[26].strip(),
                "comment": mch[28].strip(),
                }
            courses.append(course)
        return courses
