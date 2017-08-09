# -*- coding: utf-8 -*-
#
# This file is part of cepces.
#
# cepces is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cepces is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cepces.  If not, see <http://www.gnu.org/licenses/>.
#
"""This module contains all the supported certmonger operations."""

from abc import ABCMeta, abstractmethod
from cepces.core import Base
from cepces.certmonger.core import MissingEnvironmentVariable
from cepces.certmonger.core import Result as CertmongerResult
import os
import sys


class Operation(Base, metaclass=ABCMeta):
    """Abstract base class used by classes mapping certmonger operations.

    As certmonger calls a helper, all of the necessary data is available as
    environment variables. Some of these variables may be required to perform
    an action, whereas others are optional. This base class helps ensure
    everything required is present, or fails otherwise.

    Two class variables are used to define this behaviour:

    * _required_: A list containing all required environment variables.
    * _optional_: A list containing tuples of all optional environment
                  variables and their defaults (e.g., '("VAR", None)').
    """
    _required_ = []
    _optional_ = []
    _name_ = None

    def __init__(self, out=sys.stdout):
        """Initializes an Operation.

        All required and optional environment variables are verified, read and
        stored in the instance as a dictionary.

        :param out: default output stream (default: sys.stdout)
        """
        super().__init__()

        self._out = out
        self._vars = {}

        # Verify that all required environment variables are present.
        for var in self.__class__._required_:
            if var not in os.environ:
                raise MissingEnvironmentVariable(var)
            else:
                self._vars[var] = os.environ[var]

        # Get all optional variables and set their defaults if they're missing.
        for var, default in self.__class__._optional_:
            if var not in os.environ:
                self._vars[var] = default
            else:
                self._vars[var] = os.environ[var]

    @abstractmethod
    def __call__(self):
        """Calls the operation to let it performs its logic."""
        pass

    @property
    def name(self):
        """Returns the operation's name as designated by certmonger.

        :return: The certmonger operation's name.
        """
        if not self.__class__._name_:
            raise RuntimeError('No name has been set for {}'
                               .format(self.__class__))

    @property
    def result(self):
        """Returns the final result of the operation."""
        # If no result has been set, raise an exception. Either the result is
        # requested too early, or it is never set.
        if not hasattr(self, '_result'):
            raise RuntimeError('No result has been set')
        else:
            return self._result


class Submit(Operation):
    """Attempt to enroll a new certificate."""
    _name_ = 'SUBMIT'

    def __call__(self):
        raise NotImplementedError()


class Poll(Operation):
    """Poll the status for a previous deferred request."""
    _name_ = 'POLL'

    def __call__(self):
        raise NotImplementedError()


class Identify(Operation):
    """Outputs version information for this helper."""
    _name_ = 'IDENTIFY'

    def __call__(self):
        raise NotImplementedError()


class GetNewRequestRequirements(Operation):
    """Outputs a list of required environment variables for submission."""
    _name_ = 'GET-NEW-REQUEST-REQUIREMENTS'

    def __call__(self):
        raise NotImplementedError()


class GetRenewRequestRequirements(Operation):
    """Outputs a list of required environment variables for renewal."""
    _name_ = 'GET-RENEW-REQUEST-REQUIREMENTS'

    def __call__(self):
        raise NotImplementedError()


class GetSupportedTemplates(Operation):
    """Outputs a list of supported templates."""
    _name_ = 'GET-SUPPORTED-TEMPLATES'

    def __call__(self):
        raise NotImplementedError()


class GetDefaultTemplate(Operation):
    """Outputs the default template (which is nothing).

    MS-XCEP doesn't specify a default template/policy, so this operation always
    results in no output.
    """
    _name_ = 'GET-DEFAULT-TEMPLATE'

    def __call__(self):
        self._result = CertmongerResult.DEFAULT


class FetchRoots(Operation):
    """Outputs suggested nick-names and certificates for all CAs."""
    _name_ = 'FETCH-ROOTS'

    def __call__(self):
        raise NotImplementedError()
