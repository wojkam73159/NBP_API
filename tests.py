import json
import unittest
import main


# import requests


class MockedNBP:
    def __init__(self, url, status_code, json_content):
        self.url = url
        self.status_code = status_code
        self.content = json_content

    def get(self, url):
        return self

    def json(self):
        return [{"table": "A", "no": "140/A/NBP/2023", "effectiveDate": "2023-07-21",
                 "rates": [{"currency": "yuan renminbi (Chiny)", "code": "CNY", "mid": 0.5567},
                           {"currency": "SDR (MFW)", "code": "XDR", "mid": 5.3696}]}]

    def raise_for_status(self):
        pass


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # self.table_A = main.getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/a?format=json')
        # self.table_B = main.getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/b?format=json')
        rates = b'[{ "table": "A", "no": "140/A/NBP/2023", "effectiveDate": "2023-07-21", "rates":[{ "currency": "yuan renminbi (Chiny)", "code": "CNY","mid": 0.5567 }, { "currency": "SDR (MFW)","code": "XDR","mid": 5.3696} ] }]'
        # correct NBP_api format of returned data
        url = r'http://api.nbp.pl/api/exchangerates/tables/b?format=json'
        self.original_request = main.requests
        response_mock = MockedNBP(url, 200, rates)  # test double
        main.requests = response_mock  # monkey patching po nim tear down

    def tearDown(self) -> None:
        main.requests = self.original_request  # powrot do orginalnego requesta z maina

    def test_get_data_nbp_against_correct_json_type(self):
        expected = [{"table": "A", "no": "140/A/NBP/2023", "effectiveDate": "2023-07-21",
                     "rates": [{"currency": "yuan renminbi (Chiny)", "code": "CNY", "mid": 0.5567},
                               {"currency": "SDR (MFW)", "code": "XDR", "mid": 5.3696}]}]
        result = main.get_data_nbp("")
        self.assertListEqual(result, expected)

    def test_get_data_nbp_against_correct_json_keys(self):
        expected_keys = {'table', 'no', 'effectiveDate', 'rates'}
        json_keys = main.get_data_nbp("")[0].keys()
        for i in expected_keys:
            self.assertIn(i, json_keys)

    def test_get_data_nbp_has_list_of_rates(self):
        nbp_mock_response = main.get_data_nbp()
        expected = list
        result = nbp_mock_response[0]['rates']
        self.assertIsInstance(result, expected)

    def test_merge_two_json_against_correct_size(self):
        nbp_mock_response1 = main.get_data_nbp()
        nbp_mock_response2 = main.get_data_nbp()
        expected = 4
        result = len(main.merge_two_tables_rates(nbp_mock_response1, nbp_mock_response2))
        self.assertEqual(expected, result)

    def test_add_column_to_merged_effective_date_present(self):
        api_response_mock1 = main.get_data_nbp()
        api_response_mock2 = main.get_data_nbp()
        merged = main.merge_two_tables_rates(api_response_mock1, api_response_mock2)
        effective_date = api_response_mock1[0]['effectiveDate']

        main.add_column_to_merged(merged, effective_date)
        expected = effective_date
        for i in merged:
            result = i['effectiveDate']
            self.assertEqual(expected, result)

    def test_normalize_data(self):
        api_response_mock1 = main.get_data_nbp()
        api_response_mock2 = main.get_data_nbp()
        merged = main.merge_two_tables_rates(api_response_mock1, api_response_mock2)
        effective_date = api_response_mock1[0]['effectiveDate']

        main.add_column_to_merged(merged, effective_date)

        result = main.normalize_data(merged)
        result = result
        self.assertIsInstance(result, list)
        result = result[0]
        self.assertIsInstance(result, list)

    # def test_save_to_csv(self):


if __name__ == '__main__':
    unittest.main()

# notes

'''
linki:
 "http://api.nbp.pl/api/exchangerates/tables/a?format=json"
 "http://api.nbp.pl/api/exchangerates/tables/b?format=json"

'''
