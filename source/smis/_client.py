# (C) Copyright 2015 Autodesk, Inc.  All rights reserved.
#
# Permission to use, copy, modify, and distribute these source code samples is
# hereby granted, provided that (i) you must clearly identify any modified
# source code files and any resulting binary files as works developed by you,
# and not by Autodesk;  and (ii) you may distribute the resulting binary files
# of the source code samples in works that are commercially distributed
# software applications only if:  (a) such applications require an Autodesk
# product to operate; and (b) such applications contain, subject to Autodesk's
# sole discretion, significant features and functionality in addition to the
# source code samples so that the source code samples are not the primary
# source of value.  In any copy of the source code samples, derivative works,
# and resulting binary files, you must include the copyright notices of
# Autodesk, Inc., the limited warranty and restricted rights notice below, and
# (if modified) the following statement: "This software contains copyrighted
# code owned by Autodesk but has been modified and is not endorsed by Autodesk
# in its modified form".
#
# AUTODESK PROVIDES THIS SOFTWARE "AS IS" AND WITH ALL FAULTS.  AUTODESK MAKES
# NO WARRANTIES, EXPRESS OR IMPLIED, AS TO NON-INFRINGEMENT OF THIRD PARTY
# RIGHTS, MERCHANTABILITY, OR FITNESS FOR ANY PARTICULAR PURPOSE. IN NO EVENT
# WILL AUTODESK BE LIABLE TO YOU FOR ANY CONSEQUENTIAL, INCIDENTAL OR SPECIAL
# DAMAGES, INCLUDING ANY LOST PROFITS OR LOST SAVINGS, EVEN IF AUTODESK HAS
# BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES, OR FOR ANY CLAIM BY ANY
# THIRD PARTY. AUTODESK DOES NOT WARRANT THAT THE OPERATION OF THE SOFTWARE
# WILL BE UNINTERRUPTED OR ERROR FREE.
#
# Use, duplication, or disclosure by the U.S. Government is subject to
# restrictions set forth in FAR 52.227-19 (Commercial ComputerSoftware -
# Restricted Rights) and DFAR 252.227-7013(c)(1)(ii) (Rights in Technical Data
# and Computer Software), as applicable.
#
# You may not export the source code samples or any derivative works,
# resulting binaries, or any related technical documentation,  in violation of
# U.S. or other applicable export control laws.
#
from smis import _utils as utils

class Client(object):
    """
    Model Information Service client application.

    This class is provided as entry point for all interfaces that communicate with the |mis|. The class is instantiated
    with a ``service`` proxy that knows how to communicate with the on-line service REST API.

    Client applications should not instantiate this class directly, and they should use the ``connect()`` method
    instead to access the ``Client`` object.
    """

    def __init__(self, service):
        self._service = service
        self._root_resource = _Resource('', self._service)

    @property
    def url(self):
        """
        Provides the end-point URL of the |mis|.

        :return:
            A string containing the URL to the |mis|.

        ..  todo::
            Provide sample code.
        """
        return self._service.endpoint

    @property
    def response(self):
        """
        Returns the response object from the service. This property returns None if ``get()`` has not been invoked yet.
        The property becomes handy in case of exceptions where it can provide more information about what went wrong.

        :return:
            The response object from accessing the client end-point.
        """
        return self._root_resource.response

    def get(self):
        """
        Returns the service payload.

        :return:
            Returns the service end-point payload as a python object (a dict).

        ..  todo::
            Finalize behavior and complete documentation with sample code.
        """
        return self._root_resource.get()

    def __getattr__(self, item):
        return _Resource(item, self._service, self._root_resource)


class _Resource(object):
    """
    This internal class is accessed through the :py:class:`Client` interface an allows accessing resources
    in the service.
    """

    def __init__(self, url_token, service, parent=None):
        self._url_token = url_token
        self._service = service
        self._parent = parent
        self._response = None

    @property
    def url(self):
        """
        Provides the full URL to the resource.

        :return:
            A string containing the full URL to the resource.

        ..  todo::
            Provide sample code.
        """
        return utils.url_join(self._service.endpoint, self.path)

    @property
    def path(self):
        """
        Provides the relative path to the resource from the base end-point.

        :return:
            Returns a string containing the relative path to the resource.

        ..  todo::
            Provide sample code.
        """
        return utils.url_join(self._parent.path, self._url_token) if self._parent else self._url_token

    @property
    def response(self):
        """
        Returns the response object for the resource. This property returns None if ``get()`` has not been invoked yet.
        The property becomes handy in case of exceptions where it can provide more information about what went wrong.

        :return:
            The response object from accessing the resource.
        """
        return self._response

    def get(self):
        """
        Provides the resource representation as a python object (dict for single resources, list for collections).

        :return:
            Returns the resource representation.

        ..  todo::
            Finalize behavior and complete documentation with sample code.
        """
        self._response = self._service.get(self.path)
        self._response.raise_for_status()
        return self._response.json()

    def item(self, identity):
        """
        Temporary ``item()`` method documentation.
        :param identity:
        :return:

        ..  todo::
            Finalize behavior and complete documentation with sample code.
        """
        return _Resource(identity, self._service, self)

    def __getattr__(self, item):
        return self.item(item)