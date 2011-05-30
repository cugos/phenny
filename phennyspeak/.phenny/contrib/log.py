#!/usr/bin/env python

# Copyright 2008, Noah Slater <nslater@bytesexual.org>

# Copying and distribution of this file, with or without modification, are
# permitted in any medium without royalty provided the copyright notice and this
# notice are preserved.

import os
import shutil
import re
import sys
import unicodedata
from os import path

import xapian

CONTEXT_DIRECTORY = "~/.phenny/context"
DATABASE_FILENAME = "~/.phenny/database"
VOCABULARY_DIRECTORY = "~/.phenny/vocabulary"

OBSCENITY_LIST = ["nigger", "nigra", "cunt", "fag", "faggot", "faggit"]

def index(message):
    database = xapian.WritableDatabase(DATABASE_FILENAME, xapian.DB_CREATE_OR_OPEN)
    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)
    doc = xapian.Document()
    doc.set_data(message)
    indexer.set_document(doc)
    indexer.index_text(message)
    database.add_document(doc)
    database.flush()


def log(phenny, input, channel=None):
    # ignore the output from other bots
    if phenny:
        if input.nick == "otherbotname":
            return
        channel = input.sender.replace("#", "")
    # ignore anything which isn't entirely ASCII
    try:
        input = input.encode("ascii")
    except UnicodeEncodeError:
        return
    # ignore server commands
    if re.compile(r".*(VERSION|ACTION)").match(input):
        return
    # ignore obscenities
    for obscenity in OBSCENITY_LIST:
        if obscenity in input:
            return
    # ignore text intended for other bots
    if re.compile(r"(?i)(\.|,|\w+:\w|\[off\])").match(input):
        return
    # save the context
    context_filename = path.join(CONTEXT_DIRECTORY, "%s.txt" % channel)
    context_file = file(context_filename, "a+")
    context_list = context_file.readlines()
    context_list.append(input)
    context_file = file(context_filename, "w")
    context_file.write("%s\n" % "".join(context_list[-2:]))
    context_file.close()
    # ignore text intended for other bots
    # if re.compile(r"(?i).*\botherbotname\b").match(input):
    #     return
    # ignore text with compound periods
    if re.compile(r".*\.[^,.!?\s$]").match(input):
        return
    # remove initial nick
    input = re.compile(r"\w+[:,] ").sub("", input)
    # ignore text with special characters
    if re.compile(r".*[@/\\<>:;|]").match(input):
        return
    # sanitise common honorifics
    input = re.compile(r"(?i)dr\.").sub("dr", input)
    input = re.compile(r"(?i)prof\.").sub("prof", input)
    input = re.compile(r"(?i)mr\.").sub("mr", input)
    input = re.compile(r"(?i)mrs\.").sub("mrs", input)
    # sanitise initials
    input = re.compile(r"(?i)(^|\s)([a-z])\.").sub("\g<1>\g<2>", input)
    # sanitise double characters
    input = re.compile(r"--").sub("-", input)
    input = re.compile(r"==").sub("=", input)
    # sanitise special characters
    input = re.compile(r"[*]").sub("", input)
    # strip quotation marks with non-words on either side
    input = re.compile(r"\W[\"']|[\"']\W").sub(" ", input)
    # convert parenthesis
    input = re.compile(r"[{}()\[\]]").sub(",", input)
    # normalise use of message seperators
    input = re.compile(r"([)]\s?)\W+[,]").sub("\g<1>,", input)
    input = re.compile(r"([)]\s?)\W+[.]").sub("\g<1>.", input)
    input = re.compile(r"([)]\s?)\W+[?]").sub("\g<1>?", input)
    input = re.compile(r"([)]\s?)\W+[!]").sub("\g<1>!", input)
    # split the text into seperate messages
    message_end = None
    message_list = []
    expression_split_list = re.compile(r"([,.!?])").split(input)
    for key, message in enumerate(expression_split_list):
        if message not in (",", ".", "!", "?"):
            # normalise spaces and lowercase
            message = " ".join(message.split()).lower()
            # sanitise leading non word characters
            message = re.compile(r"^\W+ ?").sub("", message)
            message_list.append(message)
            continue
        else:
            message_end = message
        message_list[-1] = "%s%s" % (message_list[-1], message_end)
    # randomly punctuate messages if not already punctuated
    new_message_list = []
    for key, message in enumerate(message_list):
        if not message or len(message.split()) < 2:
            continue
        if message[-1] in (",", ".", "!", "?"):
            new_message_list.append(message)
            continue
        new_message_list.append("%s," % message)
    # write out each message to the vocabulary file
    vocabulary_filename = path.join(VOCABULARY_DIRECTORY, "%s.txt" % channel)
    vocabulary_file = file(vocabulary_filename, "a")
    for message in new_message_list:
        message = message.strip()
        vocabulary_file.write("%s\n" % message)
        index(message)
    vocabulary_file.close()

log.rule =  r".*"
log.priority = "low"
log.thread = False

def reprocess():
    for filename in os.listdir(VOCABULARY_DIRECTORY):
        vocabulary_filename = path.join(VOCABULARY_DIRECTORY, filename)
        temporary_vocabulary_filename = path.extsep.join([filename, "tmp"])
        vocabulary_file = file(vocabulary_filename)
        vocabulary = vocabulary_file.read()
        vocabulary_file.close()
        shutil.move(vocabulary_filename , temporary_vocabulary_filename)
        channel = filename.split(".")[0]
        for message in vocabulary.splitlines():
            log(None, message.decode("utf-8"), channel)
        os.unlink(temporary_vocabulary_filename)

if __name__ == "__main__":
    reprocess()
