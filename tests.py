import json
import unittest
import main


# import requests


class MockedNBP:
    def __init__(self, url, status_code, json_content):
        self.url = url
        self.status_code = status_code
        self.content = json_content


def create_mock():
    rates = b'[{ "table": "A", "no": "140/A/NBP/2023", "effectiveDate": "2023-07-21", "rates":[{ "currency": "yuan renminbi (Chiny)", "code": "CNY","mid": 0.5567 }, { "currency": "SDR (MFW)","code": "XDR","mid": 5.3696} ] }]'
    # correct NBP_api format of returned data
    url = r'http://api.nbp.pl/api/exchangerates/tables/b?format=json'
    a = MockedNBP(url, 200, rates)
    return a


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # self.tabel_A = main.getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/a?format=json')
        # self.tabel_B = main.getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/b?format=json')
        response_mock = create_mock()
        self.api_response_json_mock1 = json.loads(response_mock.content)
        response_mock = create_mock()
        self.api_response_json_mock2 = json.loads(response_mock.content)

    def test_getDataNBP_against_correct_json_type(self):
        # tutaj testuje zgodnosc typu jsona jakiego zwraca api, robie to z mockiem
        # ale w razie co mozna zrobic to z tym co zwraca api
        # return_data = main.getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/b?format=json')

        rates_json = json.loads(r'[{"one":"json"}]')

        expected_type = type(rates_json)
        result = self.api_response_json_mock1
        self.assertIsInstance(result, expected_type)
        # print(expected)
        # print(result)
        # print(type(return_data))

    def test_getDataNBP_against_correct_json_keys(self):
        # "http://api.nbp.pl/api/exchangerates/tables/a?format=json"

        expected_keys = {'table', 'no', 'effectiveDate', 'rates'}
        json_keys = self.api_response_json_mock1[0].keys()
        for i in expected_keys:
            self.assertIn(i, json_keys)

    def test_getDataNBP_has_list_ofRates(self):

        expected = json.loads(r'[{"one":"json"}]')
        result = self.api_response_json_mock1[0]['rates']
        self.assertIsInstance(result, type(expected))

    def test_merge_two_json_against_correct_size(self):
        expected = 4
        result = len(main.merge_two_tables_rates(self.api_response_json_mock1, self.api_response_json_mock2))
        self.assertEqual(expected, result)

    def test_add_column_to_merged_effective_date_present(self):

        merged = main.merge_two_tables_rates(self.api_response_json_mock1, self.api_response_json_mock2)
        effective_date = self.api_response_json_mock1[0]['effectiveDate']

        main.add_column_to_merged(merged, effective_date)
        expected = effective_date
        for i in merged:
            result = i['effectiveDate']
            self.assertEqual(expected, result)

    def test_normalize_data(self):
        merged = main.merge_two_tables_rates(self.api_response_json_mock1, self.api_response_json_mock2)
        effective_date = self.api_response_json_mock1[0]['effectiveDate']

        main.add_column_to_merged(merged, effective_date)

        result = main.normalize_data(merged)
        expected_type1 = type([])
        result = result
        self.assertIsInstance(result, expected_type1)
        expected_type2 = type([])
        result = result[0]
        self.assertIsInstance(result, expected_type2)

    # def test_save_to_csv(self):


if __name__ == '__main__':
    unittest.main()

# notes

'''
linki:
 "http://api.nbp.pl/api/exchangerates/tables/a?format=json"
 "http://api.nbp.pl/api/exchangerates/tables/b?format=json"
 print(type(json.loads(r'[{"one":"json"}]')))

'''
