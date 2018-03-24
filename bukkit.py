#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 jkirchartz <me@jkirchartz.com>
#
# Distributed under terms of the NPL (Necessary Public License) license.


from cloudbot import hook
from cloudbot.util import web
import requests
import urllib
import random
from pyquery import PyQuery as pq

@hook.on_start()
def loadBukkit():
    global BUKKIT
    imgdata = pq("http://bukk.it/")
    for img in imgdata('tr > td > a'):
        BUKKIT.append(img.attrib['href'])


@hook.command('b', 'bukkit')
def bukkit(text):
    text = text.strip()
    output = ""
    if len(text) == 0:
        output = random.choice(BUKKIT)
    else:
        matching = [s for s in BUKKIT if text.upper() in s.upper()]
        if len(matching):
            output = random.choice(matching)
        else:
            output = " doesn't have anything like that..."

    return "http://bukk.it/" + output






