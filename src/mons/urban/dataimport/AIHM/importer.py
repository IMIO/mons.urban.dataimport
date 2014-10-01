# -*- coding: utf-8 -*-
from imio.urban.dataimport.AIHM.importer import importAIHM


def importMonsAIHM(context):
    """ Just calls the default AIHM import from Mons AIHM profile """
    if context.readDataFile('monsurbandataimport_marker.txt') is None:
        return

    importAIHM(context)
