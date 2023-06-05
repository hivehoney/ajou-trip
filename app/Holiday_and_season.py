from fastapi import FastAPI
import pandas as pd
import requests
import json
import os
from datetime import datetime as dt
from app.api import API
from api import API

api = API()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

result = api.get_festival()
"""
    fstvlNm: 축제명
    addr: 소재지주소
    rdnmadr: 소재지도로명주소
    lnmadr: 소재지지번주소
    fstvlStartDate: 축제시작일자
    fstvlEndDate: 축제종료일자
    fstvlDate: 축제일
"""
class travel_place:
    def Festival_Schedule(self):
        # Festivaldata_filename = fr'2023_festival_schedule.csv'
        # Festival_Schedule_df = pd.read_csv(Festivaldata_filename, encoding='utf-8').sort_values('축제시작일자')
        Festival_Schedule_df = pd.DataFrame(api.get_festival())

        #addr(소재지주소) 컬럼으로 병합
        Festival_Schedule_df['addr'] = Festival_Schedule_df['rdnmadr'].str.split().str[:2].str.join(' ')
        Festival_Schedule_df.loc[Festival_Schedule_df['addr'].isnull(), 'addr'] = Festival_Schedule_df['lnmadr'].str.split().str[:2].str.join(' ')

        del Festival_Schedule_df['rdnmadr']
        del Festival_Schedule_df['lnmadr']

        #데이터 format
        Festival_Schedule_df['addr'] = Festival_Schedule_df['addr'].fillna('')
        Festival_Schedule_df['fstvlStartDate'] = pd.to_datetime(Festival_Schedule_df['fstvlStartDate'])
        Festival_Schedule_df['fstvlEndDate'] = pd.to_datetime(Festival_Schedule_df['fstvlEndDate'])
        #######################################

        #시작일~종료일 날짜 생성
        festival_dates = pd.concat([pd.DataFrame({'fstvlNm': row['fstvlNm'], 'fstvlDate': pd.date_range(row['fstvlStartDate'], row['fstvlEndDate'])
                                                     ,'addr': row['addr']}) for i, row in Festival_Schedule_df.iterrows()])

        #인기여행지인 곳만 생성 
        festival_dates = festival_dates[festival_dates['addr'].isin(Travel_Place_df.values())]
        
        #데이터 포맷
        festival_dates['fstvlDate'] = pd.to_datetime(festival_dates['fstvlDate']).dt.strftime('%Y-%m-%d')
        festival_dates_grouped_1 = festival_dates.groupby(['fstvlNm', 'addr']).agg({'fstvlDate': list})
        festival_dates_grouped_2 = festival_dates.groupby(['addr']).agg(fstvlDate=('fstvlDate', lambda x: list(x)))

        return festival_dates_grouped_1, festival_dates_grouped_2

    def classify_season(date):
        month = date.month

        if month in [3, 4, 5]:
            return "Spring"  # Spring
        elif month in [6, 7, 8]:
            return "Summer"  # Summer
        elif month in [9, 10, 11]:
            return "Autumn"  # Autumn
        else:
            return "Winter"  # Winter

# 인기 도시별 축제일정 불러오기-------------------------start
# Citydata_filename = fr'Citydata_2023-05-20.csv'
# Travel_Place_df = pd.read_csv(Citydata_filename, encoding='utf-8')
# station = dict(zip(Travel_Place_df['districtCode'], Travel_Place_df['districtName']))

travel = travel_place()
year = [2023]
#인기여행지
global Travel_Place_df, holidays

Travel_Place_df = api.get_travel_place()
holidays = api.get_kr_HOLI_holidays(2023)

#인기여행지 축제정보
festival_dates_grouped_1, festival_dates_grouped_2 = travel.Festival_Schedule()

print(festival_dates_grouped_1)
print(festival_dates_grouped_2)

#휴일체크
def classify_holiday(holidays, date):
    if date.weekday() in [5, 6] or date.strftime("%Y%m%d") in holidays.values():
        return "holiday"
    else:
        return "non-holiday"

"""
holYN: 휴일여부
date: 날짜
fstvlCnt: 축제 갯수
"""
for year in year:
    for key, value in Travel_Place_df.items():
        print(f'{value}')

        Human_data = fr'{year}_human_data.csv'

        #휴일데이터생성
        date_list = pd.date_range(f'{year}-01-01', f'{year}-12-31')
        holiday_df = pd.DataFrame({"date": date_list})
        holiday_df["holYN"] = holiday_df["date"].apply(lambda date: classify_holiday(holidays, date))
        holiday_df['date'] = holiday_df['date'].dt.strftime('%Y-%m-%d')

        Festival_place = list(festival_dates_grouped_2.index)
        print(Festival_place)

        if year == dt.now().year:
            holiday_df['fstvlCnt'] = holiday_df['date'].apply(lambda x: sum(str(x.split()[0]) in festival_dates for festival_dates in festival_dates_grouped_2.loc[value, 'fstvlDate']) if value in Festival_place else 0)
            result_df = holiday_df
            print(result_df)
        else:
            Human_df = pd.read_csv(Human_data, encoding='utf-8')[value]
            Human_df = Human_df.rename('유동인구수')
            result_df = pd.concat([holiday_df, Human_df], axis=1)

        result_df.fillna(0, inplace=True)
        result_df['계절'] = result_df['date'].apply(lambda x: travel_place.classify_season(pd.to_datetime(x)))
        print(result_df.to_string())
        folder_path = f'{year}_holidayandseason_data'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        result_df.to_csv(os.path.join(folder_path, f'{year}_result_data({value}).csv'), encoding='utf-8-sig', index=False)

    print("dd")