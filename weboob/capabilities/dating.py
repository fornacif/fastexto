# -*- coding: utf-8 -*-

# Copyright(C) 2010-2011 Romain Bignon
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


from .base import IBaseCap, CapBaseObject, Field, StringField, DateField, UserError
from .contact import Contact


__all__ = ['OptimizationNotFound', 'Optimization', 'Event', 'ICapDating']


class OptimizationNotFound(UserError):
    """
    Raised when an optimization is not found.
    """


class Optimization(object):
    """
    Optimization.

    :var CONFIG: Configuration of optim can be made by
                 :class:`weboob.tools.value.Value` objects
                 in this dict.
    """
    CONFIG = {}

    def start(self):
        """
        Start optimization.
        """
        raise NotImplementedError()

    def stop(self):
        """
        Stop optimization.
        """
        raise NotImplementedError()

    def is_running(self):
        """
        Know if the optimization is currently running.

        :rtype: bool
        """
        raise NotImplementedError()

    def get_config(self):
        """
        Get config of this optimization.

        :rtype: dict
        """
        return None

    def set_config(self, params):
        """
        Set config of this optimization.

        :param params: parameters
        :type params: dict
        """
        raise NotImplementedError()


class Event(CapBaseObject):
    """
    A dating event (for example a visite, a query received, etc.)
    """
    date =      DateField('Date of event')
    contact =   Field('Contact related to this event', Contact)
    type =      StringField('Type of event')
    message =   StringField('Message of the event')

class ICapDating(IBaseCap):
    """
    Capability for dating websites.
    """
    def init_optimizations(self):
        """
        Initialization of optimizations.
        """
        raise NotImplementedError()

    def add_optimization(self, name, optim):
        """
        Add an optimization.

        :param name: name of optimization
        :type name: str
        :param optim: optimization
        :type optim: :class:`Optimization`
        """
        setattr(self, 'OPTIM_%s' % name, optim)

    def iter_optimizations(self):
        """
        Iter optimizations.

        :rtype: iter[:class:`Optimization`]
        """
        for attr_name in dir(self):
            if not attr_name.startswith('OPTIM_'):
                continue
            attr = getattr(self, attr_name)
            if attr is None:
                continue

            yield attr_name[6:], attr

    def get_optimization(self, optim):
        """
        Get an optimization from a name.

        :param optim: name of optimization
        :type optim: str
        :rtype: :class:`Optimization`
        """
        optim = optim.upper()
        if not hasattr(self, 'OPTIM_%s' % optim):
            raise OptimizationNotFound()

        return getattr(self, 'OPTIM_%s' % optim)

    def iter_events(self):
        """
        Iter events.

        :rtype: iter[:class:`Event`]
        """
        raise NotImplementedError()
