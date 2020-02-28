from app.common import example_generator as ex


def test_generate_tld_url_list(self):
    random_list = ex.generate_tld_url_list(10, None)
    self.assertEqual(random_list[9]["url"][:11], "http://www.")


def test_create_url_list(self):
    random_collection = ex.generate_frontier(3, 10, "de")
    self.assertEqual(random_collection[0][9]["url"][-3:], ".de")
