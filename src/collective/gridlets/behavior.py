from zope.interface import alsoProvides
from zope import schema
from z3c.form.interfaces import IEditForm

from plone.supermodel import model
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider

from collective.gridlets import _
from collective.gridlets.widget import GridsterFieldWidget


class IGridlets(model.Schema):
    """Add gridlets serialization field to content
    """

    form.omitted('gridlets')
    form.no_omit(IEditForm, 'gridlets')
    form.widget(gridlets=GridsterFieldWidget)
    gridlets = schema.TextLine(
        title=_(u"Gridlets"),
        description=_(u"gridlets_description"),
        default=u'',
        required=False,
    )

alsoProvides(IGridlets, IFormFieldProvider)
