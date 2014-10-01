#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from py4j.protocol import Py4JJavaError

from ckan.lib.base import BaseController, render, abort
import ckan.model as model
import ckan.new_authz as new_authz
from ckan.logic import tuplize_dict, clean_dict, parse_params
from ckan.lib.navl.dictization_functions import unflatten
from ckan.logic import get_action
from ckan.common import _, request, c
import ckan.lib.helpers as h


''' Common helper functions required dealing with WSO2 ESB. '''

def getBrokerClient():
    ''' Gets BrokerClientWrapper java class to communicate with WSO2 ESB. '''

    from py4j.java_gateway import JavaGateway
    gateway = JavaGateway()

    return gateway.entry_point

def getPackageIdFromName(package_name):
    ''' Turn id (dataset's slug) to package_id (its actual id). '''
    
    package_data = get_action('package_show')({'model': model, 'session': model.Session, 'user': c.user or c.author, 'auth_user_obj': c.userobj}, {'id': package_name})
    if 'id' in package_data:
        return package_data['id']
    else:
        return None

def getResourceUrlName(resource_name):
    ''' Use resource id to get its url field value. '''

    resource_data = get_action('resource_show')({'model': model, 'session': model.Session, 'user': c.user or c.author, 'auth_user_obj': c.userobj}, {'id': resource_name})
    if 'url' in resource_data:
        return resource_data['url']
    else:
        return None

''' WSO2 ESB controller '''

log = logging.getLogger(__name__)

class WSO2ESB(BaseController):

    def topicsubscription_delete(self, subscription_id):
        ''' Delete a WSO2 ESB Topic's subscription. Note that no relation to CKAN is required! '''
        
        if not new_authz.is_sysadmin(c.user):
            abort(401, _('Unauthorized to delete WSO2 ESB Topic subscriptions'))

        brokerclient = getBrokerClient()
        brokerclient.unsubscribe(subscription_id)

        log.info(_('WSO2 ESB Topic subscription with an id {id} was deleted.').format(id=subscription_id))
        h.flash_notice(_('WSO2 ESB Topic subscription with an id {id} was deleted.').format(id=subscription_id))

        h.redirect_to(controller='admin', action='wso2esb')

    def topicsubscription_create(self):
        ''' Create a WSO2 ESB Topic's subscription. Note that no relation to CKAN will be made! '''
        
        if not new_authz.is_sysadmin(c.user):
            abort(401, _('Unauthorized to create WSO2 ESB Topic subscriptions'))

        data = clean_dict(unflatten(tuplize_dict(parse_params(request.POST))))
        if 'topic' not in data or not isinstance(data['topic'], basestring) or data['topic'] == '':
            h.flash_error(_('Error: missing topic field value.'))
            h.redirect_to(controller='admin', action='wso2esb')
        if 'url' not in data or not isinstance(data['url'], basestring) or data['url'] == '':
            h.flash_error(_('Error: missing url field value.'))
            h.redirect_to(controller='admin', action='wso2esb')

        topic = data['topic']
        url = data['url']

        brokerclient = getBrokerClient()
        subscription_id = brokerclient.subscribe("/" + topic, url)

        log.info(_('WSO2 ESB Topic subscription id {id} was created with url {url} to topic /{topic}.').format(id=subscription_id, url=url, topic=topic))
        h.flash_notice(_('WSO2 ESB Topic subscription id {id} was created with url {url} to topic /{topic}.').format(id=subscription_id, url=url, topic=topic))

        h.redirect_to(controller='admin', action='wso2esb')
