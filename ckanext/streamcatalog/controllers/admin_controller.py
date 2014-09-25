#!/usr/bin/python
# -*- coding: utf-8 -*-
from ckan.controllers.admin import AdminController

import ckan.lib.base as base
from ckan.common import c

import json


def getBrokerClient():
    ''' Gets BrokerClientWrapper java class to communicate with WSO2 ESB. '''

    from py4j.java_gateway import JavaGateway
    gateway = JavaGateway()
    return gateway.entry_point


class admin(AdminController):

    def wso2esb(self):
        ''' Queries WSO2 ESB for information. '''

        brokerclient = getBrokerClient()
        subscriptions = brokerclient.getAllSubscriptions()

        from py4j.java_gateway import get_method, get_field

        c.subscriptions = json.loads(subscriptions)
        
        return base.render('admin/wso2esb.html')
