# -*- coding: utf-8 -*-

from imio.urban.dataimport.interfaces import IUrbanDataImporter

from plone.theme.interfaces import IDefaultPloneLayer


class IMonsUrbanDataimportLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""


class IMonsDataImporter(IUrbanDataImporter):
    """ Marker interface for IMons licence importer """
