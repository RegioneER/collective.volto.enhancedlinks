from plone import api


def invalidate(obj, event):
    """
    Invalidate cache for items that has a link to this.
    In this way we will refresh enhanched links infos.
    """
    tool = api.portal.get_tool("portal_enhancedlinks")
    tool.get_enhanced_link(obj.UID(), force_reload=True)
