from fastapi import FastAPI
import pandas as pd
import requests
import json
from datetime import datetime as dtime

app = FastAPI()
params ={'serviceKey' : '서비스키', 'pageNo' : '1', 'numOfRows' : '10', 'dataType' : 'JSON', 'stnId' : '108', 'tmFc' : '201310170600' }

# async def request(client):
#     response = await client.get(URL, headers=headers)
#     return response.text
#
#
# async def task():
#     async with httpx.AsyncClient() as client:
#         tasks = [request(client) for i in range(100)]
#         result = await asyncio.gather(*tasks)s
#         print(result)

headers = {
    "accept": "application/json",
    "appkey": "l7xx846db5f3bc1e48d29b7275a745d501c8"
}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hellos {name}"}

#인기여행지 123개 조사
def get_travelplace():
    sk_url = "https://apis.openapi.sk.com/puzzle/travel?type=sig"
    response = requests.get(sk_url, headers=headers)
    get_TravelPlace = response.json()['contents']
    get_TravelPlace_dict = {Dict['districtCode']: Dict['districtName'] for Dict in get_TravelPlace}
    return get_TravelPlace_dict

Travel_Place = get_travelplace()

#get_travelplace에서 얻어온 여행지를 바탕으로 123개 여행지의 월별 방문자 수 조회
@app.get("/test")
def get_people(Place):
    districtCode = list(Place)
    for i in range(0, 2):  # len(districtCode)):
        for year in range(2022, 2023):  # dtime.now().year):
            for month in range(1, 3):
                print(districtCode[i])
                sk_url = fr"https://apis.openapi.sk.com/puzzle/traveler-count/raw/monthly/districts/{districtCode[i]}?yearMonth={year}{str(month).zfill(2)}&gender=all&ageGrp=all&companionType=all"
                response = requests.get(sk_url, headers=headers)
                get_TravelerCountOfDate = response.json().get('contents')
                #get_TravelerCountOfDate_dict = {int(item['raw']['yearMonth']): int(item['raw']['travelerCount']) for itema in get_TravelerCountOfDate}
                print(get_TravelerCountOfDate)

get_people(Travel_Place)

#날씨 정보 수집 API
@app.get("/test1")
def Weather_API():
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

Weather_API()
