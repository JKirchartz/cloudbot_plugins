#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright Â© 2018 jkirchartz <me@jkirchartz.com>
#
# Distributed under terms of the NPL (Necessary Public License) license.

from datetime import datetime
from cloudbot import hook
from cloudbot.event import EventType
import json
import random

mcache = dict()

# spongemock.py
# author: Noah Krim
# email: nkrim62@gmail.com

def mock(text, diversity_bias=0.5, random_seed=None):
	# Error handling
	if diversity_bias < 0 or diversity_bias > 1:
		raise ValueError('diversity_bias must be between the inclusive range [0,1]')
	# Seed the random number generator
	random.seed(random_seed)
	# Mock the text
	out = ''
	last_was_upper = True
	swap_chance = 0.5
	for c in text:
		if c.isalpha():
			if random.random() < swap_chance:
				last_was_upper = not last_was_upper
				swap_chance = 0.5
			c = c.upper() if last_was_upper else c.lower()
			swap_chance += (1-swap_chance)*diversity_bias
		out += c
	return out

# end spongemock

def vaporwave(text):
    output = ""
    for c in list(text):
        a = ord(c)
        if a >= 33 and a <= 126:
            output += chr( (a - 33) + 65281 )
        else:
            output += c
    return output


unicode_offsets = {
        "cursive": {"upper": 119951, "lower": 119945},
        "circle": {"upper": 9333, "lower": 9327}
        }

def unicode_offset(text, fun):
    output = ""
    for c in list(text):
        a = ord(c)
        if a > 64 and a < 91:
            output += chr( a + unicode_offsets[fun]["upper"] )
        elif a > 96 and a < 123:
            output += chr( a + unicode_offsets[fun]["lower"] )
        else:
            output += c
    return output

json_mungers = {}

# json_mungers['blackletter'] = {"A": "í´„",        "B": "í´…",
# "C": "â„­",         "D": "í´‡",         "E": "í´ˆ",         "F": "í´‰",
# "G": "í´Š",         "H": "â„Œ",         "I": "â„‘",         "J": "í´",
# "K": "í´Ž",         "L": "í´",         "M": "í´",         "N":
# "í´‘",         "O": "í´’",         "P": "í´“",         "Q": "í´”",
# "R": "â„œ",         "S": "í´–",         "T": "í´—",         "U": "í´˜",
# "V": "í´™",         "W": "í´š",         "X": "í´›",         "Y":
# "í´œ",         "Z": "â„¨",         "a": "í´ž",         "b": "í´Ÿ",
# "c": "í´ ",         "d": "í´¡",         "e": "í´¢",         "f":
# "í´£",         "g": "í´¤",         "h": "í´¥",         "i": "í´¦",
# "j": "í´§",         "k": "í´¨",         "l": "í´©",         "m":
# "í´ª",         "n": "í´«",         "o": "í´¬",         "p": "í´­",
# "q": "í´®",         "r": "í´¯",         "s": "í´°",         "t":
# "í´±",         "u": "í´²",         "v": "í´³",         "w": "í´´",
# "x": "í´µ",         "y": "í´¶",         "z": "í´·"     }

json_mungers['russian'] = {
	"A": ["Ð”"],
	"B": ["Ð‘", "Ðª", "Ð¬"],
	"C": ["Òª"],
	"E": ["Ô", "Ð„", "Ð­"],
	"F": ["Óº", "Ò’"],
	"H": ["ÐŠ", "Ò¤", "Ó‰", "Ò¢"],
	"I": ["Ð‡"],
	"K": ["Òš", "Ò ", "Òœ", "Ôž"],
	"M": ["Ô "],
	"N": ["Ð˜", "Ð", "Ð™"],
	"O": ["Ð¤"],
	"R": ["Ð¯"],
	"T": ["Ð“", "Ò", "Ò¬"],
	"U": ["Ð¦","Ð"],
	"W": ["Ð¨", "Ð©"],
	"X": ["Ó¾", "Ò²", "Ó¼", "Ð–"],
	"Y": ["Ð§", "Ò°"]
}

