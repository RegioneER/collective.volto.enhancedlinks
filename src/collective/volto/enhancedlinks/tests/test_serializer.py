"""Setup tests for this package."""
from collective.volto.enhancedlinks.testing import RESTAPI_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from plone.restapi.interfaces import ISerializeToJson
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
        self.csv = api.content.create(
            type="File",
            title="csv file",
            container=self.portal,
            file=self.get_attachment(filename="file_csv.csv", filetype="file"),
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

    def create_document_with_link(self, uid):
        document = api.content.create(
            type="Document",
            title="foo",
            container=self.portal,
            blocks={
                "157998cf-440e-49a0-9dd1-f4dd5a75200b": {
                    "@type": "slate",
                    "value": [
                        {
                            "type": "p",
                            "children": [
                                {"text": ""},
                                {
                                    "type": "link",
                                    "data": {
                                        "url": f"../resolveuid/{uid}",
                                        "dataElement": "",
                                    },
                                    "children": [{"text": "this is the link"}],
                                },
                                {"text": ""},
                            ],
                        }
                    ],
                    "plaintext": " This is the link ",
                },
            },
            blocks_layout={"items": ["157998cf-440e-49a0-9dd1-f4dd5a75200b"]},
        )
        commit()
        return document

    def test_serializer_with_file_pdf(self):
        doc = self.create_document_with_link(uid=self.pdf.UID())
        doc_brain = api.content.find(UID=self.pdf.UID())[0]

        serializer = getMultiAdapter((doc, self.request), ISerializeToJson)
        block = list(serializer()["blocks"].values())[0]
        block_data = block["value"][0]["children"][1]["data"]

        self.assertIn("enhanced_link_infos", block_data)
        self.assertEqual(
            block_data["enhanced_link_infos"]["mime_type"], "application/pdf"
        )
        self.assertEqual(
            block_data["enhanced_link_infos"]["getObjSize"], doc_brain.getObjSize
        )

    def test_serializer_with_file_csv(self):
        doc = self.create_document_with_link(uid=self.csv.UID())
        doc_brain = api.content.find(UID=self.csv.UID())[0]

        serializer = getMultiAdapter((doc, self.request), ISerializeToJson)
        block = list(serializer()["blocks"].values())[0]
        block_data = block["value"][0]["children"][1]["data"]

        self.assertIn("enhanced_link_infos", block_data)
        self.assertEqual(
            block_data["enhanced_link_infos"]["mime_type"],
            "text/comma-separated-values",
        )
        self.assertEqual(
            block_data["enhanced_link_infos"]["getObjSize"], doc_brain.getObjSize
        )

    def test_serializer_with_image(self):
        doc = self.create_document_with_link(uid=self.image.UID())
        doc_brain = api.content.find(UID=self.image.UID())[0]

        serializer = getMultiAdapter((doc, self.request), ISerializeToJson)
        block = list(serializer()["blocks"].values())[0]
        block_data = block["value"][0]["children"][1]["data"]

        self.assertIn("enhanced_link_infos", block_data)
        self.assertEqual(
            block_data["enhanced_link_infos"]["mime_type"],
            "image/jpeg",
        )
        self.assertEqual(
            block_data["enhanced_link_infos"]["getObjSize"], doc_brain.getObjSize
        )

    def test_serializer_does_not_work_without_behavior_enabled(self):
        doc = self.create_document_with_link(uid=self.news.UID())

        serializer = getMultiAdapter((doc, self.request), ISerializeToJson)
        block = list(serializer()["blocks"].values())[0]
        block_data = block["value"][0]["children"][1]["data"]

        self.assertNotIn("enhanced_link_infos", block_data)
