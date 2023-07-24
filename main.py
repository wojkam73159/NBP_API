
import json
import requests
import unittest
import pandas as pd
import csv


#http://api.nbp.pl/api/exchangerates/tables/b?format=json
def getDataNBP(url="http://api.nbp.pl/api/exchangerates/tables/a?format=json")->json:
    receivedData=requests.get(url)
    if receivedData.status_code==200:
        jsonData=json.loads(receivedData.content)
        return jsonData
    else:
        raise Exception("error while connecting to api, status code:{}".format(receivedData.status_code))



def mergeTwoTablesRates(tabel_A, tabel_B):
    rates_A=tabel_A[0]['rates']
    rates_B=tabel_B[0]['rates']

    rates_A=list(rates_A)
    rates_B=list(rates_B)

    merged=rates_A+rates_B
    return merged


def addColumnToMerged(merged, effectiveDate):

    for i in merged:
        i["effectiveDate"]=effectiveDate

    return merged

def normalize_data(merged):
    myTab=list(merged[0].keys())
    myTab=[myTab]
    tempTab1=[]
    for i in merged:
        for j in i.keys():
            tempTab1.append(i[j])
        myTab.append(tempTab1)
        tempTab1=[]
    print("debug")
    return myTab

def saveToCSV(listOfLists, fileName):
    with open(fileName, 'w',encoding= "utf-8") as f:

        write = csv.writer(f)


        write.writerows(listOfLists)

def wholeRun():
    tabel_A = getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/a?format=json')
    tabel_B = getDataNBP(r'http://api.nbp.pl/api/exchangerates/tables/b?format=json')


    merged=mergeTwoTablesRates(tabel_A, tabel_B)

    effectiveDate=tabel_A[0]['effectiveDate']
    addColumnToMerged(merged,effectiveDate)
    merged=normalize_data(merged)
    saveToCSV(merged,effectiveDate+".csv")

    #df = pd.json_normalize(merged)
    #df.to_csv("{}.csv".format(effectiveDate), index=False)



if __name__ == '__main__':

    wholeRun()



#structure of received json:
'''//only keys:
[
'table':
'no':
effectiveDate:
rates:list[]
]
'''




