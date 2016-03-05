# -*- coding: utf-8 -*-

from imio.urban.dataimport.AIHM.importer import AIHMDataImporter
from imio.urban.dataimport.AIHM.interfaces import IAIHMDataImporter
from imio.urban.dataimport.browser.adapter import ImporterFromSettingsForm

from zope.interface import implements


class MonsImporterFromSettingsForm(ImporterFromSettingsForm):

    implements(IAIHMDataImporter)

    def __init__(self, settings_form, importer_class=AIHMDataImporter):
        """
        """
        super(MonsImporterFromSettingsForm, self).__init__(settings_form, importer_class)
