import requests
from bs4 import BeautifulSoup
import unittest


class Test(unittest.TestCase):
    bs = None

    def setUpClass():
        url = 'https://crypto.com/price'
        req = requests.get(url).text
        Test.bs = BeautifulSoup(req, 'lxml')

    def test_titleText(self):
        page_title = Test.bs.find('title').get_text()
        self.assertEqual('Crypto.com', page_title.split(' ')[-1])

    def test_contentExists(self):
        content = Test.bs.find(class_='css-1cxc880')
        self.assertIsNotNone(content)

    def test_nameExists(self):
        name = Test.bs.find(class_='chakra-text css-rkws3').get_text()
        self.assertEqual('Bitcoin', name)

    def test_shortnameExists(self):
        short_name = Test.bs.find(class_='chakra-text css-1jj7b1a').get_text()
        self.assertEqual('BTC', short_name)

    def test_priceExists(self):
        price = Test.bs.find(class_='css-b1ilzc').get_text()
        self.assertIn('$', price)


if __name__ == '__main__':
    unittest.main()