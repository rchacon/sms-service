import os
import unittest

from scraper import extractsms, extractphone

TEST_DIR = os.path.dirname(__file__)


class ScraperTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_extractsms(self):
        with open(os.path.join(TEST_DIR, 'fixtures/source.html')) as f:
            html = f.read()

        result = extractsms(html)

        obj = {
            u'conversation_id': u'12e5a6b7197fe086ceb516e1c3d3130593b77ed6',
            u'phone': u'(510) 555-5555',
            u'time': u'6:59 PM',
            u'from': u'Me:',
            u'text': u'where u at'
        }
        self.assertEqual(result[0], obj)

    def test_extractphone(self):
        result = extractphone(u'Google will call your phone and connect you to(510) 315-1225.')

        self.assertEqual(result, '(510) 315-1225')


if __name__ == '__main__':
    unittest.main()
