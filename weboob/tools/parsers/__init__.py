# -*- coding: utf-8 -*-

# Copyright(C) 2010-2011 Christophe Benz, Romain Bignon
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


import logging


__all__ = ['get_parser', 'NoParserFound']


class NoParserFound(Exception):
    pass


def load_lxml():
    from .lxmlparser import LxmlHtmlParser
    return LxmlHtmlParser


def load_lxmlsoup():
    from .lxmlsoupparser import LxmlSoupParser
    return LxmlSoupParser


def load_html5lib():
    from .html5libparser import Html5libParser
    return Html5libParser


def load_elementtidy():
    from .elementtidyparser import ElementTidyParser
    return ElementTidyParser


def load_builtin():
    from .htmlparser import HTMLParser
    return HTMLParser


def load_json():
    # This parser doesn't read HTML, don't include it in the
    # preference_order default value below.
    from .jsonparser import JsonParser
    return JsonParser


def get_parser(preference_order=('lxml', 'lxmlsoup')):
    return load_lxml()
