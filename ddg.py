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


@hook.command()
def ddg(text):
    params = urllib.parse.urlencode({'q':text,'format':'json','no_html':1, 'no_redirect': 1})
    output = ""
    request = requests.get("http://api.duckduckgo.com/?"+params)
    data = None
    if request.status_code == 200:
      data = request.json()

    print(data)

    if data["Abstract"]:
        output = [data["Abstract"], data["AbstractURL"]]
    elif data["AbstractText"]:
        output = [data["AbstractText"], data["AbstractURL"]]
    elif data["Heading"]:
        output = ' '.join([data["Heading"], ':', data["AbstractURL"]])
    elif data["Definition"]:
        output += data["Definition"]
    elif data["Answer"]:
        output += data["Answer"]
    elif data["Redirect"]:
        output += data["Redirect"]
    else:
        output += "DO YOUR OWN RESEARCH! "

    if output is "DO YOUR OWN RESEARCH! ":
        output += "".join([" https://duckduckgo.com/?", urllib.parse.urlencode({'q':text})])

    return output






