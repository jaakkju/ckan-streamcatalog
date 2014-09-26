#!/usr/bin/python
# -*- coding: utf-8 -*-
from ckan.controllers.admin import AdminController

from ckan.lib.base import render
from ckan.common import c

import json

from ckanext.streamcatalog.controllers.wso2esb_controller import getBrokerClient


class admin(AdminController):

    def wso2esb(self):
        ''' Queries WSO2 ESB for information. '''

        brokerclient = getBrokerClient()
        subscriptions = brokerclient.getAllSubscriptions()

        c.subscriptions = json.loads(subscriptions)
        
        return render('admin/wso2esb.html')
