# -*- coding: utf-8 -*-

# Copyright(C) 2010-2011 Christophe Benz
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.


import re

from weboob.capabilities.messages import CantSendMessage
from weboob.tools.browser import BasePage



__all__ = ['ClosePage', 'ComposePage', 'ConfirmPage', 'SentPage']


class ClosePage(BasePage):
    pass


class ComposePage(BasePage):
    phone_regex = re.compile('^(\+33|0033|0)(6|7)(\d{8})$')

    def get_nb_remaining_free_sms(self):
        remaining_regex = re.compile(u'Il vous reste (?P<nb>.+) Texto gratuits vers les numéros SFR à envoyer aujourd\'hui')
        text = self.parser.select(self.document.getroot(), '#smsReminder', 1).text.strip()
        return remaining_regex.match(text).groupdict().get('nb')

    def post_message(self, message):
        receiver = message.thread.id
        if self.phone_regex.match(receiver) is None:
            raise CantSendMessage(u'Invalid receiver: %s' % receiver)
        self.browser.select_form(nr=0)
        self.browser['msisdns'] = receiver
        self.browser['textMessage'] = message.content.encode('utf-8')
        self.browser.submit()


class ConfirmPage(BasePage):
    def confirm(self):
        self.browser.select_form(nr=0)
        self.browser.submit()


class SentPage(BasePage):
    pass
