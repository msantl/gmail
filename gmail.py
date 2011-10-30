#!/usr/bin/env python
import imaplib, re
import sys
import pynotify
import os

def get_user_and_pass():
	dat = open( "/home/matija/scripts/gmail/config.ini", "r" )
	username = ""
	password = ""

	for line in dat:
		line = line.strip()
		match = re.search( r"<user>[\w.@]+</user>", line )
		if match: username = line.split(">")[1].split("<")[0]
		match = re.search( r"<pass>[\w.@]+</pass>", line )
		if match: password = line.split(">")[1].split("<")[0]
	
	dat.close()
	
	return (username, password)

class gmail(object):
  def __init__(self):
    self.IMAP_SERVER='imap.gmail.com'
    self.IMAP_PORT=993
    self.M = None
    self.response = None
    self.mailboxes = []

  def login(self, username, password):
    self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
    rc, self.response = self.M.login(username, password)
    return rc

  def get_unread_count(self, folder='Inbox'):
    rc, self.response = self.M.status(folder, "(UNSEEN)")
    unreadCount = re.search("UNSEEN (\d+)", self.response[0]).group(1)
    return unreadCount
    
  def get_mailboxes(self):
    rc, self.response = self.M.list()
    for item in self.response:
      self.mailboxes.append(item.split()[-1])
    return rc

  def logout(self):
    self.M.logout()    

def main():
  cnt = 0
  g = gmail()
  username,password = get_user_and_pass()
  g.login( username, password )

  out = int( g.get_unread_count('INBOX') ) + int( g.get_unread_count('Facebook') ) + int( g.get_unread_count('FER') )+ int( g.get_unread_count('TopCoder') )
  if not pynotify.init("GMail"):
    sys.exit(1)

  if out:
    n = pynotify.Notification( "GMail", "You have " + str(out) + ' new mail.' ,"notification-message-im"  )
    n.set_property("icon-name", "/home/matija/scripts/gmail/gmail.png" ) 
    n.show()

  print out
    
  g.logout()

if __name__ == "__main__":
    main()

