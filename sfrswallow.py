#! /usr/bin/env python
#   -*- encoding: utf-8 -*-
#
#   SFR Swallow - send SMS through the SFR web interface
#   Version 0.4
#
#   Copyright (c) 2010, Émile Decorsière, Florian Birée
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import urllib
import mechanize
import logging

# urls
SFR_LOGIN_URL = 'http://www.sfr.fr/mon-espace-client'
SFR_COMPOSE_URL = 'http://www.sfr.fr/xmscomposer/index.html?todo=compose'
SFR_CONFIRM_URL = 'http://www.sfr.fr/xmscomposer/mc/envoyer-texto-mms/confirm.html'

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
        self.br.form["textMessage"] = message
        r = self.br.submit()
        
        if "Confirmer l'envoi" in r.get_data():
            # confirm if needed
            data = urllib.urlencode({})
            r = self.br.open(SFR_CONFIRM_URL, data)
        
        assert "Votre texto a" in r.get_data()

