import json
import requests
# import unittest
# import pandas as pd
import csv
from typing import Union


# http://api.nbp.pl/api/exchangerates/tables/b?format=json
def get_data_nbp(url: str = "http://api.nbp.pl/api/exchangerates/tables/a?format=json") -> Union[list, dict]:
    received_data = requests.get(url)
    received_data.raise_for_status()
    json_data = received_data.json()
    return json_data


def merge_two_tables_rates(tabel_a, tabel_b):
    rates_a = tabel_a[0]['rates']
    rates_b = tabel_b[0]['rates']

    rates_a = list(rates_a)
    rates_b = list(rates_b)

    merged = rates_a + rates_b
    return merged


def add_column_to_merged(merged, effective_date):
    for i in merged:
        i["effectiveDate"] = effective_date

    return merged


def normalize_data(merged):
    my_tab2 = list(merged[0].keys())
    my_tab = [my_tab2]
    for elem in merged:
        temp_tab1 = list(elem.values())
        # for j in elem.keys():
        #    temp_tab1.append(elem[j])
        my_tab.append(temp_tab1)
    print("debug")
    return my_tab


def save_to_csv(list_of_lists, file_name):
    with open(file_name, 'w', encoding="utf-8") as f:
        write = csv.writer(f)
        write.writerows(list_of_lists)


def whole_run():
    table_a = get_data_nbp(r'http://api.nbp.pl/api/exchangerates/tables/a?format=json')
    table_b = get_data_nbp(r'http://api.nbp.pl/api/exchangerates/tables/b?format=json')

    merged = merge_two_tables_rates(table_a, table_b)

    effective_date = table_a[0]['effectiveDate']
    add_column_to_merged(merged, effective_date)
    merged = normalize_data(merged)
    save_to_csv(merged, effective_date + ".csv")

    # df = pd.json_normalize(merged)
    # df.to_csv("{}.csv".format(effectiveDate), index=False)


if __name__ == '__main__':
    whole_run()

# structure of received json:
'''//only keys:
[
'table':
'no':
effectiveDate:
rates:list[]
]
'''
