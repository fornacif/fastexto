import urllib
import mechanize
import logging

# URLs
SFR_LOGIN_URL = 'https://www.sfr.fr/mon-espace-client'
SFR_COMPOSE_URL = 'http://www.sfr.fr/xmscomposer/index.html?todo=compose'
SFR_CONFIRM_URL = 'http://www.sfr.fr/xmscomposer/mc/envoyer-texto-mms/send.html'

class SMSSender(object):
    """Object to send sms through SFR web interface"""
    
    def __init__(self, username, password):
        """Build a new sms sender by login to the SFR web interface"""
        # connect to www.sfr.fr
        self.br = mechanize.Browser()
        # set a fake user agent
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; '
                               'fr-FR; rv:1.9.0.1) Gecko/2008071615 '
                               'Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        resp1 = self.br.open(SFR_LOGIN_URL)
        # fill the login form
        self.br.select_form(nr=0)
        self.br.form['username'] = username
        self.br.form['password'] = password
        r = self.br.submit()
        # check the sucess of the login
        assert "Bienvenue dans votre Espace Client" in r.get_data()
    
    def sendsms(self, dest, message):
        """Send a message to dest"""
        # open the compose page
        self.br.open(SFR_COMPOSE_URL)
        # fill the sms form
        self.br.select_form(nr=0)
        self.br.form["msisdns"] = dest
        self.br.form["textMessage"] = message.encode('utf-8')
        r = self.br.submit()
        
        if "Voulez-vous envoyer ce message ?" in r.get_data():
            # confirm if needed
            data = urllib.urlencode({})
            r = self.br.open(SFR_CONFIRM_URL, data)
        
        assert "Votre texto a" in r.get_data()

