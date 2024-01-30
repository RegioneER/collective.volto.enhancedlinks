from plone import api
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.app.contentlisting.realobject import RealContentListingObject
from plone.indexer.interfaces import IIndexableObject
from plone.restapi.interfaces import IJSONSummarySerializerMetadata
from zope.component import queryMultiAdapter
from zope.interface import implementer


@implementer(IJSONSummarySerializerMetadata)
class JSONSummarySerializerMetadata:
    def default_metadata_fields(self):
        return {"enhanced_links_enabled", "getObjSize", "mime_type"}


@implementer(IContentListingObject)
class EnhancedLinksContentListingObject(RealContentListingObject):
    """
    Provide some extra infos
    """

    @property
    def enhanced_links_enabled(self):
        return True

    @property
    def getObjSize(self):
        return self.getSize()

    @property
    def mime_type(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        adapter = queryMultiAdapter((self.getObject(), catalog), IIndexableObject)
        return adapter.mime_type
