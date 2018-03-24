#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 jkirchartz <me@jkirchartz.com>
#
# Distributed under terms of the NPL (Necessary Public License) license.

"""
use memegen.link to generate memes
"""

from cloudbot import hook
import requests
import json
import textwrap

memegen_link = "https://memegen.link/"

def sendline(text):
  return text

def fix_text(text):
    if (len(text) == 0):
      return '_'
    text = text.replace("-", "--")
    text = text.replace("_", "__")
    text = text.replace(" ", "_")
    text = text.replace("?", "~q")
    text = text.replace("%", "~p")
    text = text.replace("#", "~h")
    text = text.replace("/", "~s")
    text = text.replace("\"", "''")
    return text

@hook.command('mg', 'memegen')
def memegen(text):
    """mg <template>|<top text>|<bottom text> or mg custom|<top text>|<bottom text>|<image url> or mg examples or mg templates"""
    text = text.split('|')
    template = text[0]
    url = ""

    # if template == "templates":
    #   request = requests.get(memegen_link + "api/templates/")
    #   if request.status_code == 200:
    #     data = request.json()
    #     output = "Templates: "
    #     for key,value in data.items():
    #       item = value.split("/")[5]
    #       output += "" + key + " = '" + item + "', "
    #     return textwrap.wrap(output, width=350, break_long_words=False)
    #   return "error retreiving templates"

    if template == "examples":
      return "http://memegen.link/examples"

    if template == "templates":
      return "http://memegen.link/api/templates/"


    top = fix_text(text[1])
    bottom = fix_text(text[2])
    custom = text[3]

    if template == "custom":
      url = memegen_link + top + "/" + bottom + "/"
      if ("jpg" in custom or "png" in custom):
          url = memegen_link + ".jpg?watermark=none&alt=" + custom
      else:
        return "please provide a png or jpg for the custom template"
    else:
      url = memegen_link + template + "/" + top + "/" + bottom + "/?watermark=none"

    request = requests.get(url)
    if request.status_code == 200:
      data = request.json()
      return "Meme: " + data['direct']['visible']
    else:
      return "error generating meme"





