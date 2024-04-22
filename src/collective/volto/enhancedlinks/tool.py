from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from OFS.SimpleItem import SimpleItem
from persistent.mapping import PersistentMapping
from plone import api
from Products.CMFCore.utils import UniqueObject
from zope.interface import implementer
from zope.interface import Interface

import logging


logger = logging.getLogger(__name__)
_miss = object()


class IEnhancedLinksTool(Interface):
    """Marker interface enhancedlinks tool"""


@implementer(IEnhancedLinksTool)
class EnhancedLinksTool(UniqueObject, SimpleItem):
    id = "portal_enhancedlinks"
    meta_type = "Collective Enhanced Links Tool"
    security = ClassSecurityInfo()

    def __init__(self):
        self._enhanced_links = PersistentMapping()

    def get_enhanced_link(self, uid, force_reload=False):
        if not force_reload:
            info = self._enhanced_links.get(uid, _miss)
        else:
            info = _miss
        if info is _miss:
            brains = api.content.find(
                UID=uid, enhanced_links_enabled=True, unrestricted=True
            )
            if not brains:
                info = {}
            else:
                if len(brains) > 1:
                    logger.warning(f'Found multiple brains with the same UID: "${uid}"')
                brain = brains[0]
                if brain.getObjSize == "0 KB":
                    # not a link to file/image
                    info = {}
                else:
                    info = {
                        "getObjSize": brain.getObjSize,
                        "mime_type": brain.mime_type,
                    }
            self._enhanced_links[uid] = info
        return info


InitializeClass(EnhancedLinksTool)
