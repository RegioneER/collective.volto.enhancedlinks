from collective.volto.enhancedlinks.interfaces import IEnhancedLinksEnabled
from plone.indexer.decorator import indexer


@indexer(IEnhancedLinksEnabled)
def enhanced_links_enabled(context, **kw):
    return True
