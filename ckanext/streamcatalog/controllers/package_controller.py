#!/usr/bin/python
# -*- coding: utf-8 -*-
from ckan.controllers.package import PackageController

import ckan.model as model
from ckan.logic import tuplize_dict, clean_dict, parse_params
from ckan.lib.navl.dictization_functions import unflatten
from ckan.logic import get_action
from ckan.common import _, request, c

from py4j.protocol import Py4JJavaError

from ckanext.streamcatalog.controllers.wso2esb_controller import getBrokerClient, getPackageIdFromName, getResourceUrlName


class package(PackageController):

    def publish(self, id):
        ''' Publishes (sends) a message to WSO2 ESB Topic related to the dataset. '''
        
        data = clean_dict(unflatten(tuplize_dict(parse_params(request.POST))))
        if 'message' in data and isinstance(data['message'], basestring):
            if c.userobj.sysadmin:
                package_id = getPackageIdFromName(id)
                brokerclient = getBrokerClient()
                if brokerclient.publish(package_id, data['message']):
                    h.flash_notice(_('The message was sent.'))
                else:
                    h.flash_error(_('Error sending the message.'))
            else:
                h.flash_error(_('Error: sysadmin rights required to send a message.'))
        else:
            h.flash_error(_('Error: no message was provided.'))

        return super(package, self).read(id)

    def new_resource(self, id, data=None, errors=None, error_summary=None):
        ''' Before creating a resource into CKAN, we request WSO2 ESB to add a subscription to the related Topic. '''

        if request.method == 'POST' and not data:
            # Recogniced new resource form POST, extract variables.
            postdata = data or clean_dict(unflatten(tuplize_dict(parse_params(request.POST))))
            
            if 'save' in postdata and 'url' in postdata:
                package_id = getPackageIdFromName(id)
                # Add a new subscription for the topic named after the dataset, pointing to the URL given.
                brokerclient = getBrokerClient()
                try:
                    result = brokerclient.subscribe(package_id, postdata['url'])
                except Py4JJavaError, e:
                    # Errors are propagated to the CKAN controller below to prevent new resource creation.
                    error_message = str(e)
                    if 'Error While Subscribing :Cannot initialize URI with empty parameters.' in error_message:
                        error_message = _('Error While Subscribing: Cannot initialize URI with empty parameters.')
                    if 'org.apache.axis2.AxisFault: Connection refused' in error_message:
                        error_message = _('Error While Subscribing: Cannot connect to WSO2 ESB.')

                    if errors and isinstance(errors, dict):
                        errors.update({ 'error': error_message })
                    else:
                        errors = { 'error': error_message }
                    data = postdata
                    error_summary = { _('WSO2 ESB'): error_message }

        return super(package, self).new_resource(id, data, errors, error_summary)

    def resource_delete(self, id, resource_id):
        ''' Before deleting a resource from CKAN, we request WSO2 ESB to remove the subscription from the related Topic. '''

        import json

        subscription_id = None
        brokerclient = getBrokerClient()
        package_id = getPackageIdFromName(id)
        resource_url = getResourceUrlName(resource_id)
        # Cycle through subscriptions until the right one is found, then select its id.
        subscriptions = brokerclient.getAllSubscriptions()
        subscriptions = json.loads(subscriptions)
        for subscription in subscriptions:
            # Note here that CKAN appends http:// prefix into URLs if it's not present upon resource creation, causing mismatch here - so we must take that to account.
            if subscription['localTopic'] == '/' + package_id and subscription['localEventSinkAddress'] == resource_url or "http://" + subscription['localEventSinkAddress'] == resource_url:
                subscription_id = subscription['localSubscriptionId']

        # Since we now have access to the subscription id, simply use it to unsubscribe.
        # @TODO Try-catch?
        brokerclient.unsubscribe(subscription_id)

        return super(package, self).resource_delete(id, resource_id)