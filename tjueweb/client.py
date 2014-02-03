#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @author:   hty0807@gmail.com
"""
from httputils import WebClient
from format import fmtattr
from pattern import extract
import re

class EWebClient():

    def __init__(self):
        self.client = WebClient()
        self.logged = False
        self.uid = None
        self.password = None

    def request(self, url, withsession=True, **args):
        resp = self.client.request(url, **args)
        if not withsession:
            return resp
        while resp.find(self.uid) < 0:
            if not self.login(self.uid, self.password):
                return None
            resp = self.client.request(url, **args)
        return resp

    ''' attempt to log in with specified authentication '''
    ''' returns true if succeed '''
    def login(self, uid, password):
        # logging in
        resp = self.request("http://e.tju.edu.cn/Main/logon.do", False, data={'uid':uid, 'password':password})
        # if logging is a success, page would contain uid
        if resp.find(uid) < 0:
            return False
        self.logged = True
        self.uid = uid
        self.password = password
        return True

    ''' destroy session '''
    def logoff(self):
        self.request("http://e.tju.edu.cn/Main/logoff.do", False)
        self.logged = False
        return True

    ''' get a list of enrolled courses '''
    def enrollresult(self):
        resp = self.request("http://e.tju.edu.cn/Education/stuslls.do?todo=result")
        return extract(resp, 'enroll/result')

    ''' get a list of evaluate courses '''
    def evaluatelist(self):
        resp = self.request("http://e.tju.edu.cn/Education/evaluate.do?todo=list")
        return extract(resp, 'evaluate/rows')

    ''' get a list of evaluate courses '''
    def evaluate(self, lessonid, courseid, unioncode, score=100, content=''):
        resp = self.request("http://e.tju.edu.cn/Education/evaluate.do?todo=detail&lesson_id=%s&union_id=%s&course_id=%s" % (lessonid, unioncode, courseid))
        fields = {"lesson_id": lessonid, "course_id": courseid, "union_id": unioncode, "sumScore": score, "evaluateContent": content, "evaluate_type": 1}
        for lecturer in extract(resp, 'evaluate/lecturers'):
            for i in range(1, 5):
                fields["%s_%s" % (lecturer, i)] = score
        resp = self.request("http://e.tju.edu.cn/Education/evaluate.do?todo=Submit", data=fields)
        return True

    ''' fetch basic info for current user '''
    def userinfo(self):
        resp = self.request("http://e.tju.edu.cn/UserInfo/UserBasicInfo.do")
        info = {}
        for row in extract(resp, 'userinfo/rows'):
            attr = fmtattr(row['attr'], row['value'])
            info[attr[0]] = attr[1]
        return info

    ''' get a list of available terms '''
    def achvterms(self):
        resp = self.request("http://e.tju.edu.cn/Education/stuachv.do")
        return extract(resp, 'achv/terms')

    ''' get course info of specified term '''
    def achv(self, term):
        resp = self.request("http://e.tju.edu.cn/Education/stuachv.do?todo=display&term=%s" % term)
        return extract(resp, 'achv/courses')
