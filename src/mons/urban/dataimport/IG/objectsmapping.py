# -*- coding: utf-8 -*-

from mons.urban.dataimport.IG.mappers import LicenceFactory, \
    IdMapper, PortalTypeMapper, WorklocationMapper, NotaryMapper, ArchitectMapper, \
    CompletionStateMapper, ContactFactory, ContactTitleMapper, ContactSreetMapper, \
    ContactNumberMapper, ContactIdMapper, ParcelFactory, \
    ParcelReferencesMapper, UrbanDecisionEventFactory, DepositEventTypeMapper, \
    DepositDateMapper, DecisionEventTypeMapper, DecisionDateMapper, \
    NotificationDateMapper, DecisionMapper, UrbanDepositEventFactory, ErrorsMapper

from imio.urban.dataimport.mapper import SimpleMapper

OBJECTS_NESTING = [
    (
        'LICENCE', [
            ('CONTACT', []),
            ('PARCEL', []),
            ('DEPOSIT EVENT', []),
            ('DECISION EVENT', []),
            ('COLLEGE DECISION EVENT', []),
        ],
    ),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [LicenceFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'OBJET',
                    'to': 'licenceSubject',
                },
                {
                    'from': 'N°',
                    'to': 'reference',
                },
            ),

            IdMapper: {
                'from': ('N°',),
                'to': ('id',)
            },

            PortalTypeMapper: {
                'from': ('Type de permis',),
                'to': ('portal_type', 'folderCategory',)
            },

            WorklocationMapper: {
                'from': ('SITUATION DU BIEN -PARCELLE - RUE', 'NUM', 'CODE', 'LOCALITE'),
                'to': ('workLocations',)
            },

            ArchitectMapper: {
                'allowed_containers': ['BuildLicence'],
                'from': ('TITRE', 'PRENOM', 'NOM DEMANDEUR'),
                'to': ('architects',)
            },

            NotaryMapper: {
                'allowed_containers': ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter'],
                'from': ('PRENOM', 'NOM DEMANDEUR'),
                'to': ('notaryContact',),
            },

            CompletionStateMapper: {
                'from': ('DECISION CBE'),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },

            ErrorsMapper: {
                'from': (),
                'to': ('description',),  # log all the errors in the description field
            }
        },
    },

    'CONTACT':
    {
        'factory': [ContactFactory],

        'mappers': {

            SimpleMapper: (
                {
                    'from': 'NOM DEMANDEUR',
                    'to': 'name1',
                },
                {
                    'from': 'PRENOM',
                    'to': 'name2',
                },
                {
                    'from': 'CODE D',
                    'to': 'zipcode',
                },
                {
                    'from': 'LOCALITE D',
                    'to': 'city',
                },
                {
                    'from': 'N° DE TELEPHONE',
                    'to': 'phone',
                },
            ),

            ContactTitleMapper: {
                'from': ('TITRE'),
                'to': 'personTitle',
            },

            ContactSreetMapper: {
                'from': ('ADRESSE DU DEMANDEUR - RUE'),
                'to': 'street',
            },

            ContactNumberMapper: {
                'from': ('ADRESSE DU DEMANDEUR - RUE'),
                'to': 'number',
            },

            ContactIdMapper: {
                'from': ('NOM DEMANDEUR'),
                'to': 'id',
            },
        },
    },

    'PARCEL':
    {
        'factory': [ParcelFactory, {'portal_type': 'PortionOut'}],

        'mappers': {
            ParcelReferencesMapper: {
                'from': ('DIV.      CAD.', 'REFERENCES', 'LOCALITE'),
                'to': (),  # we dont know yet how many parcels will be extracted
                # maybe we will parse several parcels data from REFERENCES
            },
        },
    },

    'DEPOSIT EVENT':
    {
        'factory': [UrbanDepositEventFactory],

        'mappers': {
            DepositEventTypeMapper: {
                'from': (),
                'to': 'eventtype',
            },

            DepositDateMapper: {
                'from': 'DATE ENTREE',
                'to': 'eventDate',
            }
        },
    },

    'DECISION EVENT':
    {
        'factory': [UrbanDecisionEventFactory],

        'allowed_containers': ['UrbanCertificateOne', 'NotaryLetter', 'Declaration', 'Division'],

        'mappers': {
            DecisionEventTypeMapper: {
                'from': (),
                'to': 'eventtype',
            },

            DecisionDateMapper: {
                'from': 'DATE CBE',
                'to': 'eventDate',
            },

            DecisionMapper: {
                'from': 'DECISION CBE',
                'to': 'decision',
            },
        },
    },

    'COLLEGE DECISION EVENT':
    {
        'factory': [UrbanDecisionEventFactory],

        'allowed_containers': ['BuildLicence', 'ParcelOutLicence', 'UrbanCertificateTwo'],

        'mappers': {
            DecisionEventTypeMapper: {
                'from': (),
                'to': 'eventtype',
            },

            DecisionDateMapper: {
                'from': 'DATE CBE',
                'to': 'decisionDate',
            },

            NotificationDateMapper: {
                'from': 'DATE DE NOTIFICATION',
                'to': 'eventDate',
            },

            DecisionMapper: {
                'from': 'DECISION CBE',
                'to': 'decision',
            },
        },
    },
}
