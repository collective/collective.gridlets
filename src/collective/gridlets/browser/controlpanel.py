from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from collective.gridlets.interfaces import IGridletSettings
from plone.z3cform import layout


class ControlpanelForm(RegistryEditForm):
    schema = IGridletSettings


ControlPanelView = layout.wrap_form(
    ControlpanelForm,
    ControlPanelFormWrapper
)
