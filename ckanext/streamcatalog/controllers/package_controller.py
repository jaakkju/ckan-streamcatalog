#!/usr/bin/python
# -*- coding: utf-8 -*-
from ckan.controllers.package import PackageController
from ckan.lib.base import *

import ckan.model as model
from ckan.logic import tuplize_dict, clean_dict, parse_params
from ckan.lib.navl.dictization_functions import DataError, unflatten
from ckan.logic import NotFound, NotAuthorized, ValidationError
from ckan.logic import get_action, check_access

from ckan.common import OrderedDict, _, json, request, c, g, response


from urllib import urlencode
import ckan.plugins as p
import ckan.lib.maintain as maintain
from ckan.controllers.package import _encode_params, url_with_params, search_url
from ckan.lib.helpers import _create_url_with_params


class package(PackageController):

    def new_resource(self, id, data=None, errors=None, error_summary=None):
        if request.method == 'POST' and not data:
            # Recogniced new resource form POST, extract variables.
            data = data or clean_dict(unflatten(tuplize_dict(parse_params(request.POST))))
            if 'save' in data and 'url' in data:
                # Get BrokerClientWrapper java class to communicate with WSO2 ESB.
                from py4j.java_gateway import JavaGateway
                gateway = JavaGateway()
                brokerclient = gateway.entry_point
                # Add a new subscription for the topic named after the dataset, pointing to the URL given.
                result = brokerclient.subscribe(id, data['url'])
                #raise Exception(str(result))
        return super(package, self).new_resource(id, data, errors, error_summary)
