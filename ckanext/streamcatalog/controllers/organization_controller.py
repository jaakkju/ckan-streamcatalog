from ckanext.streamcatalog.controllers.group_controller import group


class organization(group):
    # this makes us use organization actions
    group_type = 'organization'

    def _guess_group_type(self, expecting_name=False):
        return 'organization'