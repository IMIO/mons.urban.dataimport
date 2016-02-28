# -*- coding: utf-8 -*-

from imio.urban.dataimport.browser.controlpanel import ImporterControlPanel
from imio.urban.dataimport.browser.import_panel import ImporterSettings
from imio.urban.dataimport.browser.import_panel import ImporterSettingsForm


class MonsImporterSettingsForm(ImporterSettingsForm):
    """ """


class MonsImporterSettings(ImporterSettings):
    """ """
    form = MonsImporterSettingsForm


class MonsImporterControlPanel(ImporterControlPanel):
    """ """
    import_form = MonsImporterSettings
