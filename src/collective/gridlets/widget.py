# -*- coding: utf-8 -*-
from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import textarea
from z3c.form.converter import BaseDataConverter

from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletManager
from collective.gridlets.browser.manager import GridletsAddPortletsRenderer

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import adapter
from zope.interface import implementer
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget

from collective.gridlets.interfaces import IGridsterWidget

import json
import zope.component
import zope.interface
import zope.schema


class GridsterWidget(textarea.TextAreaWidget):
    """Widget for Gridster Input area."""
    zope.interface.implementsOnly(IGridsterWidget)
    klass = u"gridster-widget"
    display_template = ViewPageTemplateFile('browser/templates/gridster_display.pt')
    input_template = ViewPageTemplateFile('browser/templates/gridster_input.pt')

    # JavaScript template
    js_template = u"""\
    (function($) {
        $().ready(function() {
            $('.gridster ul').gridster({
                widget_margins: [10, 10],
                widget_base_dimensions: [150, 150],
                max_cols: 6,
                resize: {
                  enabled: true,
                  axes: ['x'],
                  stop: function(e, ui, $widget) {
                    data = {
                      position: JSON.stringify(this.serialize())
                    }
                    $('#'+'%(id)s').val(data.position);
                  }
                },
                draggable: {
                  stop: function(event, ui) {
                    data = {
                      position: JSON.stringify(this.serialize())
                    };
                    $('#'+'%(id)s').val(data.position);
                  }
                },
                serialize_params: function($w, wgd) {
                  return {
                    id: $($w).data().portlethash,
                    col: wgd.col,
                    row: wgd.row,
                    size_x: wgd.size_x,
                    size_y: wgd.size_y
                  };
                }
            });

        // var gridster = $(".gridster ul").gridster().data('gridster');

        });
    })(jQuery);
    """

    def js(self):
        return self.js_template % dict(id=self.id)

    def render(self):
        if self.mode == interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)

    def getIt(self):
        pass

    def render_edit_portlet_manager(self):
        managerview = self.get_portlet_manager_view()
        managerview.update()
        return managerview.render()

    def get_portlet_manager_view(self):
        manageview = getMultiAdapter((self.context, self.request), name="manage-portlets")
        manager = getUtility(IPortletManager, name='collective.gridlets.portletManager')
        return GridletsAddPortletsRenderer(self.context, self.request, manageview, manager)

    def get_gridlet_position(self, portlet_hash):
        if getattr(self.context, 'gridlets', False):
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
            import transaction
            transaction.commit()

            # And return a faked one for this time only
            return dict(row=1, col=1, size_x=1, size_y=1)


@zope.interface.implementer(interfaces.IFieldWidget)
def GridsterFieldWidget(field, request):
    """IFieldWidget factory for GridsterWidget."""
    return widget.FieldWidget(field, GridsterWidget(request))
