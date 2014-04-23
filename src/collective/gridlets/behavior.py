from rwproperty import getproperty, setproperty
from zope.component import adapts
from zope.interface import implements, alsoProvides
from zope import schema
from z3c.form.interfaces import IEditForm

from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent

from collective.gridlets import _
from collective.gridlets.widget import GridsterField


class IGridlets(form.Schema):
    """Add gridlets serialization field to content
    """

    form.omitted('gridlets')
    form.no_omit(IEditForm, 'gridlets')
    form.widget(gridlets=GridsterField)
    gridlets = schema.TextLine(
        title=_(u"Gridlets"),
        description=_(u"gridlets_description"),
        default=u'',
        required=False,
    )

alsoProvides(IGridlets, form.IFormFieldProvider)


class Gridlets(object):
    implements(IGridlets)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    @getproperty
    def gridlets(self):
        return self.context.gridlets
    @setproperty
    def gridlets(self, value):
        self.context.gridlets = value
