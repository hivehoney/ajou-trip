from fastapi import FastAPI
import pandas as pd
import requests
import json
from datetime import datetime as dtime

class API:
    app = FastAPI()

    # 축제정보 API
    def get_festival(self):
        url = 'http://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api'
        service_key = 'd4oz2HqVBL5Q9fG2IkdqGaMsqtxZCdrOh9y6IDk0ya7qmGH8DrTxPnR3hI4UfwHIRy5IxZKFzxGRUw10ZUef4A=='
        params ={'serviceKey' : service_key, 'pageNo' : '1', 'numOfRows' : '100', 'type' : 'json'}

        response = requests.get(url, params=params)
        return response.json().get('response').get('body').get('items')


    # 인기여행지API(123곳)
    def get_travel_place(self):
        sk_url = "https://apis.openapi.sk.com/puzzle/travel?type=sig"
        headers = {
            "accept": "application/json",
            "appkey": "l7xx846db5f3bc1e48d29b7275a745d501c8"
        }

        response = requests.get(sk_url, headers=headers)
        travel_place = response.json()['contents']
        return {Dict['districtCode']: Dict['districtName'] for Dict in travel_place}

    #휴일정보 API
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

    @app.get("/hello/{name}")
    async def say_hello(name: str):
        return {"message": f"Hellos {name}"}


    #날씨 정보 수집 API
    @app.get("/test1")
    def Weather_API(self):
        last_successful_year = 0
        last_successful_month = 0

        #2021년~현재날짜 까지 조회
        for year in range(2021, dtime.now().year):
            for month in range(1, 13):
                #만약 connection refused로 인한 API 조회 실패시 현재시점에서 재시도
                while True:
                    try:
                        print(year, month)
                        go_url = fr'http://apis.data.go.kr/1360000/SfcMtlyInfoService/getDailyWthrData?serviceKey=Pm03tXCB2ZJ%2BbD7FGDUmckrH2bJUO51xVBAEbNMTc1roEH2S91LuL%2BmMmEhmVvf5BxAqk2%2BLbrI3WUhtF1O%2BnA%3D%3D&numOfRows=10&dataType=JSON&pageNo=1&year={year}&month={str(month).zfill(2)}&station=90'
                        response = requests.get(go_url)

                        Weather_data = json.loads(response.content)
                        Weather_items = Weather_data['response']['body']['items']['item'][0]['stndays']['stn_ko']
                        Weather_info = Weather_data['response']['body']['items']['item'][0]['stndays']['info']
                        Weather_info_Filter = []

                        #garbage 데이터 걸러내기(날짜만)
                        for item in Weather_info:
                            if item['tm'] not in ['상순', '중순', '하순', 'null']:
                                Weather_info_Filter.append(item)

                        #데이터 결과값(날짜,최저기온,최고기온,풍량)
                        Weather_result = pd.DataFrame({
                            'tm': [item['tm'] for item in Weather_info_Filter],
                            'ta_min': [item['ta_min'] for item in Weather_info_Filter],
                            'ta_max': [item['ta_max'] for item in Weather_info_Filter],
                            'ws' : [item['ta_max'] for item in Weather_info_Filter]
                        })
                        Weather_items_df = pd.DataFrame([Weather_items])
                        Weather_result_df = pd.DataFrame(Weather_result)
                        print(Weather_result_df.to_string())

                        last_successful_year = year
                        last_successful_month = month

                        break
                    except Exception as e:
                        print(f"예외사항 발생 :  {str(e)}")
                        print(f"API를 재호출합니다. 연도 : {last_successful_year}, 월 : {last_successful_month}")
                        continue

            else:
                continue
            break
        return 0
