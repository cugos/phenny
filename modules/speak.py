#!/usr/bin/env python

# Copyright 2008, Noah Slater <nslater@bytesexual.org>

# Copying and distribution of this file, with or without modification, are
# permitted in any medium without royalty provided the copyright notice and this
# notice are preserved.


import random
import re
import sys
import time
from os import path

import xapian

CONTEXT_DIRECTORY = "/home/aaronr/.phenny/context"
DATABASE_FILENAME = "/home/aaronr/.phenny/database"
STOP_LIST_FILENAME = "/home/aaronr/.phenny/list/stop.txt"
VOCABULARY_DIRECTORY = "/home/aaronr/.phenny/vocabulary"

THANKS_LIST = ["thanks", "thank you", "cheers"]

WELCOME_LIST = ["you're welcome", "don't mention it", "no problem", "np"]

LAUGH_LIST = ["haha", "hehe", "lol"]
START_LAUGH_LIST = LAUGH_LIST + ["ha", "heh"]
END_LAUGH_LIST = LAUGH_LIST + ["lmao", "rofl"]

STUMPED_LIST = ["hmm?", "huh?", "excuse me?", "sorry, what?","sudobangbang is an ass!"]

FLIRT_KEYWORD_LIST = [
    "sex", "flirt", "romance", "love", "girlfriend", "boyfriend", "cyber",
    "penis", "cock", "breast", "boobs", "tits", "horny", "porn", "fetish",
    "erotic", "bondage", "masturbate"
]

FLIRT_MESSAGE_LIST = [
    "what's your number?",
    "wanna have cybersex?",
    "can I have your email?",
    "does that turn you on?",
    "pm me and we can talk about it some more.",
    "at least, that's what you said last night.",
]

INSULT_KEYWORD_LIST = [
    "idiot", "stupid", "fucker", "arsehole", "simpleton", "luser",
    "looser",  "idiotic", "shit", "fail", "diaf", "foad", "shut up", "fool"
]

# "nub", "newbie", "noob", "n00b", "clueless",

INSULT_MESSAGE_LIST = [
    "and that, my friend, is why no one likes you.",
    "so shut up, please.",
    "please spare us your nonsense.",
    "sigh, not that I expect you to understand.",
    "you fail at life.",
    "someone should just kick you already.",
    "ugh, why am I wasting my energy on you.",
    "youre an idiot.",
]

# BAD_WORD_LIST= ["foo", "bar", "foobar"]

BAD_WORD_LIST= []

database = xapian.Database(DATABASE_FILENAME)
enquire = xapian.Enquire(database)
stemmer = xapian.Stem("english")
stopper = xapian.SimpleStopper()

for word in file(STOP_LIST_FILENAME):
    stopper.add(word.strip())

parser_strict = xapian.QueryParser()
parser_strict.set_database(database)
parser_strict.set_stopper(stopper)
parser_strict.set_stemmer(stemmer)
parser_strict.set_stemming_strategy(xapian.QueryParser.STEM_SOME)

parser_relaxed = xapian.QueryParser()
parser_relaxed.set_database(database)
parser_relaxed.set_stemmer(stemmer)
parser_relaxed.set_stemming_strategy(xapian.QueryParser.STEM_SOME)

def context(input):
    try:
        channel = input.sender.replace("#", "")
    except:
        return ""
    context_filename = path.join(CONTEXT_DIRECTORY, "%s.txt" % channel)
    context_file = file(context_filename, "a+")
    context = ""
    for line in context_file.read():
        for word in BAD_WORD_LIST:
            line = line.replace(word, "")
        context += line
    return " ".join(context.split())

def search(parser, input):
    database.reopen()
    token_list_size = len(input.split())
    query = parser.parse_query(input)
    enquire.set_query(query)
    result_list = enquire.get_mset(0, 200)
    if len(result_list) > 20:
        result_list = random.sample(result_list, 20)
    message_list = []
    word_list = []
    for result in result_list:
        message = result.document.get_data()
        if message in message_list:
            continue
        if len(message.split()) < 4:
            continue
        for word in BAD_WORD_LIST:
            message = message.replace(word, "bangbang")
        message_list.append(message)
        word_list = word_list + message.split()
    return message_list, word_list

def filter(input):
    input = re.compile(r"(?i)\bbangbang\b").sub("", input)
    input = input.replace("ACTION", "")
    for word in BAD_WORD_LIST:
        input = input.replace(word, "")
    return input

