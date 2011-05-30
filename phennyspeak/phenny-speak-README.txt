"Foolproof" instructions to install and run Phenny and an phenny-speak on Debian, Ubuntu and derivatives by Tim Dobson <tdobson.net/contact>


I've recently rediscovered Phenny, a modular python irc bot, written by Sean B. Palmer, as well as Noah Slater's previously unreleased "phenny-speak" module which uses markov chains to provide a source of amusement.

    * Phenny is free software, licenced under the Eiffel Forum License 2
    * "phenny speak" is free software, licenced under a very permissive BSD-like licence.

Setup Phenny Speak

Everybody run:

cd ~
wget http://www.blog.tdobson.net/files/phennyspeak.zip
unzip -o phennyspeak.zip
rm phennyspeak.zip

You have just installed the phenny speak module and the bits it messes with. It has put a whole lot of stuff in ~/.phenny

Install Phenny and phenny-speaks' dependencies

On Ubuntu Hardy

wget http://ftp.uk.debian.org/debian/pool/main/p/phenny/phenny_2~hg16-1_all.deb
sudo dpkg -i phenny*.deb
sudo apt-get install -f
rm phenny*.deb
sudo apt-get install python-xapian -y


On Ubuntu Intrepid

sudo apt-get install python-xapian phenny -y


On Debian Lenny:

su root
apt-get install python-xapian phenny -y


On other distros:

    * Install manually phenny from the source package at http://inamidst.com/phenny/
    * phenny-speak relies on the xapian-python package and any dependencies that might have.

In theory, it can run on anything that xapian-python and python 2.4 and it's dependencies are capable of running on.

Setup Phenny and phenny-speak

sensible-editor ~/.phenny/default.py

Change your IRC network, nick, password, channels to join etc. and save it.

sensible-editor ~/.phenny/module/speak.py

Do a Edit | "Find and Replace" in the file and replace "foonickbar" with the nick of your bot. eg. "crazybot"
There are 5 instances that should be replaced.

There are lots of other options like that to ignore the output from some bots but you can go hunting in the code to find those...

Start the bot

Start the bot with

phenny

or perhaps if you are going to run it for an extended period of time run:

nohup phenny 2> ~/.phenny/log.txt &

More info

A list of commands that the bot will respond to can be found on phenny's homepage
Troubleshooting

    * Check you have followed the instructions to the letter
    * Follow the instructions again from the start
    * If you think it is a problem with phenny then you want to be here.
    * If you think it might be a problem with phenny-speak then you might want to talk to Noah Slater
    * If you can see a problem in my instructions, please contact me, Tim Dobson - tdobson.net/contact
