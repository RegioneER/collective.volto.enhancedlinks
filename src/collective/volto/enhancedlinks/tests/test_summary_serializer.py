"""Setup tests for this package."""
from collective.volto.enhancedlinks.testing import RESTAPI_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.uuid.utils import uuidToCatalogBrain
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from plone.restapi.interfaces import ISerializeToJsonSummary
from transaction import commit
from zope.component import getMultiAdapter

import os
import unittest


class TestSerializer(unittest.TestCase):
    """Test that collective.volto.enhancedlinks is properly installed."""

    layer = RESTAPI_TESTING

    def get_attachment(self, filename, filetype):
        file_path = os.path.join(os.path.dirname(__file__), "files", filename)
        with open(file_path, "rb") as f:
            if filetype == "image":
                return NamedBlobImage(data=f.read(), filename=filename)
            return NamedBlobFile(data=f.read(), filename=filename)

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.pdf = api.content.create(
            type="File",
            title="file",
            container=self.portal,
            file=self.get_attachment(filename="file.pdf", filetype="file"),
        )
        self.image = api.content.create(
            type="Image",
            title="image",
            container=self.portal,
            image=self.get_attachment(filename="image.jpg", filetype="image"),
        )
        self.news = api.content.create(
            type="News Item",
            title="news",
            container=self.portal,
            image=self.get_attachment(filename="image.jpg", filetype="image"),
        )
        self.document = api.content.create(
            type="Document", title="A page", container=self.portal
        )

        commit()

    def test_summary_adapter_always_return_enhanced_metadata_for_brains(self):
        brain = uuidToCatalogBrain(self.pdf.UID())
        data = getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()
        self.assertIn("enhanced_links_enabled", data)
        self.assertIn("getObjSize", data)
        self.assertIn("mime_type", data)

        brain = uuidToCatalogBrain(self.document.UID())
        data = getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()
        self.assertIn("enhanced_links_enabled", data)
        self.assertIn("getObjSize", data)
        self.assertIn("mime_type", data)

    def test_summary_adapter_return_flag_if_enhanced_is_enabled_or_not(self):
        brain = uuidToCatalogBrain(self.pdf.UID())
        data = getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()
        self.assertTrue(data["enhanced_links_enabled"])

        brain = uuidToCatalogBrain(self.image.UID())
        data = getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()
        self.assertTrue(data["enhanced_links_enabled"])

        brain = uuidToCatalogBrain(self.news.UID())
        data = getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()
        self.assertFalse(data["enhanced_links_enabled"])

        brain = uuidToCatalogBrain(self.document.UID())
        data = getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()
        self.assertFalse(data["enhanced_links_enabled"])

    def test_summary_adapter_return_enhanced_data_for_objects(self):
        data = getMultiAdapter((self.pdf, self.request), ISerializeToJsonSummary)()
        self.assertIn("enhanced_links_enabled", data)
        self.assertIn("getObjSize", data)
        self.assertIn("mime_type", data)

    def test_summary_adapter_return_flag_if_enhanced_is_enabled_for_objects(
        self,
    ):
        data = getMultiAdapter((self.pdf, self.request), ISerializeToJsonSummary)()
        self.assertTrue(data["enhanced_links_enabled"])

        data = getMultiAdapter((self.image, self.request), ISerializeToJsonSummary)()
        self.assertTrue(data["enhanced_links_enabled"])

        data = getMultiAdapter((self.news, self.request), ISerializeToJsonSummary)()
        self.assertIsNone(data["enhanced_links_enabled"])

        data = getMultiAdapter((self.document, self.request), ISerializeToJsonSummary)()
        self.assertIsNone(data["enhanced_links_enabled"])

    def test_summary_adapter_return_obj_size_if_enhanced_is_enabled_for_objects(
        self,
    ):
        data = getMultiAdapter((self.pdf, self.request), ISerializeToJsonSummary)()
        brain = uuidToCatalogBrain(self.pdf.UID())
        self.assertEqual(data["getObjSize"], brain.getObjSize)

        data = getMultiAdapter((self.image, self.request), ISerializeToJsonSummary)()
        brain = uuidToCatalogBrain(self.image.UID())
        self.assertEqual(data["getObjSize"], brain.getObjSize)

        data = getMultiAdapter((self.news, self.request), ISerializeToJsonSummary)()
        self.assertIsNone(data["getObjSize"])

        data = getMultiAdapter((self.document, self.request), ISerializeToJsonSummary)()
        self.assertIsNone(data["getObjSize"])

    def test_summary_adapter_return_obj_mime_if_enhanced_is_enabled_for_objects(
        self,
    ):
        data = getMultiAdapter((self.pdf, self.request), ISerializeToJsonSummary)()
        brain = uuidToCatalogBrain(self.pdf.UID())
        self.assertEqual(data["mime_type"], brain.mime_type)

        data = getMultiAdapter((self.image, self.request), ISerializeToJsonSummary)()
        brain = uuidToCatalogBrain(self.image.UID())
        self.assertEqual(data["mime_type"], brain.mime_type)

        data = getMultiAdapter((self.news, self.request), ISerializeToJsonSummary)()
        self.assertIsNone(data["mime_type"])

        data = getMultiAdapter((self.document, self.request), ISerializeToJsonSummary)()
        self.assertIsNone(data["mime_type"])