def clean_response(response):
    # fix grammatically incorrect response start
    response = re.compile(r"^and").sub("", response)
    response = re.compile(r"^then").sub("", response)
    response = re.compile(r"^but").sub("yes, but", response)
    # fix grammatically incorrect response content
    response = re.compile(r".[.!?] and").sub(" and", response)
    response = re.compile(r"[.!?] then").sub(" then", response)
    response = re.compile(r"[.!?] but").sub(" but", response)
    # fix grammatically incorrect response ending
    response = re.compile(r"[^.!?]$").sub(".", response)
    response = response.strip()
    return response

def response_add_self(response):
    if random.randint(1, 2) == 1:
        response = re.compile(
            r"(\ba\b )(\w+)(.*)").sub("\g<1>bangbang\g<3>", response)
    return response

def response_add_emotion(response):
    emotion_number = random.randint(1, 5)
    if emotion_number == 1:
        response = "%s, %s" % (random.choice(START_LAUGH_LIST), response)
    if emotion_number == 2:
        response = "%s %s" % (response, random.choice(END_LAUGH_LIST))
    return response

def _speak(phenny, message):
    token_count = len(message.split())
    time.sleep(token_count * 0.2)
    if phenny:
        phenny.say(message)
    else:
        print message
    return

def speak(phenny, input):
    if input.sender.startswith("#"):
        if not "bangbang" in input.lower(): return
    for thanks in THANKS_LIST:
        if input == "%s bangbang" % thanks:
            return _speak(phenny, random.choice(WELCOME_LIST))
    flirt_nick_list = re.compile(r"(?i).*(hit on|flirt with) ([^ ]+)").findall(input)
    flirt_nick = None
    if flirt_nick_list:
        flirt_nick = flirt_nick_list[0][1]
        input = " ".join(FLIRT_KEYWORD_LIST)
    insult_nick_list = re.compile(r"(?i).*(insult|flame) ([^ ]+)").findall(input)
    insult_nick = None
    if insult_nick_list:
        insult_nick = insult_nick_list[0][1]
        input = " ".join(INSULT_KEYWORD_LIST)
    filtered_input = filter(input)
    search_message_list, search_word_list = search(parser_strict, filtered_input)
    if len(search_message_list) < 10:
        filtered_input = "%s %s" % (filtered_input, context(input))
        filtered_input = filter(filtered_input)
        search_message_list, search_word_list = search(parser_relaxed, filtered_input)
    if not search_word_list:
        return _speak(phenny, random.choice(STUMPED_LIST))
    end_sentence_list = []
    markov_dict = {}
    previous_word_a = ""
    previous_word_b = ""
    for word in search_word_list:
        if previous_word_a != "" and previous_word_b != "":
            key = (previous_word_b, previous_word_a)
            if markov_dict.has_key(key):
                markov_dict[key].append(word)
            else:
                markov_dict[key] = [word]
                if previous_word_a[-1] in (",", ".", "!", "?"):
                    end_sentence_list.append(key)
        previous_word_b = previous_word_a
        previous_word_a = word
    if not end_sentence_list:
        return _speak(phenny, random.choice(STUMPED_LIST))
    key = ()
    count = 2
    message_list = [[]]
    while 1:
        if markov_dict.has_key(key):
            word = random.choice(markov_dict[key])
            message_list[len(message_list) - 1].append(word)
            key = (key[1], word)
            if word[-1] in (",", ".", "!", "?"):
                count = count - 1
                message_list.append([])
                if count <= 0:
                    break
        else:
            key = random.choice(end_sentence_list)
    word_list = []
    start_list_list = []
    # stop the repetition of messages
    for message in message_list:
        if message[:3] in start_list_list:
            continue
        start_list_list.append(message[:3])
        word_list += message
    response = " ".join(word_list)
    response = clean_response(response)
    if flirt_nick:
        response = "%s, %s %s" % (
            flirt_nick, response, random.choice(FLIRT_MESSAGE_LIST))
    if insult_nick:
        response = "%s, %s %s" % (
            insult_nick, response, random.choice(INSULT_MESSAGE_LIST))
    else:
        pass
        #response = response_add_self(response)
        #response = response_add_emotion(response)
    return _speak(phenny, response)

speak.rule =  r".*"
speak.priority = "low"
speak.thread = False

if __name__ == "__main__":
    speak(None, " ".join(sys.argv[1:]))
