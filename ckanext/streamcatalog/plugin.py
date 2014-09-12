#from py4j.java_gateway import JavaGateway
import logging
import uuid

import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
''' The plugins toolkit is a Python module containing core functions, classes and exceptions for CKAN plugins to use. '''

#gateway = JavaGateway()
#brokerclient = gateway.entry_point
log = logging.getLogger(__name__)

''' Helper functions that can be called from CKAN snippet '''

def createTopic():
    topicID = str(uuid.uuid1())
    brokerclient.createTopic(topicID);
    # log.info('UserID:'  ' Created topic, ID: ' + topicID)

    return topicID

def subscribe(topicID, eventSinkUrl):
    return brokerclient.subscribe(topicID, eventSinkUrl)

def unsubscribe(suID):
    return brokerclient.unsubscribe(suID)

def getAllSubscriptions(package_id = None, user_id = None):
    import ckan.model as model
    
    q = model.Session.query(model.User, model.Resource) \
             .join(model.Activity, model.Activity.user_id==model.User.id) \
             .join(model.ActivityDetail, model.ActivityDetail.activity_id==model.Activity.id) \
             .join(model.Resource, model.ActivityDetail.object_id==model.Resource.id)
    if package_id:
        q = q.filter(model.Activity.object_id == package_id)
    if user_id:
        q = q.filter(model.Activity.user_id == user_id)
    q = q.filter(model.ActivityDetail.object_type == 'Resource')
    q = q.filter(model.ActivityDetail.activity_type == 'new')

    return q.all()


class StreamCatalogPlugin(p.SingletonPlugin):
    ''' This is a plugin that add the possibility to add data streams as resources '''
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IResourcePreview, inherit=True)
    p.implements(p.IRoutes, inherit=True)

    stream_types = ['stream.json', 'stream.xml']

    def before_map(self, map):
        map.connect('/streamcatalog/tulosta', controller='ckanext.streamcatalog.controller:StreamCatalogController', action='tulosta')
        map.connect('/dataset/new_resource/{id}', controller='ckanext.streamcatalog.controllers.package_controller:package', action='new_resource')
        return map
    
    def can_preview(self, data_dict):
        resource = data_dict['resource'];
        format_lower = resource['format'].lower()
        if format_lower in self.stream_types:
            return {'can_preview': True, 'quality': 2}

        return {'can_preview': False}

    def preview_template(self, context, data_dict):
        # String name of the template rendered
        return 'preview.html'

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        toolkit.add_template_directory(config, 'templates')

    def get_helpers(self):
        ''' Register functions above as a template helper function '''

        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
                'streamcatalog_subscribe': subscribe,
                'streamcatalog_unsubscribe': unsubscribe,
                'streamcatalog_getAllSubscriptions': getAllSubscriptions,
                'streamcatalog_createTopic': createTopic
            }