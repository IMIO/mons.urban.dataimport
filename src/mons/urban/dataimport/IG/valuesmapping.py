# -*- coding: utf-8 -*-

from imio.urban.dataimport.mapping import table

VALUES_MAPS = {

'type_map': table({
'header'  : ['portal_type',         'foldercategory', 'abreviation'],
''        : ['BuildLicence',        'uap',            'PU'],
'P'       : ['BuildLicence',        'uap',            'PU'],
'1'       : ['BuildLicence',        'upp',            'PU'],
'2'       : ['BuildLicence',        '',               'PU'],
'ART. 48' : ['BuildLicence',        'udc',               'PU'],
'C.U. 1'  : ['UrbanCertificateOne', 'cu1',            'CU1'],
'C.U. 2'  : ['UrbanCertificateTwo', 'cu2',            'CU2'],
'22'      : ['NotaryLetter',        '',               'Not'],
'30'      : ['ParcelOutLicence',    '',               'PL'],
'40'      : ['MiscDemand',          'apct',           'DD'],
'50'      : ['BuildLicence',        'art127',         'PU'],
'80'      : ['BuildLicence',        'pu',             'PU'],
'82'      : ['Declaration',         'dup',            'Decl'],
'100'     : ['MiscDemand',          'apct',           'Decl'],
}),

'division_map': {
    '21': '53018',  # 'Ciply'
    '6': '53019',  # 'Cuesmes'
    '23': '53027',  # 'Fl\xc3\xa9nu'
    '7': '53030',  # 'Ghlin'
    '16': '53034',  # 'Harmignies'
    '17': '53035',  # 'Harveng'
    '13': '53038',  # 'Havr\xc3\xa9'
    '8': '53042',  # 'Hyon'
    '22': '53043',  # 'Jemappes'
    '12': '53048',  # 'Maisi\xc3\xa8res'
    '20': '53052',  # 'Mesvin'
    '1': '53053',  # 'Mons 1 div'
    '9': '53059',  # 'Nimy'
    '18': '53061',  # 'Nouvelles'
    '10': '53062',  # 'Obourg'
    '14': '53071',  # 'Saint-symphorien'
    '19': '53074',  # 'Spiennes'
    '2': '53402',  # 'Mons 2 div'
    '3': '53403',  # 'Mons 3 div'
    '4': '53404',  # 'Mons 4 div'
    '5': '53405',  # 'Mons 5 div'
    '11': '53502',  # 'Saint-Denis'
    '15': '55048',  # 'Villers-Saint-Ghislain'
},

'eventtype_id_map': table({
'header'             : ['decision_event',                       'folder_complete',     'deposit_event'],
'BuildLicence'       : ['delivrance-du-permis-octroi-ou-refus', 'accuse-de-reception', 'depot-de-la-demande'],
'UrbanCertificateOne': ['octroi-cu1',                           '',                    'depot-de-la-demande'],
'UrbanCertificateTwo': ['octroi-cu2',                           '',                    'depot-de-la-demande'],
'NotaryLetter'       : ['octroi-lettre-notaire',                '',                    'depot-de-la-demande'],
'ParcelOutLicence'   : ['delivrance-du-permis-octroi-ou-refus', 'accuse-de-reception', 'depot-de-la-demande'],
'Declaration'        : ['deliberation-college',                 '',                    'depot-de-la-demande'],
'MiscDemand'         : ['deliberation-college',                 '',                    'depot-de-la-demande'],
'Division'           : ['decision-octroi-refus',                '',                    'depot-de-la-demande'],
}),

'titre_map': {
    'monsieur': 'mister',
    'm': 'mister',
    'm.': 'mister',
    'messieurs': 'misters',
    'mrs.': 'misters',
    'mrs': 'misters',
    'madame': 'madam',
    'mme': 'madam',
    'mme.': 'madam',
    'mesdames': 'ladies',
    'mademoiselle': 'miss',
    'monsieur et madame': 'madam_and_mister',
    'm et mme': 'madam_and_mister',
    'mr et mme': 'madam_and_mister',
    'm. et mme': 'madam_and_mister',
    'm et mme.': 'madam_and_mister',
    'm. et mme.': 'madam_and_mister',
    'notaire': 'master',
    'monsieur le notaire': 'master',
    'notaires': 'masters',
    'ma\xc3\xaetre': 'master',
    'ma\xc3\xaetres': 'masters',
},

'country_map': {
    'belgique': 'belgium',
    'france': 'france',
    'allemagne': 'germany',
    'luxembourg': 'luxembourg',
    'pays bas': 'netherlands',
},
}
