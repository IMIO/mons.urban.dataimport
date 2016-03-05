# -*- coding: utf-8 -*-

from zope.interface import implements

from imio.urban.dataimport.csv.importer import CSVDataImporter
from imio.urban.dataimport.mapping import ObjectsMapping, ValuesMapping
from mons.urban.dataimport.IG.interfaces import IIGDataImporter

from mons.urban.dataimport.IG import objectsmapping, valuesmapping


class IGDataImporter(CSVDataImporter):
    """ """

    implements(IIGDataImporter)

    def __init__(self, csv_filename='IG-urbanisme.csv', key_column='N°', savepoint_length=0):
        super(IGDataImporter, self).__init__(csv_filename, key_column)


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
