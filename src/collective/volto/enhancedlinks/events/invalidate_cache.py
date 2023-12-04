# -*- coding: utf-8 -*-
from plone.app.linkintegrity.utils import getIncomingLinks
from plone.memoize.instance import _m as memojito


def invalidate(obj, event):
    """
    Invalidate cache for items that has a link to this.
    In this way we will refresh enhanched links infos.
    """
    direct_links = getIncomingLinks(obj, from_attribute="isReferencing")
    for link in direct_links:
        related_obj = link.from_object
        if related_obj:
            memojito.clear(related_obj)
