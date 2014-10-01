# -*- coding: utf-8 -*-

from imio.urban.dataimport.mapper import Mapper
from imio.urban.dataimport.mapper import FinalMapper
from imio.urban.dataimport.mapper import PostCreationMapper

from imio.urban.dataimport.factory import BaseFactory, MultiObjectsFactory
from imio.urban.dataimport.utils import cleanAndSplitWord
from DateTime import DateTime
from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName


#
# LICENCE
#

# factory


class LicenceFactory(BaseFactory):
    def getCreationPlace(self, **kwargs):
        path = '%s/urban/%ss' % (self.site.absolute_url_path(), kwargs['portal_type'].lower())
        return self.site.restrictedTraverse(path)

# mappers


class IdMapper(Mapper):
    def mapId(self, line):
        return normalizeString(self.getData('N°'))


class PortalTypeMapper(Mapper):
    def mapPortal_type(self, line):
        type_value = self.getData('Type de permis')
        portal_type = self.getValueMapping('type_map')[type_value]['portal_type']
        if not portal_type:
            self.logError(self, line, 'No portal type found for this type value', {'TYPE value': type_value})
        return portal_type

    def mapFoldercategory(self, line):
        type_value = self.getData('Type de permis')
        foldercategory = self.getValueMapping('type_map')[type_value]['foldercategory']
        return foldercategory


class WorklocationMapper(Mapper):
    def mapWorklocations(self, line):
        num = self.getData('NUM')
        noisy_words = set(('d', 'du', 'de', 'des', 'le', 'la', 'les', 'à', ',', 'rues'))
        raw_street = self.getData('SITUATION DU BIEN -PARCELLE - RUE').split(',')[0]
        street = cleanAndSplitWord(raw_street)
        street_keywords = [word for word in street if word not in noisy_words and len(word) > 1]
        street_keywords.extend(cleanAndSplitWord(self.getData('CODE')))
        street_keywords.extend(cleanAndSplitWord(self.getData('LOCALITE')))
        brains = self.catalog(portal_type='Street', Title=street_keywords)
        if len(brains) == 1:
            return ({'street': brains[0].UID, 'number': num},)

        street_keywords = street_keywords[1:]
        brains = self.catalog(portal_type='Street', Title=street_keywords)
        if len(brains) == 1:
            return ({'street': brains[0].UID, 'number': num},)
        if street:
            self.logError(
                self,
                line,
                'Couldnt find street or found too much streets',
                {'address': raw_street, 'street': street_keywords, 'search result': len(brains)}
            )
        return {}


class ArchitectMapper(PostCreationMapper):
    def mapArchitects(self, line, plone_object):
        title = self.getData('TITRE')
        # we consider the applicant as an architect only if his/her title says so
        if 'arch' not in title.lower():
            return
        archi_name = self.getData('NOM DEMANDEUR') + self.getData('PRENOM')
        fullname = cleanAndSplitWord(archi_name)
        if not fullname:
            return []
        name_keywords = [word.lower() for word in fullname]
        architects = self.catalog(portal_type='Architect', Title=name_keywords)
        if len(architects) == 1:
            return architects[0].getObject()
        self.logError(self, line, 'No architects found or too much architects found', {'name': name_keywords, 'search_result': len(architects)})
        return []


class GeometricianMapper(PostCreationMapper):
    def mapGeometricians(self, line, plone_object):
        title_words = [word for word in self.getData('Titre').lower().split()]
        for word in title_words:
            if word not in ['géometre', 'géomètre']:
                return
        name = self.getData('Nom')
        name = cleanAndSplitWord(name)
        firstname = self.getData('Prenom')
        firstname = cleanAndSplitWord(firstname)
        names = name + firstname
        geometrician = self.catalog(portal_type='Geometrician', Title=names)
        if not geometrician:
            geometrician = self.catalog(portal_type='Geometrician', Title=name)
        if len(geometrician) == 1:
            return geometrician[0].getObject()
        self.logError(self, line, 'no geometricians found or too much geometricians found',
                      {'title': self.getData('Titre'), 'name': name, 'firstname': firstname, 'search_result': len(geometrician)})
        return []


