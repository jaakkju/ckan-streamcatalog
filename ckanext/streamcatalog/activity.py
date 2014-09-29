import re
import datetime

from pylons import config
from webhelpers.html import literal

import ckan.lib.helpers as h
import ckan.lib.base as base
import ckan.lib.dictization.model_dictize as model_dictize
import ckan.logic as logic
from ckan.logic.action.get import dashboard_activity_list
import ckan.model as model

from ckan.common import _, c

_check_access = logic.check_access

''' 
This file is a forced copy-pasta of ckan/lib/activity_streams.py due to the inability to overwrite activity streams.

Here we simply replace all occurrances of "dataset" with "datastream".

@TODO: Refactor everything - if possible...
'''

# Salvage what we do not need to rewrite.
from ckan.lib.activity_streams import get_snippet_actor, get_snippet_user, get_snippet_dataset, \
                                      get_snippet_tag, get_snippet_group, get_snippet_organization, \
                                      get_snippet_extra, get_snippet_resource, get_snippet_related_item, \
                                      get_snippet_related_type

# activity_stream_string_*() functions return translatable string
# representations of activity types, the strings contain placeholders like
# {user}, {dataset} etc. to be replaced with snippets from the get_snippet_*()
# functions above.

''' Replacements and salvaging in the order of appearance. '''

def activity_stream_string_added_tag(context, activity):
    return _("{actor} added the tag {tag} to the datastream {dataset}")

from ckan.lib.activity_streams import activity_stream_string_changed_group, activity_stream_string_changed_organization

def activity_stream_string_changed_package(context, activity):
    return _("{actor} updated the datastream {dataset}")

def activity_stream_string_changed_package_extra(context, activity):
    return _("{actor} changed the extra {extra} of the datastream {dataset}")

def activity_stream_string_changed_resource(context, activity):
    return _("{actor} updated the subscription {resource} in the datastream {dataset}")

from ckan.lib.activity_streams import activity_stream_string_changed_user

def activity_stream_string_changed_related_item(context, activity):
    if activity['data'].get('dataset'):
        return _("{actor} updated the {related_type} {related_item} of the "
                "datastream {dataset}")
    else:
        return _("{actor} updated the {related_type} {related_item}")

from ckan.lib.activity_streams import activity_stream_string_deleted_group, activity_stream_string_deleted_organization

def activity_stream_string_deleted_package(context, activity):
    return _("{actor} deleted the datastream {dataset}")

def activity_stream_string_deleted_package_extra(context, activity):
    return _("{actor} deleted the extra {extra} from the datastream {dataset}")

def activity_stream_string_deleted_resource(context, activity):
    return _("{actor} deleted the subscription {resource} from the datastream "
             "{dataset}")

from ckan.lib.activity_streams import activity_stream_string_new_group, activity_stream_string_new_organization

def activity_stream_string_new_package(context, activity):
    return _("{actor} created the datastream {dataset}")

def activity_stream_string_new_package_extra(context, activity):
    return _("{actor} added the extra {extra} to the datastream {dataset}")

def activity_stream_string_new_resource(context, activity):
    return _("{actor} added the subscription {resource} to the datastream {dataset}")

from ckan.lib.activity_streams import activity_stream_string_new_user

def activity_stream_string_removed_tag(context, activity):
    return _("{actor} removed the tag {tag} from the datastream {dataset}")

from ckan.lib.activity_streams import activity_stream_string_deleted_related_item, activity_stream_string_follow_dataset, \
                                      activity_stream_string_follow_user, activity_stream_string_follow_group

def activity_stream_string_new_related_item(context, activity):
    if activity['data'].get('dataset'):
        return _("{actor} added the {related_type} {related_item} to the "
                 "datastream {dataset}")
    else:
        return _("{actor} added the {related_type} {related_item}")

# A dictionary mapping activity snippets to functions that expand the snippets.
activity_snippet_functions = {
    'actor': get_snippet_actor,
    'user': get_snippet_user,
    'dataset': get_snippet_dataset,
    'tag': get_snippet_tag,
    'group': get_snippet_group,
    'organization': get_snippet_organization,
    'extra': get_snippet_extra,
    'resource': get_snippet_resource,
    'related_item': get_snippet_related_item,
    'related_type': get_snippet_related_type,
}

