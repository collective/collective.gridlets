from zope import schema
from zope.component import adapts, getUtility, getMultiAdapter
from zope.interface import Interface, implements
from zope.container  import contained

from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from plone.app.portlets.manager import ColumnPortletManagerRenderer
from plone.app.portlets.browser.manage import ManageContextualPortlets
from plone.app.portlets.browser.interfaces import IManageContextualPortletsView
from plone.app.portlets.browser.editmanager import ContextualEditPortletManagerRenderer
from plone.app.portlets.browser.editmanager import ManagePortletAssignments
from plone.portlets.interfaces import IPortletAssignmentSettings
from plone.app.portlets.interfaces import IPortletPermissionChecker

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlets.interfaces import IPortletManager

from collective.gridlets.interfaces import IGridletsPortletManager
from Acquisition import aq_inner

import json


class GridletsAddPortletsRenderer(ContextualEditPortletManagerRenderer):
    """Render a portlet manager in edit mode for contextual portlets"""
    adapts(Interface, IDefaultBrowserLayer, IManageContextualPortletsView, IGridletsPortletManager)

    template = ViewPageTemplateFile('templates/add-portlets-widget.pt')

    def get_delete_action_url(self):
        return '{}/@@delete-gridlet'.format(self.baseUrl())


class GridletsContextualPortletManagerRenderer(ContextualEditPortletManagerRenderer):
    """Render a portlet manager in edit mode for contextual portlets"""
    adapts(Interface, IDefaultBrowserLayer, IManageContextualPortletsView, IGridletsPortletManager)

    template = ViewPageTemplateFile('templates/edit-manager-contextual.pt')

    def get_gridlet_position(self, portlet_hash):
        if self.context.gridlets:
            positions = json.loads(self.context.gridlets)
            for position in positions:
                if position['id'] == portlet_hash:
                    return position

            # We have a new portlet in the house so update the annotation
            positions.append(dict(id=portlet_hash, row=1, col=1, size_x=1, size_y=1))
            self.context.gridlets = json.dumps(positions)
            # And return a faked one for this time only
            return dict(row=1, col=1, size_x=1, size_y=1)

        else:
            # Is the first portlet so init the value
            self.context.gridlets = json.dumps([dict(id=portlet_hash, row=1, col=1, size_x=1, size_y=1)])

            # And return a faked one for this time only
            return dict(row=1, col=1, size_x=1, size_y=1)


class GridletsManageContextualPortlets(ManageContextualPortlets):
    """ Define our very own view for manage portlets with our helper methods """

    def get_gridlet_position(self, portlet_hash):
        if self.context.gridlets:
            positions = json.loads(self.context.gridlets)
            for position in positions:
                if position['id'] == portlet_hash:
                    return position

            # We have a new portlet in the house so update the annotation
            positions.append(dict(id=portlet_hash, row=1, col=1, size_x=1, size_y=1))
            self.context.gridlets = json.dumps(positions)
            # And return a faked one for this time only
            return dict(row=1, col=1, size_x=1, size_y=1)

        else:
            # Is the first portlet so init the value
            self.context.gridlets = json.dumps([dict(id=portlet_hash, row=1, col=1, size_x=1, size_y=1)])

            # And return a faked one for this time only
            return dict(row=1, col=1, size_x=1, size_y=1)


class ManageGridletsPortletAssignments(ManagePortletAssignments):

    def delete_gridlet(self, name):
        self.authorize()
        assignments = aq_inner(self.context)
        IPortletPermissionChecker(assignments)()

        # set fixing_up to True to let zope.container.contained
        # know that our object doesn't have __name__ and __parent__
        fixing_up = contained.fixing_up
        contained.fixing_up = True

        del assignments[name]

        # revert our fixing_up customization
        contained.fixing_up = fixing_up

        return self.finish_portlet_change()

    def toggle_gridlet_visibility(self, name):
        self.authorize()
        assignments = aq_inner(self.context)
        settings = IPortletAssignmentSettings(assignments[name])
        visible = settings.get('visible', True)
        settings['visible'] = not visible
        import ipdb;ipdb.set_trace()
        return self.finish_portlet_change()
