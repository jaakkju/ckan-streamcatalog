#!/usr/bin/python
# -*- coding: utf-8 -*-
from ckan.lib.base import *

import ckan.model as model
from ckan.logic import tuplize_dict, clean_dict, parse_params
from ckan.lib.navl.dictization_functions import unflatten
from ckan.logic import get_action

from ckan.common import _, request, c

from py4j.protocol import Py4JJavaError

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
