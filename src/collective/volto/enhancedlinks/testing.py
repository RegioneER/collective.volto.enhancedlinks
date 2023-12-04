# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.volto.enhancedlinks


class CollectiveVoltoEnhancedlinksLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.volto.enhancedlinks)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.volto.enhancedlinks:default")


COLLECTIVE_VOLTO_ENHANCEDLINKS_FIXTURE = CollectiveVoltoEnhancedlinksLayer()


COLLECTIVE_VOLTO_ENHANCEDLINKS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_VOLTO_ENHANCEDLINKS_FIXTURE,),
    name="CollectiveVoltoEnhancedlinksLayer:IntegrationTesting",
)


COLLECTIVE_VOLTO_ENHANCEDLINKS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_VOLTO_ENHANCEDLINKS_FIXTURE,),
    name="CollectiveVoltoEnhancedlinksLayer:FunctionalTesting",
)