class NotaryMapper(PostCreationMapper):
    def mapNotarycontact(self, line, plone_object):
        name = self.getData('NOM DEMANDEUR')
        firstname = self.getData('PRENOM')
        notary = self.catalog(portal_type='Notary', Title=[name, firstname])
        if not notary:
            notary = self.catalog(portal_type='Notary', Title=name)
        if len(notary) == 1:
            return notary[0].getObject()
        self.logError(self, line, 'no notaries found or too much notaries found',
                      {'name': name, 'firstname': firstname, 'search_result': len(notary)})
        return []


class CompletionStateMapper(PostCreationMapper):
    def map(self, line, plone_object):
        self.line = line
        decision = self.getData('DECISION CBE').lower()
        if 'autorisé' in decision:
            state = 'accepted'
        elif 'refusé' in decision:
            state = 'refused'
        else:
            state = 'accepted'
        workflow_tool = getToolByName(plone_object, 'portal_workflow')
        workflow_def = workflow_tool.getWorkflowsFor(plone_object)[0]
        workflow_id = workflow_def.getId()
        workflow_state = workflow_tool.getStatusOf(workflow_id, plone_object)
        workflow_state['review_state'] = state
        workflow_tool.setStatusOf(workflow_id, plone_object, workflow_state.copy())


class ErrorsMapper(FinalMapper):
    def mapDescription(self, line, plone_object):

        line_number = self.importer.current_line
        errors = self.importer.errors.get(line_number, None)
        description = plone_object.Description()

        error_trace = []

        if errors:
            parcel_error = False
            for error in errors:
                data = error.data
                if 'streets' in error.message:
                    error_trace.append('<p>adresse : {address}</p>'.format(address=data['address']))
                elif 'Cannot parse cadastral' in error.message and not parcel_error:
                    parcel_error = True
                    error_trace.append(
                        '<p>référence cadastrale : {division} {ref}</p>'.format(
                            division=data['division'],
                            ref=data['ref'],
                        )
                    )
        error_trace = ''.join(error_trace)

        return '%s%s' % (error_trace, description)

#
# CONTACT
#

# factory


class ContactFactory(BaseFactory):
    def create(self, place, **kwargs):
        return super(ContactFactory, self).create(place, **kwargs)

    def getPortalType(self, place, **kwargs):
        if place.portal_type in ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter']:
            return 'Proprietary'
        return 'Applicant'

# mappers


class ContactIdMapper(Mapper):
    def mapId(self, line):
        name = self.getData('NOM DEMANDEUR')
        return normalizeString(self.site.portal_urban.generateUniqueId(name))


class ContactTitleMapper(Mapper):
    def mapPersontitle(self, line):
        titre = self.getData('TITRE').lower()
        titre_mapping = self.getValueMapping('titre_map')
        title = titre_mapping.get(titre, 'notitle')
        return title


class ContactSreetMapper(Mapper):
    def mapStreet(self, line):
        street = self.getData('ADRESSE DU DEMANDEUR - RUE')
        street = street.split(',')[0]
        return street


class ContactNumberMapper(Mapper):
    def mapNumber(self, line):
        street = self.getData('ADRESSE DU DEMANDEUR - RUE')
        street = street.split(',')
        if len(street) == 2:
            return street[1]
        return ''


#
# PARCEL
#

#factory


