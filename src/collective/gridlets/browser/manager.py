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
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlets.interfaces import IPortletManager

from collective.gridlets.interfaces import IGridletsPortletManager
from collective.gridlets.interfaces import IGridletSettings
from Acquisition import aq_inner

import json


class GridletsAddPortletsRenderer(ContextualEditPortletManagerRenderer):
    """Render a portlet manager in edit mode for contextual portlets"""
    adapts(
        Interface,
        IDefaultBrowserLayer,
        IManageContextualPortletsView,
        IGridletsPortletManager
    )

    template = ViewPageTemplateFile('templates/add-portlets-widget.pt')

    def get_delete_action_url(self):
        return '{}/@@delete-gridlet'.format(self.baseUrl())

    def get_toggle_action_url(self):
        return '{}/@@toggle-gridlet-visibility'.format(self.baseUrl())


class GridletsContextualPortletManagerRenderer(ContextualEditPortletManagerRenderer):
    """Render a portlet manager in edit mode for contextual portlets"""
    adapts(
        Interface,
        IDefaultBrowserLayer,
        IManageContextualPortletsView,
        IGridletsPortletManager
    )

    template = ViewPageTemplateFile('templates/edit-manager-contextual.pt')

    def get_gridlet_position(self, portlet_hash):
        if self.context.gridlets:
            positions = json.loads(self.context.gridlets)
            for position in positions:
                if position['id'] == portlet_hash:
                    return position

            # We have a new portlet in the house so update the annotation
            positions.append({
                'id': portlet_hash,
                'row': 1,
                'col': 1,
                'size_x': 1,
                'size_y': 1
            })
            self.context.gridlets = json.dumps(positions)
            # And return a faked one for this time only
            return {'row': 1, 'col': 1, 'size_x': 1, 'size_y': 1}

        else:
            # Is the first portlet so init the value
            self.context.gridlets = json.dumps([{
                'id': portlet_hash,
                'row': 1,
                'col': 1,
                'size_x': 1,
                'size_y': 1
            }])

            # And return a faked one for this time only
            return {'row': 1, 'col': 1, 'size_x': 1, 'size_y': 1}


class GridletsManageContextualPortlets(ManageContextualPortlets):
    """ Define our very own view for manage portlets with our helper methods """

    def get_gridlet_position(self, portlet_hash):
        if self.context.gridlets:
            positions = json.loads(self.context.gridlets)
            for position in positions:
                if position['id'] == portlet_hash:
                    return position

            # We have a new portlet in the house so update the annotation
            positions.append({
                'id': portlet_hash,
                'row': 1,
                'col': 1,
                'size_x': 1,
                'size_y': 1
            })
            self.context.gridlets = json.dumps(positions)
            # And return a faked one for this time only
            return {'row': 1, 'col': 1, 'size_x': 1, 'size_y': 1}

        else:
            # Is the first portlet so init the value
            self.context.gridlets = json.dumps([{
                'id': portlet_hash,
                'row':1,
                'col': 1,
                'size_x': 1,
                'size_y':1
            }])

            # And return a faked one for this time only
            return {'row': 1, 'col': 1, 'size_x': 1, 'size_y': 1}


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

    @property
    def config(self):
        registry = getUtility(IRegistry)
        return registry.forInterface(IGridletSettings)

    def get_grid_portlets(self):
        results = {
            'unassigned': [],
            'gridlets': []
        }

        if getattr(self.context, 'gridlets', False):
            gridster = json.loads(self.context.gridlets)
        else:
            gridster = []

        # sort by row and column
        gridster.sort(key=lambda x: x['row'] ^ x['col'])

        # get all portlet by hash
        portlets = {i['hash']: i for i in self.allPortlets()}

        rows = {}
        layout_columns = self.config.n_of_columns
        grid_system_columns = self.config.grid_system_columns
        column_ratio = grid_system_columns / layout_columns
        remainder = grid_system_columns % layout_columns

        positions = {}
        # for each element in my grid
        # I get a portlet
        # set its properties
        # and I populate a dictionary of rows that contains
        # another dictionary of columns...
        for element in gridster:
            _portlet = portlets[element['id']]
            width = int(element['size_x'] * column_ratio)
            row_idx = element['row']
            row = rows.get(row_idx)

            if not row:
                row = rows[row_idx] = {}
                positions[row_idx] = 0

            current_position = positions[row_idx]
            positions[row_idx] += width

            # help me column doesn't fit the grid system...
            # We fix that...
            if (positions[row_idx] + remainder) == grid_system_columns:
                width += remainder

            tile = {
                'css_class': self.config.css_cell_class.format(
                    position=current_position,
                    width=width
                ),
                'hash': _portlet['hash'],
                'category': _portlet['category'],
                'available': _portlet['available'],
                'name': _portlet['name'],
                'assignment': _portlet['assignment'],
                'manager': _portlet['manager'],
                'renderer': _portlet['renderer'],
                'key': _portlet['key']
            }
            row[element['col']] = tile

        rows_idx = rows.keys()
        rows_idx.sort()
        for idx in rows_idx:
            row = rows[idx]
            cols_idx = row.keys()
            cols_idx.sort()
            results['gridlets'].append([row[i] for i in cols_idx])

        return results
