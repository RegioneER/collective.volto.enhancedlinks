from contextlib import contextmanager
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.protect.utils import safeWrite
from plone.restapi.deserializer.blocks import SlateBlockTransformer
from plone.restapi.interfaces import IBlockFieldSerializationTransformer
from plone.restapi.serializer.utils import RESOLVEUID_RE
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest

import itertools
import logging
import os


logger = logging.getLogger(__name__)


# https://github.com/collective/Products.AutoUserMakerPASPlugin/blob/master/Products/AutoUserMakerPASPlugin/auth.py
@contextmanager
def safe_write(request):
    """Disable CSRF protection of plone.protect for a block of code.
    Inside the context manager objects can be written to without any
    restriction. The context manager collects all touched objects
    and marks them as safe write."""
    # We used 'set' here before, but that could lead to:
    # TypeError: unhashable type: 'PersistentMapping'
    objects_before = _registered_objects(request)
    yield
    objects_after = _registered_objects(request)
    for obj in objects_after:
        if obj not in objects_before:
            safeWrite(obj, request)


def _registered_objects(request):
    """Collect all objects part of a pending write transaction."""
    app = request.PARENTS[-1]
    return list(
        itertools.chain.from_iterable(
            [
                conn._registered_objects
                # skip the 'temporary' connection since it stores session objects
                # which get written all the time
                for name, conn in app._p_jar.connections.items()
                if name != "temporary"
            ]
        )
    )


@implementer(IBlockFieldSerializationTransformer)
@adapter(IDexterityContent, IBrowserRequest)
class EnhancedLinksSerializer(SlateBlockTransformer):
    order = -1
    block_type = "slate"
    disabled = os.environ.get("disable_blocks_enhanched_links", False)

    def get_uid_from_path(self, path):
        """
        Extract uid from path when there is resolveuid
        """
        if not path:
            return ""
        match = RESOLVEUID_RE.match(path)
        if match is None:
            return ""
        uid, suffix = match.groups()
        return uid

    def handle_link(self, child):
        """
        Retrieve content_info from a linked File/Image object
        """
        uid = self.get_uid_from_path(path=child["data"].get("url", ""))
        if not uid:
            return
        tool = api.portal.get_tool("portal_enhancedlinks")
        with safe_write(self.request):
            enhanched_infos = tool.get_enhanced_link(uid)
        if enhanched_infos:
            child["data"]["enhanced_link_infos"] = enhanched_infos
