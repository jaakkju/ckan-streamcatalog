#!/usr/bin/python
# -*- coding: utf-8 -*-
from ckan.controllers.group import GroupController

import ckan.new_authz as new_authz
import ckan.model as model
from ckan.lib.base import render, abort
from ckan.logic import NotFound, NotAuthorized
from ckan.common import _, c

from ckanext.streamcatalog.activity import group_activity_list_html, organization_activity_list_html


class group(GroupController):

    ''' Overridde functions '''

    def activity(self, id, offset=0):
        '''Render this group's public activity stream page.'''

        # Only allow (logged in) admins to view activity streams.
        if not c.user or not new_authz.is_sysadmin(c.user):
            abort(401, _('Unauthorized to read activity streams for groups'))

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True}
        try:
            c.group_dict = self._get_group_dict(id)
        except NotFound:
            abort(404, _('Group not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read group {group_id}').format(group_id=id))

        # Add the group's activity stream (already rendered to HTML) to the
        # template context for the group/read.html template to retrieve later.
        if self.group_type != 'organization':
            c.group_activity_stream = group_activity_list_html(context, {'id': c.group_dict['id'], 'offset': offset})
        else:
            c.group_activity_stream = organization_activity_list_html(context, {'id': c.group_dict['id'], 'offset': offset})

        return render(self._activity_template(c.group_dict['type']))