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

def unsubscriebe(suID):
    return brokerclient.unsubscribe(suID)

# This returns a Java object, it might be a problem
def getAllSubscriptions():
    return brokerclient.getAllSubscriptions()


class StreamCatalogPlugin(p.SingletonPlugin):
    ''' This is a plugin that add the possibility to add data streams as resources '''
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IResourcePreview, inherit=True)
    p.implements(p.IRoutes, inherit=True)

    stream_types = ['stream.json', 'stream.xml']

    def before_map(self, map):
        map.connect('/streamcatalog/tulosta',
          controller='ckanext.streamcatalog.controller:StreamCatalogController',
          action='tulosta')
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
                'streamcatalog_subscriebe': subscribe,
                'streamcatalog_unsubscriebe': unsubscriebe,
                'streamcatalog_getAllSubscriptions': getAllSubscriptions,
                'streamcatalog_createTopic': createTopic
            }