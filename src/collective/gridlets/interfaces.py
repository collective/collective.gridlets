from zope.interface import Interface
from zope import schema
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.interfaces import IColumn

from z3c.form.interfaces import ITextLinesWidget
from collective.gridlets import _


class IHomepage(Interface):
    """
    Marker interface for the homepage content type.
    """


class IGridsterWidget(ITextLinesWidget):
    """Text lines widget for Gridster serialization."""


class IGridletsPortletManager(IPortletManager, IColumn):
    """
    Superclass used by our adapter
    The IColumn bit means that we can add all the portlets available to
     the right-hand and left-hand column portlet managers
    """


class IGridletsLayer(Interface):
    """
    Marker interface for the product layer.
    """


class IGridletSettings(Interface):
    css_row_class = schema.TextLine(
        title=_(u"CSS class for row div"),
        description=_(u"eg.: row")
    )

    css_cell_class = schema.TextLine(
        title=_(u"CSS class for cell"),
        description=_(u"eg.: cell width-{width} position-{position}")
    )

    n_of_columns = schema.Int(
        title=_(u"Max number of column for your layout"),
        description=_(u"")
    )

    grid_system_columns = schema.Int(
        title=_(u"Max number of column for your grid system"),
        description=_(u"")
    )
