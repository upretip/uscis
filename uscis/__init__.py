
# -*- utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import time

class USCIS:
    URL = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
    headers = {"Host": "egov.uscis.gov",
    "Connection": "keep-alive",
     "Content-Length": '255',
     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
     "Content-Type": "application/x-www-form-urlencoded",
     "Accept": "application/json, text/javascript, */*; q=0.01",
     "X-Requested-With":"XMLHttpRequest",
     "DNT": "1",
     "Referer": "https://egov.uscis.gov/casestatus/landing.do",
     "Accept-Encoding": "gzip, deflate, br",
     "Accept-Language": "en-US, en; q=0.8;q=0.6"}

    def __init__(self):
        pass

    def retrieve(self, receipt_number):
        receipt_number = str(receipt_number)
        r = requests.post(self.URL, data={'appReceiptNum':receipt_number}).text
        soup = BeautifulSoup(r,"html.parser")
        result = soup.find('div', class_='rows text-center')
        highlight = result.find("h1").text
        detail = result.find("p").text
        # print(highlight, '\n',detail)
        return time.ctime(), receipt_number, highlight, detail,

def receipt_creator():
    for serial_number in range(1000):
        if serial_number% 10 ==0:
            time.sleep(0.1)
        if serial_number % 100 == 0:
            print("completed {} of {}".format(serial_number, 10000))
        yield "MSC18915{:05d}".format(serial_number)

if __name__ == "__main__":
    # print(USCIS().retrieve("MSC1895300001")) #to check function
    with open("uscis_status.csv", "a") as writefile:
        writer = csv.writer(writefile, delimiter=',', lineterminator ='\n')
        writer.writerow(['downloaded','receipt', 'heading', 'detail'])
        for n in receipt_creator():
            writer.writerow(USCIS().retrieve(receipt_number=n))