# A dictionary mapping activity types to functions that return translatable
# string descriptions of the activity types.
activity_stream_string_functions = {
  'added tag': activity_stream_string_added_tag,
  'changed group': activity_stream_string_changed_group,
  'changed organization': activity_stream_string_changed_organization,
  'changed package': activity_stream_string_changed_package,
  'changed package_extra': activity_stream_string_changed_package_extra,
  'changed resource': activity_stream_string_changed_resource,
  'changed user': activity_stream_string_changed_user,
  'changed related item': activity_stream_string_changed_related_item,
  'deleted group': activity_stream_string_deleted_group,
  'deleted organization': activity_stream_string_deleted_organization,
  'deleted package': activity_stream_string_deleted_package,
  'deleted package_extra': activity_stream_string_deleted_package_extra,
  'deleted resource': activity_stream_string_deleted_resource,
  'new group': activity_stream_string_new_group,
  'new organization': activity_stream_string_new_organization,
  'new package': activity_stream_string_new_package,
  'new package_extra': activity_stream_string_new_package_extra,
  'new resource': activity_stream_string_new_resource,
  'new user': activity_stream_string_new_user,
  'removed tag': activity_stream_string_removed_tag,
  'deleted related item': activity_stream_string_deleted_related_item,
  'follow dataset': activity_stream_string_follow_dataset,
  'follow user': activity_stream_string_follow_user,
  'follow group': activity_stream_string_follow_group,
  'new related item': activity_stream_string_new_related_item,
}

# A dictionary mapping activity types to the icons associated to them
activity_stream_string_icons = {
  'added tag': 'tag',
  'changed group': 'group',
  'changed package': 'sitemap',
  'changed package_extra': 'edit',
  'changed resource': 'file',
  'changed user': 'user',
  'deleted group': 'group',
  'deleted package': 'sitemap',
  'deleted package_extra': 'edit',
  'deleted resource': 'file',
  'new group': 'group',
  'new package': 'sitemap',
  'new package_extra': 'edit',
  'new resource': 'file',
  'new user': 'user',
  'removed tag': 'tag',
  'deleted related item': 'picture',
  'follow dataset': 'sitemap',
  'follow user': 'user',
  'follow group': 'group',
  'new related item': 'picture',
  'changed organization': 'briefcase',
  'deleted organization': 'briefcase',
  'new organization': 'briefcase',
  'undefined': 'certificate', # This is when no activity icon can be found
}

# A list of activity types that may have details
activity_stream_actions_with_detail = ['changed package']

def activity_list_to_html(context, activity_stream, extra_vars):
    '''Return the given activity stream as a snippet of HTML.

    :param activity_stream: the activity stream to render
    :type activity_stream: list of activity dictionaries
    :param extra_vars: extra variables to pass to the activity stream items
        template when rendering it
    :type extra_vars: dictionary

    :rtype: HTML-formatted string

    '''
    activity_list = [] # These are the activity stream messages.
    for activity in activity_stream:
        detail = None
        activity_type = activity['activity_type']
        # Some activity types may have details.
        if activity_type in activity_stream_actions_with_detail:
            details = logic.get_action('activity_detail_list')(context=context,
                data_dict={'id': activity['id']})
            # If an activity has just one activity detail then render the
            # detail instead of the activity.
            if len(details) == 1:
                detail = details[0]
                object_type = detail['object_type']

                if object_type == 'PackageExtra':
                    object_type = 'package_extra'

                new_activity_type = '%s %s' % (detail['activity_type'],
                                            object_type.lower())
                if new_activity_type in activity_stream_string_functions:
                    activity_type = new_activity_type

        if not activity_type in activity_stream_string_functions:
            raise NotImplementedError("No activity renderer for activity "
                "type '%s'" % activity_type)

        if activity_type in activity_stream_string_icons:
            activity_icon = activity_stream_string_icons[activity_type]
        else:
            activity_icon = activity_stream_string_icons['undefined']

        activity_msg = activity_stream_string_functions[activity_type](context,
                activity)

        # Get the data needed to render the message.
        matches = re.findall('\{([^}]*)\}', activity_msg)
        data = {}
        for match in matches:
            snippet = activity_snippet_functions[match](activity, detail)
            data[str(match)] = snippet

        activity_list.append({'msg': activity_msg,
                              'type': activity_type.replace(' ', '-').lower(),
                              'icon': activity_icon,
                              'data': data,
                              'timestamp': activity['timestamp'],
                              'is_new': activity.get('is_new', False)})
    extra_vars['activities'] = activity_list
    return literal(base.render('activity_streams/activity_stream_items.html',
        extra_vars=extra_vars))

