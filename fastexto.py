import webapp2
import logging
import md5
import jinja2
import os

from google.appengine.ext import db
from google.appengine.api import users
from sfrswallow import SMSSender

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class SMS(db.Model):
	username = db.StringProperty(multiline=False)
	password = ""
	phonenumber = db.StringProperty(multiline=False)
	message = db.StringProperty(multiline=True)
	
class Main(webapp2.RequestHandler):
	def get(self):
		user = authenticate(self)
		if (user):
			template_values = {
				"nickname": user.nickname(),
				"logoutURL": users.create_logout_url("/")
			}
			template = jinja_environment.get_template("index.html")
			self.response.out.write(template.render(template_values))
		
class Send(webapp2.RequestHandler):
	def post(self):
		user = authenticate(self)
		if (user):
			sms = SMS()
			sms.username = self.request.get("username")
			sms.password = self.request.get("password")
			sms.phonenumber = self.request.get("phonenumber")
			sms.message = self.request.get("message")
			
			logging.info("Sending message to %s", str(sms.phonenumber))
			sender = SMSSender(sms.username, sms.password)
			sender.sendsms(sms.phonenumber, sms.message)
			
			sms.put()
			self.redirect("/")
		
def authenticate(self):
	user = users.get_current_user()
	if user is None:
		self.redirect(users.create_login_url(self.request.uri))
	else:
		return user

app = webapp2.WSGIApplication([
	("/", Main),
	("/send", Send)
], debug=True)
