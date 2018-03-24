#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 jkirchartz <me@jkirchartz.com>
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

# json_mungers['blackletter'] = {"A": "�",        "B": "�",
# "C": "ℭ",         "D": "�",         "E": "�",         "F": "�",
# "G": "�",         "H": "ℌ",         "I": "ℑ",         "J": "�",
# "K": "�",         "L": "�",         "M": "�",         "N":
# "�",         "O": "�",         "P": "�",         "Q": "�",
# "R": "ℜ",         "S": "�",         "T": "�",         "U": "�",
# "V": "�",         "W": "�",         "X": "�",         "Y":
# "�",         "Z": "ℨ",         "a": "�",         "b": "�",
# "c": "�",         "d": "�",         "e": "�",         "f":
# "�",         "g": "�",         "h": "�",         "i": "�",
# "j": "�",         "k": "�",         "l": "�",         "m":
# "�",         "n": "�",         "o": "�",         "p": "�",
# "q": "�",         "r": "�",         "s": "�",         "t":
# "�",         "u": "�",         "v": "�",         "w": "�",
# "x": "�",         "y": "�",         "z": "�"     }

json_mungers['russian'] = {
	"A": ["Д"],
	"B": ["Б", "Ъ", "Ь"],
	"C": ["Ҫ"],
	"E": ["Ԑ", "Є", "Э"],
	"F": ["Ӻ", "Ғ"],
	"H": ["Њ", "Ҥ", "Ӊ", "Ң"],
	"I": ["Ї"],
	"K": ["Қ", "Ҡ", "Ҝ", "Ԟ"],
	"M": ["Ԡ"],
	"N": ["И", "Ѝ", "Й"],
	"O": ["Ф"],
	"R": ["Я"],
	"T": ["Г", "Ґ", "Ҭ"],
	"U": ["Ц","Џ"],
	"W": ["Ш", "Щ"],
	"X": ["Ӿ", "Ҳ", "Ӽ", "Ж"],
	"Y": ["Ч", "Ұ"]
}

json_mungers['tiny'] = {
  "a":"ᵃ",
  "b":"ᵇ",
  "c":"ᶜ",
  "d":"ᵈ",
  "e":"ᵉ",
  "f":"ᶠ",
  "g":"ᵍ",
  "h":"ʰ",
  "i":"ᶦ",
  "j":"ʲ",
  "k":"ᵏ",
  "l":"ᶫ",
  "m":"ᵐ",
  "n":"ᶰ",
  "o":"ᵒ",
  "p":"ᵖ",
  "q":"ᑫ",
  "r":"ʳ",
  "s":"ˢ",
  "t":"ᵗ",
  "u":"ᵘ",
  "v":"ᵛ",
  "w":"ʷ",
  "x":"ˣ",
  "y":"ʸ",
  "z":"ᶻ",
  "A":"ᴬ",
  "B":"ᴮ",
  "C":"ᶜ",
  "D":"ᴰ",
  "E":"ᴱ",
  "F":"ᶠ",
  "G":"ᴳ",
  "H":"ᴴ",
  "I":"ᴵ",
  "J":"ᴶ",
  "K":"ᴷ",
  "L":"ᴸ",
  "M":"ᴹ",
  "N":"ᴺ",
  "O":"ᴼ",
  "P":"ᴾ",
  "Q":"ᑫ",
  "R":"ᴿ",
  "S":"ˢ",
  "T":"ᵀ",
  "U":"ᵁ",
  "V":"ⱽ",
  "W":"ᵂ",
  "X":"ˣ",
  "Y":"ʸ",
  "Z":"ᶻ",
  "`":"`",
  "~":"~",
  "!":"﹗",
  "@":"@",
  "#":"#",
  "$":"﹩",
  "%":"﹪",
  "^":"^",
  "&":"﹠",
  "*":"﹡",
  "(":"⁽",
  ")":"⁾",
  "_":"⁻",
  "-":"⁻",
  "=":"⁼",
  "+":"+",
  "{":"{",
  "[":"[",
  "}":"}",
  "]":"]",
  ":":"﹕",
  ";":"﹔",
  "?":"﹖",
}

json_mungers['upsidedown'] = {
  'A':'∀',
  'B':'𐐒',
  'C':'Ɔ',
  'E':'Ǝ',
  'F':'Ⅎ',
  'G':'פ',
  'H':'H',
  'I':'I',
  'J':'ſ',
  'L':'˥',
  'M':'W',
  'N':'N',
  'P':'Ԁ',
  'R':'ᴚ',
  'T':'⊥',
  'U':'∩',
  'V':'Λ',
  'Y':'⅄',
  'a':'ɐ',
  'b':'q',
  'c':'ɔ',
  'd':'p',
  'e':'ǝ',
  'f':'ɟ',
  'g':'ƃ',
  'h':'ɥ',
  'i':'ᴉ',
  'j':'ɾ',
  'k':'ʞ',
  'm':'ɯ',
  'n':'u',
  'p':'d',
  'q':'b',
  'r':'ɹ',
  't':'ʇ',
  'u':'n',
  'v':'ʌ',
  'w':'ʍ',
  '1':'Ɩ',
  '2':'ᄅ',
  '3':'Ɛ',
  '4':'ㄣ',
  '5':'ϛ',
  '6':'9',
  '7':'ㄥ',
  '8':'8',
  '9':'6',
  '0':'0',
  '.':'˙',
  ',':'\'',
  '\'':',',
  '"':',,',
  '`':',',
  '<':'>',
  '>':'<',
  '∴':'∵',
  '&':'⅋',
  '_':'‾',
  '?':'¿',
  '!':'¡',
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

