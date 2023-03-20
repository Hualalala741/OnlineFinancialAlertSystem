"""
_*_ coding : utf-8 -*_ 
@author：86136
@date：2023年02月06日
@File : test
@Project : 爬虫
"""
import requests
import json


def main():
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=&charset="

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    main()