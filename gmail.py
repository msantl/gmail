#!/usr/bin/env python
import imaplib, re
import sys
import pynotify
import os
import base64
CONFIGPATH="/home/matija/scripts/gmail/.config.ini"

def get_user_and_pass():
	username = ""
	password = ""
	dpassword = ""

	try:
		dat = open( CONFIGPATH, "r" )
		for line in dat:
			line = line.strip()
			match = re.search( r"<user>[\w.@]+</user>", line )
			if match: username = line.split(">")[1].split("<")[0]
			match = re.search( r"<pass>.+</pass>", line )
			if match: dpassword = line.split(">")[1].split("<")[0]
	
		password = base64.b64decode( dpassword )
		dat.close()

	except IOError as e:
		print "If you are running this script for the first time, you need to enter your email and password for your google account"
		print "Email address: ",
		username = raw_input().strip()
		print "Password: ",
		password = raw_input().strip();

		dpassword = base64.b64encode( password )

		dat = open( CONFIGPATH, "w" );

		dat.write( "<user>%s</user>\n<pass>%s</pass>\n" % ( username, dpassword ) )

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
    try:
      rc, self.response = self.M.login(username, password)
    except:
			print "Looks like you entered your credentials wrong"
			os.remove( CONFIGPATH )
			sys.exit(1)

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

  out = int( g.get_unread_count('Internship') ) + int( g.get_unread_count('INBOX') ) + int( g.get_unread_count('Facebook') ) + int( g.get_unread_count('FER') )+ int( g.get_unread_count('TopCoder') )
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

