# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from mons.dataimport.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of mons.dataimport into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if mons.dataimport is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('mons.dataimport'))

    def test_uninstall(self):
        """Test if mons.dataimport is cleanly uninstalled."""
        self.installer.uninstallProducts(['mons.dataimport'])
        self.assertFalse(self.installer.isProductInstalled('mons.dataimport'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IMonsDataimportLayer is registered."""
        from mons.dataimport.interfaces import IMonsDataimportLayer
        from plone.browserlayer import utils
        self.failUnless(IMonsDataimportLayer in utils.registered_layers())
