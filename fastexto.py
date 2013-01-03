import webapp2
import logging

from google.appengine.ext import db

class SMS(db.Model):
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
					<div><input type="text" name="phonenumber" cols="10"></input></div>
					<div><textarea name="message" rows="3" cols="60"></textarea></div>
					<div><input type="submit" value="Send Texto"></div>
				</form>
			</body>
		</html>""")
		
class Send(webapp2.RequestHandler):
	def post(self):
		sms = SMS()
		sms.phonenumber = self.request.get('phonenumber')
		sms.message = self.request.get('message')
		self.send(sms)
		sms.put()
		self.redirect('/')
	def send(self, sms):
		logging.info("Sending message to %s", str(sms.phonenumber))

app = webapp2.WSGIApplication([
	('/', Main),
	('/send', Send)
], debug=True)
