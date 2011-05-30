nick = "bot_nick"
host = "irc.freenode.net"
password = "my_pass"
channels = ["#mychan", "#foo", "#tdobson.net", "#bar" ]
owner = "mynick"

# people allowed to use admin.py functions
admins = [owner, "other-nick"]

# for available modules see /usr/share/python-support/phenny/phenny/modules

# exclude modules
exclude = ["admin"]

## DONT TOUCH unless you know what you are doing or have a backup...

# enable specific modules, trumps exclude
#enable = [ "log", "speak"]

# extra modules to load by filename
extra = ["~/.phenny/contrib", "~/.phenny/module"]

# limit modules in specific channels
# limit = {"#channel": ["module-a", "module-b"]}

