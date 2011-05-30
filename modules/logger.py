#!/usr/bin/env python

# Copyright 2011, Aaron Racicot

import sys
import os, time;

def setup(phenny):
    # loop through all the channels that this bot is
    # serving and create logs if they dont exist
    # for today
    phenny.logDir = phenny.config.logdir
    phenny.currentDay = time.strftime("%Y-%m-%d", time.localtime())
    phenny.logFile = {}
    for channel in phenny.config.channels:
        try:
            channel = channel.replace("#", "")
        except:
            return ""
        channelFile = channel + '-' + time.strftime("%Y-%m-%d", time.localtime()) + '.log'
        phenny.logFile[channel] = os.path.join(phenny.logDir, channelFile)
        if not os.path.exists(phenny.logFile[channel]):
            try: f = open(phenny.logFile[channel], 'w')
            except OSError: pass
            else:
                f.write('LogFile = ' + channelFile + "\n")
                f.close()

def log_message(phenny, teller, channel, msg):
    if time.strftime("%Y-%m-%d", time.localtime()) != phenny.currentDay:
        # We need to create new log files for new day
        for channel in phenny.config.channels:
            try:
                channel = channel.replace("#", "")
            except:
                return ""
            channelFile = channel + '-' + time.strftime("%Y-%m-%d", time.localtime()) + '.log'
            phenny.logFile[channel] = os.path.join(phenny.logDir, channelFile)
            if not os.path.exists(phenny.logFile[channel]):
                try: f = open(phenny.logFile[channel], 'w')
                except OSError: pass
                else:
                    f.write('LogFile = ' + channelFile + "\n")
                    f.close()
    timenow = time.strftime("%H:%M:%S", time.localtime())
    line = " ".join((str(timenow), ("<"+teller+"> "), msg.strip()))
    try: f = open(phenny.logFile[channel], "a")
    except OSError: pass
    else:
        f.write(line + "\n")
        f.close();

def logger(phenny, input):
    teller = input.nick
    try:
        channel = input.sender.replace("#", "")
    except:
        return ""
    msg = input.group(1).replace("ACTION", "*").encode('utf-8')
    log_message(phenny, teller, channel, msg)
logger.rule = r'(.*)'
logger.priority = 'high'

if __name__ == "__main__":
    logger(None, " ".join(sys.argv[1:]))
