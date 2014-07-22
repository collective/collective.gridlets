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

    def get_toggle_action_url(self):
        return '{}/@@toggle-gridlet-visibility'.format(self.baseUrl())


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
        return self.finish_portlet_change()


class GridletsPortletRenderer(ColumnPortletManagerRenderer):
    """
    A renderer for the Genweb portlets
    """
    adapts(Interface, IDefaultBrowserLayer, IBrowserView, IGridletsPortletManager)
    template = ViewPageTemplateFile('templates/renderer.pt')

    def get_grid_portlets(self):

        grid = dict(unassigned=[], gridlets=[])

        if getattr(self.context, 'gridlets', False):
            grid_positions = json.loads(self.context.gridlets)
        else:
            grid_positions = []

        # First index the positions
        indexed_positions = {}
        for grid_position in grid_positions:
            indexed_positions[grid_position['id']] = grid_position

        indexed_by_row = {}
        for portlet in self.allPortlets():
            if portlet['hash'] in indexed_positions:
                portlet_position = indexed_positions[portlet['hash']]
                indexed_by_row.setdefault(portlet_position['row'], [])
                indexed_by_row[portlet_position['row']].append(dict(row=portlet_position['row'],
                                                                    col=portlet_position['col'],
                                                                    size_x=str(int(portlet_position['size_x'] * 1)),
                                                                    size_y=portlet_position['size_y'],
                                                                    hash=portlet['hash'],
                                                                    category=portlet['category'],
                                                                    available=portlet['available'],
                                                                    name=portlet['name'],
                                                                    assignment=portlet['assignment'],
                                                                    manager=portlet['manager'],
                                                                    renderer=portlet['renderer'],
                                                                    key=portlet['key']))
            else:
                # We have an unsaved (unassigned) portlet, so append it to the
                # unassigned list
                grid['unassigned'].append(dict(hash=portlet['hash'],
                                               category=portlet['category'],
                                               available=portlet['available'],
                                               name=portlet['name'],
                                               assignment=portlet['assignment'],
                                               manager=portlet['manager'],
                                               renderer=portlet['renderer'],
                                               key=portlet['key']))

        for k in sorted(indexed_by_row):
            grid['gridlets'].append(sorted(indexed_by_row[k], key=lambda x: x['col']))

        return grid

        # allportlets = {}
        # for portlet in unordered_portlets:
        #     allportlets[portlet['hash']] = portlet

        # if self.context.gridlets:
        #     positions = json.loads(self.context.gridlets)
        #     index = {}
        #     # {1: [portlet1, portlet2]}
        #     for portlet in positions:
        #         index.setdefault(portlet['row'], [])
        #         portlet_info = allportlets.get(portlet['id'], False)
        #         if portlet_info:
        #             index[portlet['row']].append(dict(row=portlet['row'],
        #                                               col=portlet['col'],
        #                                               size_x=str(int(portlet['size_x'] * 2)),
        #                                               size_y=portlet['size_y'],
        #                                               hash=portlet['id'],
        #                                               category=portlet_info['category'],
        #                                               available=portlet_info['available'],
        #                                               name=portlet_info['name'],
        #                                               assignment=portlet_info['assignment'],
        #                                               manager=portlet_info['manager'],
        #                                               renderer=portlet_info['renderer'],
        #                                               key=portlet_info['key']))
        #         else:
        #             # We have an unsaved portlet, so assign it to (1, 1)
        #             index.setdefault('unassigned', [])
        #             index['unassigned'].append(dict(hash=portlet['id'],
        #                                             category=portlet_info['category'],
        #                                             available=portlet_info['available'],
        #                                             name=portlet_info['name'],
        #                                             assignment=portlet_info['assignment'],
        #                                             manager=portlet_info['manager'],
        #                                             renderer=portlet_info['renderer'],
        #                                             key=portlet_info['key']))
        #     grid_portlets = []
        #     for k in sorted(index.keys()):
        #         grid_portlets.append(sorted(index[k], key=lambda x: x['col']))
        #     import ipdb;ipdb.set_trace()
        #     return grid_portlets
        # else:
        #     # We have no gridlets because it's the first one and we haven't
        #     # either positioned it or change its size.
        #     grid_portlets = []
        #     list_portlets = []
        #     for portlet_info in unordered_portlets:
        #         list_portlets.append(dict(row='1',
        #                                   col='1',
        #                                   size_x='2',
        #                                   size_y='1',
        #                                   hash=portlet['hash'],
        #                                   category=portlet_info['category'],
        #                                   available=portlet_info['available'],
        #                                   name=portlet_info['name'],
        #                                   assignment=portlet_info['assignment'],
        #                                   manager=portlet_info['manager'],
        #                                   renderer=portlet_info['renderer'],
        #                                   key=portlet_info['key']))

        #     grid_portlets.append(list_portlets)
        #     return grid_portlets
