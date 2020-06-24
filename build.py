#!/bin/python3
# -*- coding:utf-8 -*-

import io
import re
import datetime

with open("hosts.txt", "r", encoding="utf-8") as _fr:
    hosts = _fr.readlines()

with open("only-stackoverflow.tmpl", "r", encoding="utf-8") as _fr:
    tmpl = _fr.read()

with open("only-stackoverflow.txt", "w", encoding="utf-8") as _fw:
    _fw.write(
        tmpl.format(
            version=datetime.datetime.now().strftime("%Y.%m.%d.%H.%M"),
            regex="|".join([re.escape(host.strip("\r\n")) for host in hosts]),
        )
    )

