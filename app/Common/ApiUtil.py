import pandas as pd
import requests
import json
from datetime import datetime as dtime


class API:

    # 축제정보 API
    def get_festival(self):
        url = 'http://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api'
        service_key = 'd4oz2HqVBL5Q9fG2IkdqGaMsqtxZCdrOh9y6IDk0ya7qmGH8DrTxPnR3hI4UfwHIRy5IxZKFzxGRUw10ZUef4A=='
        params = {'serviceKey': service_key, 'pageNo': '1', 'numOfRows': '100', 'type': 'json'}

        response = requests.get(url, params=params)
        return response.json().get('response').get('body').get('items')

    # 인기여행지API(123곳)
    def get_travel_place(self):
        max_length = 5
        sk_url = "https://apis.openapi.sk.com/puzzle/travel?type=sig"
        headers = {
            "accept": "application/json",
            "appkey": "l7xx846db5f3bc1e48d29b7275a745d501c8"
        }

        response = requests.get(sk_url, headers=headers)
        travel_place = response.json()['contents']
        travel_place = {Dict['districtCode']: Dict['districtName'] for Dict in travel_place}
        # travel_place['districtCode'] = travel_place['districtCode'].str.slice(stop=max_length)
        return {key[:max_length]: value for key, value in travel_place.items()}

    # 휴일정보 API
    def get_kr_HOLI_holidays(self, year):
        url = f'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getHoliDeInfo?' \
              f'solYear={year}&_type=json&numOfRows=100&' \
              f'ServiceKey=p7igRYPscMbJM%2BGd70el0sQ6MywPGRCBMQoB%2FVOhTj%2FWhBux%2FFXg2vUtRX9y0FTWwwjCfwZgMktA12I937NfYQ%3D%3D'

        response = requests.get(url)
        data = response.json().get('response').get('body').get('items').get('item')
        holidays = {}

        for item in data:
            date_name = item.get('dateName')
            loc_date = item.get('locdate')
            holidays.setdefault(date_name, []).append(loc_date)

        return holidays

    # 광역지자체 지역방문자수 집계 API
    def get_local_visitor(self, st, ed):
        try:
            url = fr'http://apis.data.go.kr/B551011/DataLabService/locgoRegnVisitrDDList?' \
                  fr'serviceKey=p7igRYPscMbJM%2BGd70el0sQ6MywPGRCBMQoB%2FVOhTj%2FWhBux%2FFXg2vUtRX9y0FTWwwjCfwZgMktA12I937NfYQ%3D%3D' \
                  fr'&numOfRows=25000&pageNo=1&MobileOS=ETC&MobileApp=HOLIDAYTRIP&_type=json&startYmd={st}&endYmd={ed}'
                  # fr'&MobileOS=ETC&MobileApp=HOLIDAYTRIP&_type=json&startYmd={date}&endYmd={date}'

            response = requests.get(url)
            data = response.json().get('response').get('body').get('items').get('item')
        except Exception as e:
            print(f"예외사항 발생 :  {str(e)}")

        return data
