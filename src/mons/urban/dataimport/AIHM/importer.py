# -*- coding: utf-8 -*-

from zope.interface import implements

from mons.urban.dataimport.interfaces import IMonsDataImporter

from imio.urban.dataimport.AIHM.importer import AIHMDataImporter


class LicencesImporter(AIHMDataImporter):
    """ """

    implements(IMonsDataImporter)

    def __init__(self, context, db_name, table_name='Urbanisme', key_column='CLEF', savepoint_length=0):
        super(LicencesImporter, self).__init__(db_name, table_name, key_column, savepoint_length)