''' Helpers copied from ckan/logic/action/get.py which use the activity_list_to_html function redefined above. '''

def user_activity_list_html(context, data_dict):
    '''Return a user's public activity stream as HTML.

    The activity stream is rendered as a snippet of HTML meant to be included
    in an HTML page, i.e. it doesn't have any HTML header or footer.

    :param id: The id or name of the user.
    :type id: string
    :param offset: where to start getting activity items from
        (optional, default: 0)
    :type offset: int
    :param limit: the maximum number of activities to return
        (optional, default: 31, the default value is configurable via the
        ckan.activity_list_limit setting)
    :type limit: int

    :rtype: string

    '''
    activity_stream = user_activity_list(context, data_dict)
    offset = int(data_dict.get('offset', 0))
    extra_vars = {
        'controller': 'user',
        'action': 'activity',
        'id': data_dict['id'],
        'offset': offset,
        }
    return activity_list_to_html(context, activity_stream, extra_vars)

def package_activity_list(context, data_dict):
    '''Return a package's activity stream.

    You must be authorized to view the package.

    :param id: the id or name of the package
    :type id: string
    :param offset: where to start getting activity items from
        (optional, default: 0)
    :type offset: int
    :param limit: the maximum number of activities to return
        (optional, default: 31, the default value is configurable via the
        ckan.activity_list_limit setting)
    :type limit: int

    :rtype: list of dictionaries

    '''
    # FIXME: Filter out activities whose subject or object the user is not
    # authorized to read.
    _check_access('package_show', context, data_dict)

    model = context['model']

    package_ref = data_dict.get('id')  # May be name or ID.
    package = model.Package.get(package_ref)
    if package is None:
        raise logic.NotFound

    offset = int(data_dict.get('offset', 0))
    limit = int(
        data_dict.get('limit', config.get('ckan.activity_list_limit', 31)))

    activity_objects = model.activity.package_activity_list(package.id,
            limit=limit, offset=offset)
    return model_dictize.activity_list_dictize(activity_objects, context)

def package_activity_list_html(context, data_dict):
    '''Return a package's activity stream as HTML.

    The activity stream is rendered as a snippet of HTML meant to be included
    in an HTML page, i.e. it doesn't have any HTML header or footer.

    :param id: the id or name of the package
    :type id: string
    :param offset: where to start getting activity items from
        (optional, default: 0)
    :type offset: int
    :param limit: the maximum number of activities to return
        (optional, default: 31, the default value is configurable via the
        ckan.activity_list_limit setting)
    :type limit: int

    :rtype: string

    '''
    activity_stream = package_activity_list(context, data_dict)
    offset = int(data_dict.get('offset', 0))
    extra_vars = {
        'controller': 'package',
        'action': 'activity',
        'id': data_dict['id'],
        'offset': offset,
        }
    return activity_list_to_html(context, activity_stream, extra_vars)

def group_activity_list(context, data_dict):
    '''Return a group's activity stream.

    You must be authorized to view the group.

    :param id: the id or name of the group
    :type id: string
    :param offset: where to start getting activity items from
        (optional, default: 0)
    :type offset: int
    :param limit: the maximum number of activities to return
        (optional, default: 31, the default value is configurable via the
        ckan.activity_list_limit setting)
    :type limit: int

    :rtype: list of dictionaries

    '''
    # FIXME: Filter out activities whose subject or object the user is not
    # authorized to read.
    _check_access('group_show', context, data_dict)

    model = context['model']
    group_id = data_dict.get('id')
    offset = data_dict.get('offset', 0)
    limit = int(
        data_dict.get('limit', config.get('ckan.activity_list_limit', 31)))

    # Convert group_id (could be id or name) into id.
    group_show = logic.get_action('group_show')
    group_id = group_show(context, {'id': group_id})['id']

    activity_objects = model.activity.group_activity_list(group_id,
            limit=limit, offset=offset)
    return model_dictize.activity_list_dictize(activity_objects, context)

def group_activity_list_html(context, data_dict):
    '''Return a group's activity stream as HTML.

    The activity stream is rendered as a snippet of HTML meant to be included
    in an HTML page, i.e. it doesn't have any HTML header or footer.

    :param id: the id or name of the group
    :type id: string
    :param offset: where to start getting activity items from
        (optional, default: 0)
    :type offset: int
    :param limit: the maximum number of activities to return
        (optional, default: 31, the default value is configurable via the
        ckan.activity_list_limit setting)
    :type limit: int

    :rtype: string

    '''
    activity_stream = group_activity_list(context, data_dict)
    offset = int(data_dict.get('offset', 0))
    extra_vars = {
        'controller': 'group',
        'action': 'activity',
        'id': data_dict['id'],
        'offset': offset,
        }
    return activity_list_to_html(context, activity_stream, extra_vars)

