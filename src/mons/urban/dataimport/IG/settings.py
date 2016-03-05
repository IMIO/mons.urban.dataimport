# -*- coding: utf-8 -*-

from mons.urban.dataimport.IG.importer import IGDataImporter
from mons.urban.dataimport.IG.interfaces import IIGDataImporter
from imio.urban.dataimport.browser.adapter import ImporterFromSettingsForm

from zope.interface import implements


class MonsIGImporterFromSettingsForm(ImporterFromSettingsForm):

    implements(IIGDataImporter)

    def __init__(self, settings_form, importer_class=IGDataImporter):
        """
        """
        super(MonsIGImporterFromSettingsForm, self).__init__(settings_form, importer_class)
