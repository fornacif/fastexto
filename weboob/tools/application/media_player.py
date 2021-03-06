# -*- coding: utf-8 -*-

# Copyright(C) 2010-2011 Christophe Benz, Romain Bignon, John Obbele
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


import os
from subprocess import Popen, PIPE

from weboob.tools.log import getLogger


__all__ = ['InvalidMediaPlayer', 'MediaPlayer', 'MediaPlayerNotFound']


PLAYERS = (
    ('mplayer', '-'),
    ('vlc',     '-'),
    ('parole',  'fd://0'),
    ('totem',   'fd://0'),
    ('xine',    'stdin:/'),
)


class MediaPlayerNotFound(Exception):
    def __init__(self):
        Exception.__init__(self, u'No media player found on this system. Please install one of them: %s.' % \
            ', '.join(player[0] for player in PLAYERS))


class InvalidMediaPlayer(Exception):
    def __init__(self, player_name):
        Exception.__init__(self, u'Invalid media player: %s. Valid media players: %s.' % (
            player_name, ', '.join(player[0] for player in PLAYERS)))


class MediaPlayer(object):
    """
    Black magic invoking a media player to this world.

    Presently, due to strong disturbances in the holidays of the ether
    world, the media player used is chosen from a static list of
    programs. See PLAYERS for more information.
    """
    def __init__(self, logger=None):
        self.logger = getLogger('mediaplayer', logger)

    def guess_player_name(self):
        for player_name in [player[0] for player in PLAYERS]:
            if self._find_in_path(os.environ['PATH'], player_name):
                return player_name
        return None

    def play(self, media, player_name=None):
        """
        Play a media object, using programs from the PLAYERS list.

        This function dispatch calls to either _play_default or
        _play_rtmp for special rtmp streams using SWF verification.
        """
        player_names = [player[0] for player in PLAYERS]
        if player_name:
            if player_name not in player_names:
                raise InvalidMediaPlayer(player_name)
        else:
            self.logger.debug(u'No media player given. Using the first available from: %s.' % \
                ', '.join(player_names))
            player_name = self.guess_player_name()
            if player_name is None:
                raise MediaPlayerNotFound()
        if media.url.startswith('rtmp'):
            self._play_rtmp(media, player_name)
        else:
            self._play_default(media, player_name)

    def _play_default(self, media, player_name):
        """
        Play media.url with the media player.
        """
        print 'Invoking "%s %s".' % (player_name, media.url)
        os.spawnlp(os.P_WAIT, player_name, player_name, media.url)

    def _play_rtmp(self, media, player_name):
        """
        Download data with rtmpdump and pipe them to a media player.

        You need a working version of rtmpdump installed and the SWF
        object url in order to comply with SWF verification requests
        from the server. The last one is retrieved from the non-standard
        non-API compliant 'swf_player' attribute of the 'media' object.
        """
        if not self._find_in_path(os.environ['PATH'], 'rtmpdump'):
            self.logger.warning('"rtmpdump" binary not found')
            return self._play_default(media, player_name)
        media_url = media.url
        try:
            player_url = media.swf_player
            if  media.swf_player:
                rtmp = 'rtmpdump -r %s --swfVfy %s' % (media_url, player_url)
            else:
                rtmp = 'rtmpdump -r %s' % media_url
        except AttributeError:
            self.logger.warning('Your media object does not have a "swf_player" attribute. SWF verification will be '
                                'disabled and may prevent correct media playback.')
            return self._play_default(media, player_name)

        rtmp += ' --quiet'

        args = None
        for (binary, stdin_args) in PLAYERS:
            if binary == player_name:
                args = stdin_args
        assert args is not None

        print ':: Streaming from %s' % media_url
        print ':: to %s %s' % (player_name, args)
        print ':: %s' % rtmp
        p1 = Popen(rtmp.split(), stdout=PIPE)
        Popen([player_name, args], stdin=p1.stdout, stderr=PIPE)

    def _find_in_path(self,path, filename):
        for i in path.split(':'):
            if os.path.exists('/'.join([i, filename])):
                return True
        return False
