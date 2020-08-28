#!/bin/python3
# -*- coding:utf-8 -*-

import datetime
import fnmatch
import re

KST = datetime.timezone(datetime.timedelta(hours=9))

with open("hosts.txt", "r", encoding="utf-8") as _fr:
    hosts = sorted([x for x in _fr.readlines() if x is not None and len(x) > 0])

with open("hosts.txt", "w", encoding="utf-8") as _fw:
    _fw.writelines(hosts)

with open("only-stackoverflow.tmpl", "r", encoding="utf-8") as _fr:
    tmpl = _fr.read()

with open("only-stackoverflow.txt", "w", encoding="utf-8") as _fw:
    regex_list = []
    for host in hosts:
        re_str = fnmatch.translate(host.rstrip())
        re_match = re.match(r'\(\?s:(.*?)\)\\Z', re_str)
        if re_match is None:
            regex_list.append(re_str)
        else:
            regex_list.append(re_match[1])

    _fw.write(
        tmpl.format(
            version=datetime.datetime.now(KST).strftime("%Y.%m.%d.%H.%M"),
            regex="|".join(regex_list).strip('|'),
        )
    )