class ParcelFactory(MultiObjectsFactory):
    def create(self, place=None, line=None, **factory_args):
        found_parcels = {}
        searchview = self.site.restrictedTraverse('searchparcels')
        for index, full_args in factory_args.iteritems():
            argnames = ['division', 'section', 'radical', 'puissance', 'exposant']
            args = {}
            for name in argnames:
                args[name] = full_args.get(name, '')
            #need to trick the search browser view about the args in its request
            for k, v in args.iteritems():
                searchview.context.REQUEST[k] = v
            #check if we can find a parcel in the db cadastre with these infos
            found = searchview.findParcel(**args)
            if not found:
                found = searchview.findParcel(browseoldparcels=True, **args)
            if len(found) == 1:
                args['divisionCode'] = args['division']
                args['division'] = args['division']
                found_parcels[index] = args
            else:
                found_parcels[index] = full_args
                self.logError(self, 'Too much parcels found or not enough parcels found', {'args': args, 'search result': len(found)})
        return super(ParcelFactory, self).create(place=place, **found_parcels)

# mappers


class ParcelReferencesMapper(Mapper):
    def map(self, line, **kwargs):

        self.line = line
        raw_references = self.getData('REFERENCES').upper()

        reference_groups = self.splitReferenceGroups(raw_references)
        tokenized_references = [self.tokenizeReference(ref) for ref in reference_groups]

        base_ref = tokenized_references[0]
        base_ref.reverse()

        division = self.getDivision()
        if not division:
            return []
        self.division_name = self.getData('LOCALITE') + ' ' + self.getData('DIV.      CAD.')

        bis = self.getBis(base_ref)
        if len(base_ref) > 4:
            self.logError(
                self,
                line,
                'Cannot parse cadastral reference',
                {'division': self.division_name, 'ref': self.getData('REFERENCES')}
            )
            return []

        reference = {
            'bis': bis,
            'section': self.getSection(base_ref),
            'radical': self.getRadical(base_ref),
            'exposant': self.getExposant(base_ref),
            'puissance': self.getPuissance(base_ref),
        }
        reference.update(division)

        references = [reference]

        for tokenized_ref in tokenized_references[1:]:
            ref = self.getSecondaryReference(tokenized_ref, reference)
            if ref:
                references.append(ref)

        references = dict([(str(i), ref) for i, ref in enumerate(references)])
        return references

    def getSecondaryReference(self, secondary_ref, base_ref):
        bis = self.getBis(secondary_ref)

        ref_parts = ['section', 'radical', 'exposant', 'puissance']

        to_fill = []
        for part in ref_parts:
            if base_ref[part]:
                to_fill.append(part)
            else:
                break

        if len(secondary_ref) > 4 or len(secondary_ref) > len(to_fill):
            self.logError(
                self,
                self.line,
                'Cannot parse cadastral secondary reference',
                {'division': self.division_name, 'ref': self.getData('REFERENCES')}
            )
            return

        reference = base_ref.copy()
        reference['bis'] = bis

        secondary_ref.reverse()
        for part in secondary_ref:
            part_name = to_fill.pop()
            old_part = reference[part_name]
            if self.isSameType(old_part, part):
                reference[part_name] = part
            else:
                self.logError(
                    self,
                    self.line,
                    'Cannot parse cadastral secondary reference',
                    {'division': self.division_name, 'ref': self.getData('REFERENCES')}
                )
                return

        return reference

    def isSameType(self, str1, str2):
        return (str1.isdigit() and str2.isdigit()) or (str1.isalpha() and str2.isalpha())

    def getPuissance(self, reference):
        if reference:
            return reference.pop()
        return ''

    def getExposant(self, reference):
        if reference:
            return reference.pop()
        return ''

    def getRadical(self, reference):
        if reference:
            return reference.pop()
        return ''

    def getSection(self, reference):
        if reference:
            return reference.pop()
        return ''

    def getBis(self, reference):
        if '/' in reference:
            bis_index = reference.index('/')
            bis = reference[bis_index - 1]
            del reference[bis_index - 1:bis_index + 1]
            return bis
        return ''

    def getDivision(self):
        IG_division = self.getData('DIV.      CAD.')
        try:
            division = self.getValueMapping('division_map')[IG_division]
        except:
            self.logError(self, self.line, 'No division found')
            return
        result = {'division': division, 'divisioncode': division}
        return result

    def tokenizeReference(self, reference):
        reference = cleanAndSplitWord(reference)
        # we do not use 'partie' in parcel search
        reference = [part.upper() for part in reference if part not in ['pie', 'pi']]
        return reference

    def splitReferenceGroups(self, raw_references):
        if '-' in raw_references:
            return raw_references.split('-')
        elif ',' in raw_references:
            return raw_references.split(',')
        else:
            return [raw_references]

