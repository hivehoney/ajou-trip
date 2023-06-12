import csv

import geolocator as geolocator
import pandas as pd
from fastapi import requests
from urllib3 import response
from geopy.geocoders import Nominatim

def write_festival(data, file_path):
    # CSV 파일에 데이터 적재
    # with open(file_path, 'w', newline='') as csv_file:
    #     writer = csv.writer(csv_file)
    #
    #     # 데이터 헤더 작성
    #     header = ['festivalName', 'location', 'latitude', 'longitude', 'etc']
    #     writer.writerow(header)
    #
    #     # 데이터 행 작성
    #     for festival in data:
    #         row = [
    #             festival['festivalName'],
    #             festival['location'],
    #             festival['latitude'],
    #             festival['longitude'],
    #             festival['etc']
    #         ]
    #         writer.writerow(row)

    # CSV 파일에 데이터 저장 (기존 파일에 추가)
    df.to_csv('data.csv', mode='a', header=False, index=False, columns=['festivalName', 'location', 'latitude', 'longitude', 'etc'])


def get_geolocation(address):
    geolocator = Nominatim(user_agent='my_geocoder')
    location = geolocator.geocode(address)

    if location is not None:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        print('위치 정보를 가져오지 못했습니다.')
        return None, None

# 주소를 위도와 경도로 변환
address = '경기도 양평군 양동면 쌍학리 223-2'
latitude, longitude = get_geolocation(address)

print(f'주소: {address}')
print(f'위도: {latitude}')
print(f'경도: {longitude}')




def get_festival(self, pageNo):
    url = 'http://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api'
    service_key = 'd4oz2HqVBL5Q9fG2IkdqGaMsqtxZCdrOh9y6IDk0ya7qmGH8DrTxPnR3hI4UfwHIRy5IxZKFzxGRUw10ZUef4A=='
    params = {'serviceKey': service_key, 'pageNo': pageNo, 'numOfRows': '100000', 'type': 'json'}

    # JSON 데이터를 DataFrame으로 변환
    data = response.json()

    return data


# 데이터 리스트
data = [
    {
        'lnmadr': 'Location 1',
        'rdnmadr': 'Location 1',
        'fstvlNm': 'Festival 1',
        'fstvlStartDate': '20230916',
        'fstvlEndDate': '20230916',
        'longitude': 127.98765,
        'latitude': 37.12345,
        'etc': 'Etc 1'
    },
    {
        'lnmadr': 'Location 1',
        'rdnmadr': 'Location 1',
        'fstvlNm': 'Festival 1',
        'fstvlStartDate': '20230916',
        'fstvlEndDate': '20230916',
        'longitude': 127.98765,
        'latitude': 37.12345,
        'etc': 'Etc 2'
    },
]


# 데이터프레임 생성
df = pd.DataFrame(data)

# 주소를 기반으로 위도와 경도 검색
location_data = df['location'].apply(geolocator.geocode)  # 주소를 기반으로 위도와 경도 검색

# 위도와 경도 열 추가
df['latitude'] = location_data.apply(lambda loc: loc.latitude if loc else None)
df['longitude'] = location_data.apply(lambda loc: loc.longitude if loc else None)
두

"""
fstvlNm: 축제
fstvlStartDate: 시작일
fstvlEndDate: 종료일
rdnmadr: 도로명
lnmadr: 지번
etc: 설명
latitude: 위도
longitude: 경도
"""
# CSV 기존 파일에 추가
df.to_csv('festival.csv', mode='a', header=False, index=False, columns=['fstvlNm', 'fstvlStartDate', 'fstvlEndDate', 'rdnmadr', 'lnmadr', 'etc', 'latitude', 'longitude'])

