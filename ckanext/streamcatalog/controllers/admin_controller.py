#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from py4j.protocol import Py4JJavaError

from ckan.controllers.admin import AdminController
from ckan.lib.base import render
from ckan.common import c
import ckan.lib.helpers as h

from ckanext.streamcatalog.controllers.wso2esb_controller import getBrokerClient


class admin(AdminController):

    def wso2esb(self):
        ''' Queries WSO2 ESB for information. '''

        try:
            brokerclient = getBrokerClient()
            subscriptions = brokerclient.getAllSubscriptions()

            c.subscriptions = json.loads(subscriptions)
        except Py4JJavaError, e:
            h.flash_error(str(e))
        
        return render('admin/wso2esb.html')