#
# UrbanEvent deposit
#

# factory


def convertDate(mapper, line, date):
    date = cleanAndSplitWord(date)
    if len(date) > 1:
        mapper.logError(mapper, line, 'More dates found')
    date = date and date[0] or date
    try:
        return date and DateTime(date) or None
    except:
        mapper.logError(mapper, line, 'Wrong date format', {'date': date})


class UrbanDepositEventFactory(BaseFactory):
    def getPortalType(self):
        return 'UrbanEvent'

    def create(self, place, **kwargs):
        if not kwargs['eventtype'] or not kwargs['eventDate']:
            return []
        event = place.createUrbanEvent(kwargs['eventtype'])
        event.setEventDate(kwargs['eventDate'])
        return [event]

#mappers


class DepositEventTypeMapper(Mapper):
    def mapEventtype(self, line):
        licence = self.importer.current_containers_stack[-1]
        urban_tool = getToolByName(licence, 'portal_urban')
        eventtype_id = self.getValueMapping('eventtype_id_map')[licence.portal_type]['deposit_event']
        config = urban_tool.getUrbanConfig(licence)
        return getattr(config.urbaneventtypes, eventtype_id).UID()


class DepositDateMapper(Mapper):
    def mapEventdate(self, line):
        date = self.getData('DATE ENTREE')
        date = convertDate(self, line, date)
        if not date:
            self.logError(self, line, 'No deposit date found')
        return date

#
# UrbanEvent decision
#

# factory


class UrbanDecisionEventFactory(BaseFactory):
    def getPortalType(self):
        return 'UrbanEvent'

    def create(self, place, **kwargs):
        if not kwargs['eventtype']:
            return []
        if place.portal_type in ['ParcelOutLicence', 'BuildLicence', 'UrbanCertificateTwo']:
            if not kwargs['decisionDate']:
                return []
        elif not kwargs['eventDate']:
            return []
        event = place.createUrbanEvent(kwargs['eventtype'])
        if place.portal_type in ['ParcelOutLicence', 'BuildLicence', 'UrbanCertificateTwo']:
            event.setDecisionDate(kwargs['decisionDate'])
        return [event]


#mappers


class DecisionEventTypeMapper(Mapper):
    def mapEventtype(self, line):
        licence = self.importer.current_containers_stack[-1]
        urban_tool = getToolByName(licence, 'portal_urban')
        eventtype_id = self.getValueMapping('eventtype_id_map')[licence.portal_type]['decision_event']
        config = urban_tool.getUrbanConfig(licence)
        return getattr(config.urbaneventtypes, eventtype_id).UID()


class DecisionDateMapper(Mapper):
    def mapDecisiondate(self, line):
        date = self.getData('DATE CBE')
        date = convertDate(self, line, date)
        if not date:
            self.logError(self, line, 'No decision date found')
        return date

    def mapEventdate(self, line):
        date = self.getData('DATE CBE')
        date = convertDate(self, line, date)
        if not date:
            self.logError(self, line, 'No decision date found')
        return date


class NotificationDateMapper(PostCreationMapper):
    def mapEventdate(self, line, plone_object):
        date = self.getData('DATE DE NOTIFICATION')
        date = convertDate(self, line, date)
        return date


class DecisionMapper(PostCreationMapper):
    def mapDecision(self, line, plone_object):
        decision = self.getData('DECISION CBE').lower()
        if 'autorisé' in decision:
            return 'favorable'
        elif 'refusé' in decision:
            return 'defavorable'
        #error
        return []
