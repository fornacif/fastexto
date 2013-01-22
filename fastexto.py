import webapp2
import logging
import datetime
import jinja2
import os
import json

from google.appengine.ext import db
from google.appengine.api import users

from sfr.browser import SfrBrowser
from weboob.capabilities.messages import Message,Thread

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class SMS(db.Model):
	phonenumber = db.StringProperty(multiline=False)
	message = db.StringProperty(multiline=True)
	username = db.StringProperty(multiline=False)
	date = db.DateTimeProperty()

class Contact(db.Model):
	name = db.StringProperty(multiline=False)
	phonenumber = db.StringProperty(multiline=False)
	def to_dict(self):
		properties = {"id": self.key().id()}
		for key in self.properties().keys():
			properties.update({key:unicode(getattr(self, key))})
		return properties

class Account(db.Model):
	username = db.StringProperty(multiline=False)
	password = db.StringProperty(multiline=False)
	def to_dict(self):
		return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class Authentication:
	@staticmethod
	def authenticate(self):
		user = users.get_current_user()
		if user is None:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			return user
	
class Index(webapp2.RequestHandler):
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
			
			params = json.loads(self.request.body)
		
			try:
				if account and account.username and account.password:	
					sms = SMS()
					sms.phonenumber = params['phonenumber']
					sms.message = params['message']
					sms.username = account.username
					sms.date = datetime.datetime.now()
				
					#browser = SfrBrowser(account.username, account.password)
					logging.info("Sending message to %s", sms.phonenumber)
					#browser.post_message(Message(Thread(sms.phonenumber), 0, content=sms.message))
					sms.put()
			except:
				logging.info("Error sending message for %s", user.nickname())
				raise
				
class Account(webapp2.RequestHandler):
	def get(self):
		user = Authentication.authenticate(self)
		if user:
			accountKey = db.Key.from_path('Account', user.user_id())
			account = db.get(accountKey)
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(account.to_dict()))
	def post(self):
		user = Authentication.authenticate(self)
		if user:
			accountKey = db.Key.from_path('Account', user.user_id())
			account = db.get(accountKey)
			
			params = json.loads(self.request.body)
			
			account.username = params['username'];
			account.password = params['password'];
			account.put();
			
class Contacts(webapp2.RequestHandler):
	def get(self):
		user = Authentication.authenticate(self)
		if user:
			contacts = Contact.all()

			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps([p.to_dict() for p in contacts]))
			
class AddContact(webapp2.RequestHandler):
	def post(self):
		user = Authentication.authenticate(self)
		if user:
			params = json.loads(self.request.body)
			
			contact = Contact()
			contact.name = params['name'];
			contact.phonenumber = params['phonenumber'];
			contact.put()
			
class DeleteContact(webapp2.RequestHandler):
	def get(self, id):
		user = Authentication.authenticate(self)
		if user:
			logging.info("Deleting contact %s", id)
			contact = Contact.get_by_id(int(id))
			contact.delete()
			
app = webapp2.WSGIApplication([
	('/', Index),
	('/send', Send),
	('/contact', AddContact),
	('/contact/(\d+)', DeleteContact),
	('/contacts', Contacts),
	('/account', Account),
], debug=True)
