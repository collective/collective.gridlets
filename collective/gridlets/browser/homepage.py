from Products.Five.browser import BrowserView
from zope.component import queryMultiAdapter
from zope.contentprovider import interfaces


class Homepage(BrowserView):
    """ Default view of the homepage content type """

    def render_gridlets(self):
        provider = queryMultiAdapter(
            (self.context, self.request, self),
            interfaces.IContentProvider, 'collective.gridlets.portletManager')

        provider.update()

        return provider.render()

    def renderProviderByName(self, provider_name):
        provider = queryMultiAdapter(
            (self.portlet_container, self.request, self),
            interfaces.IContentProvider, provider_name)

        provider.update()

        return provider.render()
