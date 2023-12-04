from plone.restapi.behaviors import IBlocks
from plone.restapi.interfaces import IBlockFieldDeserializationTransformer
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from plone.restapi.deserializer.blocks import SlateBlockTransformer

import os


@implementer(IBlockFieldDeserializationTransformer)
@adapter(IBlocks, IBrowserRequest)
class EnhancedLinksDeserializer(SlateBlockTransformer):
    order = 1000
    block_type = "slate"
    disabled = os.environ.get("disable_blocks_enhanched_links", False)

    def handle_link(self, child):
        """
        Cleanup data that we don't want to store in db
        """
        if "enhanced_link_infos" in child:
            del child["enhanced_link_infos"]
