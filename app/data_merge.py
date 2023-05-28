from fastapi import FastAPI
import pandas as pd
import requests
import json
from datetime import datetime as dt


#인기 도시별 축제일정 불러오기-------------------------start
Citydata_filename = fr'Citydata_2023-05-20.csv'
Travel_Place_df = pd.read_csv(Citydata_filename, encoding='utf-8')
station = dict(zip(Travel_Place_df['도시이름'], Travel_Place_df['날씨조회코드']))

def Festival_Schedule():
    Festivaldata_filename = fr'2023_festival_schedule.csv'
    Festival_Schedule_df = pd.read_csv(Festivaldata_filename, encoding='utf-8').sort_values('축제시작일자')
    Festival_Schedule_df['소재지주소'] = Festival_Schedule_df['소재지도로명주소'].str.split().str[:2].str.join(' ')
    Festival_Schedule_df.loc[Festival_Schedule_df['소재지주소'].isnull(), '소재지주소'] = Festival_Schedule_df['소재지지번주소'].str.split().str[:2].str.join(' ')
    del Festival_Schedule_df['소재지도로명주소']
    del Festival_Schedule_df['소재지지번주소']
    Festival_Schedule_df['소재지주소'] = Festival_Schedule_df['소재지주소'].fillna('')
    Festival_Schedule_df['축제시작일자'] = pd.to_datetime(Festival_Schedule_df['축제시작일자'])
    Festival_Schedule_df['축제종료일자'] = pd.to_datetime(Festival_Schedule_df['축제종료일자'])


    def generate_festival_dates(row):
        start_date = pd.to_datetime(row['축제시작일자'])
        end_date = pd.to_datetime(row['축제종료일자'])
        dates = pd.date_range(start_date, end_date)
        festival_name = row['축제명']
        location = row['소재지주소']
        festival_dates = pd.DataFrame({'축제명': festival_name, '축제일': dates, '소재지주소': location})
        return festival_dates

    festival_dates = Festival_Schedule_df.apply(generate_festival_dates, axis=1)
    Festival_Schedule_df = pd.concat(festival_dates.tolist(), ignore_index=True)
    Festival_Schedule_df = Festival_Schedule_df[Festival_Schedule_df['소재지주소'].isin(station.keys())]
    Festival_Schedule_df['축제일'] = pd.to_datetime(Festival_Schedule_df['축제일'])
    Festival_Schedule_df['축제일'] = Festival_Schedule_df['축제일'].dt.strftime('%Y-%m-%d')
    Festival_Schedule_df_Grouped_1 = Festival_Schedule_df.groupby(['축제명','소재지주소']).agg({'축제일':list})
    Festival_Schedule_df_Grouped_2 = Festival_Schedule_df.groupby(['소재지주소']).agg(축제일=('축제일', lambda x: list(x)))
    return Festival_Schedule_df_Grouped_1, Festival_Schedule_df_Grouped_2

#도시별 축제일정 불러오기-------------------------end
Festival_Schedule, Festival_Schedule_2 = Festival_Schedule()
#print(Festival_Schedule)
#print(Festival_Schedule_2.to_string())

def classify_season(date):
    month = date.month

    if month in [3, 4, 5]:
        return "봄"  # Spring
    elif month in [6, 7, 8]:
        return "여름"  # Summer
    elif month in [9, 10, 11]:
        return "가을"  # Autumn
    else:
        return "겨울"  # Winter


for year in [2020,2021,2022]:
    for key,value in station.items():
        print(f'{key}')
        #dtime.now().year
        Human_data = fr'{year}_human_data.csv'
        def get_kr_HOLI_holidays(year):
            url = f'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getHoliDeInfo?' \
                  f'solYear={year}&_type=json&numOfRows=100&' \
                  f'ServiceKey=Pm03tXCB2ZJ%2BbD7FGDUmckrH2bJUO51xVBAEbNMTc1roEH2S91LuL%2BmMmEhmVvf5BxAqk2%2BLbrI3WUhtF1O%2BnA%3D%3D'

            response = requests.get(url)
            data = response.json()

            holidays = {}

            if "response" in data and "body" in data["response"]:
                items = data["response"]["body"]["items"]["item"]

                for item in items:
                    holiday_date = item["locdate"]
                    holiday_name = item["dateName"]

                    if holiday_name not in holidays:
                        holidays[holiday_name] = []

                    holidays[holiday_name].append(holiday_date)

            return holidays
        holidays = get_kr_HOLI_holidays(year)

        def classify_holiday(date):
            if date.weekday() in [5, 6]:
                return "holiday"
            else:
                for value in holidays.values():
                    if date.strftime("%Y%m%d") in [str(v) for v in value]:
                        return "holiday"
                return "non-holiday"

        start_date = dt(year, 1, 1).date()
        end_date = dt(year, 12, 31).date()
        date_list = pd.date_range(start_date, end_date)
        holiday_df = pd.DataFrame({"ds": date_list}).astype('object')
        holiday_df["holiday"] = holiday_df["ds"].apply(classify_holiday)
        holiday_df["ds"] = pd.to_datetime(holiday_df["ds"])
        holiday_df['ds'] = holiday_df['ds'].dt.strftime('%Y-%m-%d')
        holiday_df.columns = ["날짜","휴일여부"]

        if year == dt.now().year:
            holiday_df['축제갯수'] = 0
            for index, row in holiday_df.iterrows():
                date = str(row['날짜']).split()[0]  # 날짜 형식을 'YYYY-MM-DD'로 변경
                festival_count = 0
                if key in Festival_Schedule_2.index:
                    for festival_dates in Festival_Schedule_2.loc[key, '축제일']:
                        if date in festival_dates:
                            festival_count += 1
                    else:
                        continue
                holiday_df.at[index, '축제갯수'] = festival_count
            result_df = holiday_df
        else:
            Human_df = pd.read_csv(Human_data, encoding='utf-8')[key]
            Human_df = Human_df.rename('유동인구수')
            result_df = pd.concat([holiday_df,Human_df],axis=1)

        result_df['계절'] = result_df['날짜'].apply(lambda x: classify_season(pd.to_datetime(x)))
        result_df.to_csv(fr'{year}_result_data({key}).csv', index=False)