def organization_activity_list(context, data_dict):
    '''Return a organization's activity stream.

    :param id: the id or name of the organization
    :type id: string

    :rtype: list of dictionaries

    '''
    # FIXME: Filter out activities whose subject or object the user is not
    # authorized to read.
    _check_access('organization_show', context, data_dict)

    model = context['model']
    org_id = data_dict.get('id')
    offset = data_dict.get('offset', 0)
    limit = int(
        data_dict.get('limit', config.get('ckan.activity_list_limit', 31)))

    # Convert org_id (could be id or name) into id.
    org_show = logic.get_action('organization_show')
    org_id = org_show(context, {'id': org_id})['id']

    activity_objects = model.activity.group_activity_list(org_id,
            limit=limit, offset=offset)
    return model_dictize.activity_list_dictize(activity_objects, context)

def organization_activity_list_html(context, data_dict):
    '''Return a organization's activity stream as HTML.

    The activity stream is rendered as a snippet of HTML meant to be included
    in an HTML page, i.e. it doesn't have any HTML header or footer.

    :param id: the id or name of the organization
    :type id: string

    :rtype: string

    '''
    activity_stream = organization_activity_list(context, data_dict)
    offset = int(data_dict.get('offset', 0))
    extra_vars = {
        'controller': 'organization',
        'action': 'activity',
        'id': data_dict['id'],
        'offset': offset,
        }

    return activity_list_to_html(context, activity_stream, extra_vars)

def recently_changed_packages_activity_list_html(context, data_dict):
    '''Return the activity stream of all recently changed packages as HTML.

    The activity stream includes all recently added or changed packages. It is
    rendered as a snippet of HTML meant to be included in an HTML page, i.e. it
    doesn't have any HTML header or footer.

    :param offset: where to start getting activity items from
        (optional, default: 0)
    :type offset: int
    :param limit: the maximum number of activities to return
        (optional, default: 31, the default value is configurable via the
        ckan.activity_list_limit setting)
    :type limit: int

    :rtype: string

    '''
    activity_stream = recently_changed_packages_activity_list(context,
            data_dict)
    offset = int(data_dict.get('offset', 0))
    extra_vars = {
        'controller': 'package',
        'action': 'activity',
        'offset': offset,
        }
    return activity_list_to_html(context, activity_stream, extra_vars)

def dashboard_activity_list_html(context, data_dict):
    '''Return the authorized user's dashboard activity stream as HTML.

    The activity stream is rendered as a snippet of HTML meant to be included
    in an HTML page, i.e. it doesn't have any HTML header or footer.

    :param id: the id or name of the user
    :type id: string
    :param offset: where to start getting activity items from
        (optional, default: 0)
    :type offset: int
    :param limit: the maximum number of activities to return
        (optional, default: 31, the default value is configurable via the
        ckan.activity_list_limit setting)
    :type limit: int

    :rtype: string

    '''
    activity_stream = dashboard_activity_list(context, data_dict)
    model = context['model']
    offset = data_dict.get('offset', 0)
    extra_vars = {
        'controller': 'user',
        'action': 'dashboard',
        'offset': offset,
    }
    return activity_list_to_html(context, activity_stream, extra_vars)

''' Overwritten activity stream helpers from ckan/lib/helpers.py. '''

def dashboard_activity_stream(user_id, filter_type=None, filter_id=None, offset=0):
    '''Return the dashboard activity stream of the current user.

    :param user_id: the id of the user
    :type user_id: string

    :param filter_type: the type of thing to filter by
    :type filter_type: string

    :param filter_id: the id of item to filter by
    :type filter_id: string

    :returns: an activity stream as an HTML snippet
    :rtype: string

    '''
    context = {'model': model, 'session': model.Session, 'user': c.user}

    if filter_type:
        action_functions = {
            'dataset': package_activity_list_html,
            'user': user_activity_list_html,
            'group': group_activity_list_html
        }
        action_function = action_functions.get(filter_type)
        return action_function(context, {'id': filter_id, 'offset': offset})
    else:
        return dashboard_activity_list_html(context, {'offset': offset})
