import json
import unittest
import main
import requests


class MockedNBP:
    def __init__(self, url, status_code, json_content):
        self.url = url
        self.status_code = status_code
        self.content = json_content


def createMock():
    rates = b'[{ "table": "A", "no": "140/A/NBP/2023", "effectiveDate": "2023-07-21", "rates":[{ "currency": "yuan renminbi (Chiny)", "code": "CNY","mid": 0.5567 }, { "currency": "SDR (MFW)","code": "XDR","mid": 5.3696} ] }]'
    #correct NBP_api format of returned data
    url = r'http://api.nbp.pl/api/exchangerates/tables/b?format=json'
    a =  MockedNBP(url, 200, rates)
    return a


class MyTestCase(unittest.TestCase):


    def test_getDataNBP_against_correct_json_type(self):
        #tutaj testuje zgodnosc typu jsona jakiego zwraca api, robie to z mockiem
        #ale w razie co mozna zrobic to z tym co zwraca api
        #return_data = main.getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/b?format=json')

        response_mock = createMock()
        api_response_json_mock = json.loads(response_mock.content)
        rates_json=json.loads(r'[{"one":"json"}]')

        expected=type(rates_json)
        result = type(api_response_json_mock)
        print(expected)
        print(result)
        #print(type(return_data))


        self.assertEqual( expected,result )


    def test_getDataNBP_against_correct_json_keys(self):
        #return_data = main.getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/b?format=json')
        # "http://api.nbp.pl/api/exchangerates/tables/a?format=json"
        # print(type(return_data))
        #

        response_mock = createMock()
        api_response_json_mock = json.loads(response_mock.content)
        expectedKeys = {'table', 'no', 'effectiveDate', 'rates'}
        json_keys= api_response_json_mock[0].keys()
        for i in expectedKeys:
            expected=True
            result= i in json_keys
            self.assertEqual( expected,result )

    def test_getDataNBP_has_list_ofRates(self):
        #return_data = main.getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/b?format=json')
        #mock has list of rates
        response_mock = createMock()
        api_response_json_mock = json.loads(response_mock.content)
        expected=type(json.loads(r'[{"one":"json"}]'))
        result=type(api_response_json_mock[0]['rates'])
        self.assertEqual( expected,result )


    def test_merge_two_json_against_correct_size(self):
        #tabel_A = main.getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/a?format=json')
        #tabel_B = main.getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/b?format=json')
        response_mock = createMock()
        api_response_json_mock1 = json.loads(response_mock.content)
        response_mock = createMock()
        api_response_json_mock2 = json.loads(response_mock.content)

        expected=4
        result=len(main.mergeTwoTablesRates(api_response_json_mock1, api_response_json_mock2))
        self.assertEqual(expected, result)

    def test_add_column_to_merged_efective_date_present(self):
        #tabel_A = main.getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/a?format=json')
        #tabel_B = main.getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/b?format=json')

        response_mock = createMock()
        api_response_json_mock1 = json.loads(response_mock.content)
        response_mock = createMock()
        api_response_json_mock2 = json.loads(response_mock.content)

        merged = main.mergeTwoTablesRates(api_response_json_mock1, api_response_json_mock2)
        effectiveDate = api_response_json_mock1[0]['effectiveDate']

        main.addColumnToMerged(merged, effectiveDate)
        expected = effectiveDate
        for i in merged:
            result = i['effectiveDate']
            self.assertEqual(expected, result )

    def test_normalize_data(self):
        response_mock = createMock()
        api_response_json_mock1 = json.loads(response_mock.content)
        response_mock = createMock()
        api_response_json_mock2 = json.loads(response_mock.content)

        merged = main.mergeTwoTablesRates(api_response_json_mock1, api_response_json_mock2)
        effectiveDate = api_response_json_mock1[0]['effectiveDate']

        main.addColumnToMerged(merged, effectiveDate)

        result= main.normalize_data(merged)
        expected1=type([])
        result1=type(result)
        self.assertEqual(expected1, result1)
        expected1=type([])
        result1=type(result[0])
        self.assertEqual(expected1, result1)

    #def test_save_to_csv(self):





if __name__ == '__main__':
    unittest.main()

# notes

'''
linki:
 "http://api.nbp.pl/api/exchangerates/tables/a?format=json"
 "http://api.nbp.pl/api/exchangerates/tables/b?format=json"
 print(type(json.loads(r'[{"one":"json"}]')))

'''
