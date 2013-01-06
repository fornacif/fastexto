import webapp2
import logging
import md5
import jinja2
import os

from google.appengine.ext import db
from google.appengine.api import users
from sfrswallow import SMSSender

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Account(db.Model):
	username = db.StringProperty(multiline=False)
	password = db.StringProperty(multiline=False)
	
class SMS(db.Model):
	phonenumber = db.StringProperty(multiline=False)
	message = db.StringProperty(multiline=True)
	
class Authentication:
	@staticmethod
	def authenticate(self):
		user = users.get_current_user()
		if user is None:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			return user
	
class Main(webapp2.RequestHandler):
	def get(self):
		user = Authentication.authenticate(self)
		if user:
			template_values = {
				"nickname": user.nickname(),
				"logoutURL": users.create_logout_url("/")
			}
			template = jinja_environment.get_template("index.html")
			self.response.out.write(template.render(template_values))
		
class Send(webapp2.RequestHandler):
	def post(self):
		user = Authentication.authenticate(self)
		if user:
			accountKey = db.Key.from_path('Account', user.user_id())
			account = db.get(accountKey)
		
			sms = SMS()
			sms.phonenumber = self.request.get("phonenumber")
			sms.message = self.request.get("message")
		
			try:
				if account and account.username and account.password:
					sender = SMSSender(account.username, account.password)
					logging.info("Sending message to %s", str(sms.phonenumber))
					sender.send(sms.phonenumber, sms.message)	
					sms.put()
			except AssertionError:
				logging.info("Bad credentials for %s", user.nickname())

		self.redirect("/")
			
class AccountManager(webapp2.RequestHandler):
	def get(self):
		user = Authentication.authenticate(self)
		if user:
			accountKey = db.Key.from_path('Account', user.user_id())
			account = db.get(accountKey)
			template_values = {
				"account": account,
				"nickname": user.nickname(),
				"logoutURL": users.create_logout_url("/")
			}
			template = jinja_environment.get_template("account.html")
			self.response.out.write(template.render(template_values))
	def post(self):
		user = Authentication.authenticate(self)
		if user:
			account = Account(key_name = user.user_id())
			account.username = self.request.get("username")
			account.password = self.request.get("password")
			account.put()
			
			self.redirect("/")

app = webapp2.WSGIApplication([
	("/", Main),
	("/send", Send),
	("/account", AccountManager)
], debug=True)
