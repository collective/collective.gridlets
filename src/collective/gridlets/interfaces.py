from zope.interface import Interface

from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.interfaces import IColumn

from z3c.form.interfaces import ITextLinesWidget


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