json_mungers['tiny'] = {
  "a":"áµƒ",
  "b":"áµ‡",
  "c":"á¶œ",
  "d":"áµˆ",
  "e":"áµ‰",
  "f":"á¶ ",
  "g":"áµ",
  "h":"Ê°",
  "i":"á¶¦",
  "j":"Ê²",
  "k":"áµ",
  "l":"á¶«",
  "m":"áµ",
  "n":"á¶°",
  "o":"áµ’",
  "p":"áµ–",
  "q":"á‘«",
  "r":"Ê³",
  "s":"Ë¢",
  "t":"áµ—",
  "u":"áµ˜",
  "v":"áµ›",
  "w":"Ê·",
  "x":"Ë£",
  "y":"Ê¸",
  "z":"á¶»",
  "A":"á´¬",
  "B":"á´®",
  "C":"á¶œ",
  "D":"á´°",
  "E":"á´±",
  "F":"á¶ ",
  "G":"á´³",
  "H":"á´´",
  "I":"á´µ",
  "J":"á´¶",
  "K":"á´·",
  "L":"á´¸",
  "M":"á´¹",
  "N":"á´º",
  "O":"á´¼",
  "P":"á´¾",
  "Q":"á‘«",
  "R":"á´¿",
  "S":"Ë¢",
  "T":"áµ€",
  "U":"áµ",
  "V":"â±½",
  "W":"áµ‚",
  "X":"Ë£",
  "Y":"Ê¸",
  "Z":"á¶»",
  "`":"`",
  "~":"~",
  "!":"ï¹—",
  "@":"@",
  "#":"#",
  "$":"ï¹©",
  "%":"ï¹ª",
  "^":"^",
  "&":"ï¹ ",
  "*":"ï¹¡",
  "(":"â½",
  ")":"â¾",
  "_":"â»",
  "-":"â»",
  "=":"â¼",
  "+":"+",
  "{":"{",
  "[":"[",
  "}":"}",
  "]":"]",
  ":":"ï¹•",
  ";":"ï¹”",
  "?":"ï¹–",
}

json_mungers['upsidedown'] = {
  'A':'âˆ€',
  'B':'ð’',
  'C':'Æ†',
  'E':'ÆŽ',
  'F':'â„²',
  'G':'×¤',
  'H':'H',
  'I':'I',
  'J':'Å¿',
  'L':'Ë¥',
  'M':'W',
  'N':'N',
  'P':'Ô€',
  'R':'á´š',
  'T':'âŠ¥',
  'U':'âˆ©',
  'V':'Î›',
  'Y':'â…„',
  'a':'É',
  'b':'q',
  'c':'É”',
  'd':'p',
  'e':'Ç',
  'f':'ÉŸ',
  'g':'Æƒ',
  'h':'É¥',
  'i':'á´‰',
  'j':'É¾',
  'k':'Êž',
  'm':'É¯',
  'n':'u',
  'p':'d',
  'q':'b',
  'r':'É¹',
  't':'Ê‡',
  'u':'n',
  'v':'ÊŒ',
  'w':'Ê',
  '1':'Æ–',
  '2':'á„…',
  '3':'Æ',
  '4':'ã„£',
  '5':'Ï›',
  '6':'9',
  '7':'ã„¥',
  '8':'8',
  '9':'6',
  '0':'0',
  '.':'Ë™',
  ',':'\'',
  '\'':',',
  '"':',,',
  '`':',',
  '<':'>',
  '>':'<',
  'âˆ´':'âˆµ',
  '&':'â…‹',
  '_':'â€¾',
  '?':'Â¿',
  '!':'Â¡',
  '[':']',
  ']':'[',
  '(':')',
  ')':'(',
  '{':'}',
  '}':'{'
}

def munger(text, json_type='russian'):
    output = ""
    json_munger = json_mungers[json_type]
    if json_type == 'russian':
        text = text.upper()
    for c in text:
        if c in json_munger:
            output += random.choice(json_munger[c])
        else:
            output += c
    return output

def munge(text, function='mock'):
    fun = function.lower()
    if fun == 'flip':
        fun = 'upsidedown'
        text = text[::-1]
    if fun == 'aesthetic' or fun == 'vaporwave':
        return vaporwave(text)
    elif fun == 'mock':
       return mock(text)
    # if fun == 'goth' or fun == 'fraktur':
    #     return json_munger(text, "blackletter");
    if fun == 'circled':
        return unicode_offset(text, "circle");
    elif fun in unicode_offsets:
       return unicode_offset(text, fun)
    elif fun in json_mungers:
       return munger(text, fun)
    else:
        return " ".join(["no munger named", fun])

@hook.on_start()
def load_key(bot):
    global buffer_size
    buffer_size = 1


@hook.event([EventType.message, EventType.action], ignorebots=True, singlethread=True)
def track(event, conn):
    if not str(event.content).startswith(('!', '.')):
        key = (event.chan, conn.name)
        mcache[key] = str(event.content)


@hook.command("munge", "m")
def munge_command(text, conn, chan):
    """!m(unge) circle, flip, vaporwave, mock, fake russian; works on either the last line of text in the channel, or any text placed after the munge style"""
    output = ""
    if len(text.split()) >= 2:
        text = text.split()
        output = munge(" ".join(text[1:]), text[0])
    else:
        try:
            if len(text):
                output = munge(mcache[(chan, conn.name)], text)
            else:
                output = munge(mcache[(chan, conn.name)])
        except KeyError:
            output = "Not Enough Messages."

    return output

