# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.volto.enhancedlinks.testing import (  # noqa: E501
    COLLECTIVE_VOLTO_ENHANCEDLINKS_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSerializer(unittest.TestCase):
    """Test that collective.volto.enhancedlinks is properly installed."""

    layer = COLLECTIVE_VOLTO_ENHANCEDLINKS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_foo(self):
        self.assertTrue(True)
