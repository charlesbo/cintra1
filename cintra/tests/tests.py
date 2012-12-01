import unittest

from pyramid import testing

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from cintra.views.views import cintra_view
        context = dict(instruments={}, quotesoftheday=['']*3)
        request = testing.DummyRequest()
        info = cintra_view(context, request)
        self.assertEqual(info['project'], 'cintra')
