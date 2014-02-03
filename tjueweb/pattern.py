#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @author:   hty0807@gmail.com
"""
import re
from handy import *

patterns = {
    "userinfo/rows": {
        'regex': """<TR *>[^<]+<TD( height="30"){0,1}>&nbsp;(?P<attr>[^<]+)：</TD>[^<]+<TD( height="30"){0,1}>(?P<value>[^<]+)</TD>[^<]+</TR>""",
        'fields': [
            ("attr", STRIP),
            ("value", STRIP)
        ]
    },
    "achv/terms": {
        'regex': """<a class="titlelink" href="/Education/stuachv\\.do\\?todo=display&term=(\\d+)" >""",
        'function': STRIP
    },
    "achv/courses": {
        'regex': """<tr align="center" bgcolor="#FFFFFF" height="25" valign="bottom">([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>(?P<term>\\d+)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>(?P<id>\\d+)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="left"><font class=ContextText2>(?P<name>[^<]*)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="left"><font class=ContextText2>(?P<coursetype>[^<]*)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>(?P<courseclass>[^<]*)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>(?P<credit>[^<]*)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>([^\\d]*)(?P<grading>\\d+)([^<]*)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>(?P<gradingtype>[^<]*)</font></td>([^<]*)<td class="(TableRowColor|TableAltRowColor2)"  align="center"><font class=ContextText2>(?P<comment>[^<]*)</font></td>([^<]*)</tr>""",
        'fields': [
            ("term", STRIP),
            ("id", STRIP),
            ("name", STRIP),
            ("coursetype", STRIP),
            ("courseclass", STRIP),
            ("credit", NUMERIC),
            ("grading", NUMERIC),
            ("gradingtype", STRIP),
            ("comment", STRIP)
        ]
    },
    "enroll/result": {
        'regex': """<tr height = "20" bgcolor="#FFFFFF">([^<]+)<td class="(TableRowColor|TableAltRowColor2)" align = "left"><font class="ContextText2">(?P<courseid>\\d+)</font></td>([^<]+)<td class="(TableRowColor|TableAltRowColor2)" align = "center"><font class="ContextText2">(?P<lessonid>\\d+)</font></td>([^<]+)<td class="(TableRowColor|TableAltRowColor2)" align = "left"><font class="ContextText2">(?P<name>[^<]*)</font></td>([^<]+)<td class="(TableRowColor|TableAltRowColor2)" align = "center"><font class="ContextText2">(?P<coursetype>[^<]*)</font></td>([^<]+)<td class="(TableRowColor|TableAltRowColor2)" align = "center"><font class="ContextText2">(?P<courseclass>[^<]*)</font></td>([^<]+)<td class="(TableRowColor|TableAltRowColor2)" align = "left"><font class="ContextText2">(?P<credit>[^<]*)</font></td>([^<]+)<td class="(TableRowColor|TableAltRowColor2)" align = "left"><font class="ContextText2">(?P<lecturer>[^<]*)</font></td>([^<]+)<td class="(TableRowColor|TableAltRowColor2)" align = "left"><font class="ContextText2">(?P<unioncode>[^<]*)([^<]+)</font>([^<]+)</td>([^<]+)<td class="(TableRowColor|TableAltRowColor2)" align = "left"><font class="ContextText2">(?P<plan>[^<]*)([^<]+)([^<]+)</font>([^<]+)</td>([^<]+)<td class="(TableRowColor|TableAltRowColor2)" align = "center"><font class="ContextText2">(?P<schedule>[^<]*)</font></td>([^<]+)<td class="(TableRowColor|TableAltRowColor2)" align = "center"><font class="ContextText2">(?P<department>[^<]*)</font></td>([^<]+)<td class="(TableRowColor|TableAltRowColor2)" align = "center">([^<]+)<font class="ContextText2">(?P<comment>[^<]*)([^<]+)([^<]+)([^<]+)([^<]+)</font>([^<]+)</td>([^<]+)([^<]+)</tr>""",
        'fields': [
            ("courseid", STRIP),
            ("lessonid", STRIP),
            ("name", STRIP),
            ("coursetype", STRIP),
            ("courseclass", STRIP),
            ("credit", NUMERIC),
            ("lecturer", STRIP),
            ("unioncode", STRIP),
            ("plan", STRIP),
            ("schedule", STRIP),
            ("department", STRIP),
            ("comment", STRIP)
        ]
    },
    "evaluate/rows": {
        'regex': """<a href="\\./evaluate\\.do\\?todo=detail&lesson_id=(?P<lessonid>\\d+)&union_id=(?P<unioncode>\\d+)&course_id=(?P<courseid>\\d+)" >[\\r\\n\\t ]+(?P<name>[^&]+)&nbsp;""",
        'fields': [
            ("lessonid", STRIP),
            ("courseid", STRIP),
            ("unioncode", STRIP),
            ("name", STRIP)
        ]
    },
    "evaluate/lecturers": {
        'regex': """<input type="radio" name="(\\d+)_4" value="100">""",
        'function': STRIP
    },
}

def extract(input, name):
    if name not in patterns:
        return None
    pattern = patterns[name]
    rows = []
    it = re.finditer(pattern['regex'], input, re.MULTILINE | re.DOTALL)
    for m in it:
        if 'fields' in pattern:
            row = {}
            for tup in pattern['fields']:
                key = tup[0]
                row[key] = tup[1](m.group(key))
            rows.append(row)
        else:
            rows.append(pattern['function'](m.group(1)))
    return rows
