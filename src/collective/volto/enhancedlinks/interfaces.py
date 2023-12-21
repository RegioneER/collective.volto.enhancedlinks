"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveVoltoEnhancedlinksLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEnhancedLinksEnabled(Interface):
    """
    Marker interface for behavior
    """
