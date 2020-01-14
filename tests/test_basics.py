from flask import current_app
from tests.base_test_setup import BaseTestSetup


class BasicsTestCase(BaseTestSetup):
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
