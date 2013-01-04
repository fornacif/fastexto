import webapp2
import logging
import md5

from google.appengine.ext import db
from sfrswallow import SMSSender

class SMS(db.Model):
	username = db.StringProperty(multiline=False)
	password = ''
	phonenumber = db.StringProperty(multiline=False)
	message = db.StringProperty(multiline=True)
	
class Main(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write("""
			<html>
				<body>""")
		
		self.response.out.write("""
				<form action="/send" method="post">
					<div>Username : <input type="text" name="username" cols="10"></input></div>
					<div>Password : <input type="password" name="password" cols="10"></input></div>
					<div>Phone Number : <input type="text" name="phonenumber" cols="10"></input></div>
					<div>Message : <textarea name="message" rows="3" cols="60"></textarea></div>
					<div><input type="submit" value="Send Texto"></div>
				</form>
			</body>
		</html>""")
		
class Send(webapp2.RequestHandler):
	def post(self):
		sms = SMS()
		sms.username = self.request.get('username')
		sms.password = self.request.get('password')
		sms.phonenumber = self.request.get('phonenumber')
		sms.message = self.request.get('message')
		self.send(sms)
		sms.put()
		self.redirect('/')
	def send(self, sms):
		logging.info("Sending message to %s", str(sms.phonenumber))
		sender = SMSSender(sms.username, sms.password)
		sender.sendsms(sms.phonenumber, sms.message)

app = webapp2.WSGIApplication([
	('/', Main),
	('/send', Send)
], debug=True)
