import unittest
from app.common import example_generator as ex


class MyTestCase(unittest.TestCase):

    def test_get_random_chars(self):
        random3 = ex.get_random_chars(3)
        random10 = ex.get_random_chars(10)
        self.assertEqual(len(random3), 3)
        self.assertEqual(len(random10), 10)


    def test_generate_tld_url_list(self):
        random_list = ex.generate_tld_url_list(10, 'all')
        self.assertEqual(random_list[9]['url'][:11], 'http://www.')


if __name__ == '__main__':
    unittest.main()
