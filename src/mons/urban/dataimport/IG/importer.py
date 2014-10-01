# -*- coding: utf-8 -*-

from zope.interface import implements

from imio.urban.dataimport.csv.importer import CSVDataImporter
from imio.urban.dataimport.mapping import ObjectsMapping, ValuesMapping
from mons.urban.dataimport.IG.interfaces import IIGDataImporter

from mons.urban.dataimport.IG import objectsmapping, valuesmapping


class IGDataImporter(CSVDataImporter):
    """ """

    implements(IIGDataImporter)


class IGMapping(ObjectsMapping):
    """ """

    def getObjectsNesting(self):
        return objectsmapping.OBJECTS_NESTING

    def getFieldsMapping(self):
        return objectsmapping.FIELDS_MAPPINGS


class IGValuesMapping(ValuesMapping):
    """ """

    def getValueMapping(self, mapping_name):
        return valuesmapping.VALUES_MAPS.get(mapping_name, None)


def importIG(context):
    """
    """
    if context.readDataFile('monsurbandataimport_marker.txt') is None:
        return

    ig_filename = 'IG/IG-urbanisme.csv'
    key_column = 'N°'

    IG_dataimporter = IGDataImporter(context, ig_filename, key_column)

    IG_dataimporter.importData(start=1, end=1000)

    IG_dataimporter.picklesErrorLog(filename='ig error log')
