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
				<head>
					<meta charset="utf-8">
					<title>SMS Sender</title>
					<meta name="viewport" content="width=device-width, initial-scale=1.0">
					<meta name="description" content="SMS Sender">
					<meta name="author" content="François Fornaciari">
					<link href="./bootstrap/css/bootstrap.css" rel="stylesheet">
					<style>
						body {
							padding-top: 20px;
						}
					</style>
					<link href="./bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
				</head>
				<body>
					<div class="container">
						<form action="/send" method="post" accept-charset="UTF-8">
							<fieldset>
								<legend>SMS Sender</legend>
								<label>Username</label>
								<input type="tel" name="username" placeholder="0102030405" required maxlength="10"/>
								<label>Password</label>
								<input type="password" name="password" required/>
								<label>Phone Number</label>
								<input type="tel" name="phonenumber" placeholder="0102030405" required maxlength="10"/>
								<label>Message</label>
								<textarea id="messageTA" name="message" rows="5"></textarea>
								<label id="messageLengthLabel">0 SMS</label>
								<div class="form-actions">
									<button type="submit" class="btn btn-primary">Send SMS</button>
								</div>
							</fieldset>
						</form>
					</div>
					<script src="http://code.jquery.com/jquery-latest.js"></script>
					<script type="text/javascript">
						$(document).ready(function(){
							$("#messageTA").keyup(function() {
								var currentString = $("#messageTA").val();
								var numMessages = Math.floor(currentString.length / 140);
								if ((currentString.length % 140) > 0) {
									numMessages++;
								}
								$("#messageLengthLabel").html(numMessages + " SMS (" + currentString.length + " caractères)");
							});
						});
					</script>
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
