from fastapi import FastAPI
import pandas as pd
import requests
import json
from datetime import datetime as dtime

#도시별 날씨 조회코드 불러오기
Citydata_filename = fr'Citydata_2023-05-20.csv'
Travel_Place_df = pd.read_csv(Citydata_filename, encoding='euc-kr')
station = dict(zip(Travel_Place_df['도시이름'], Travel_Place_df['날씨조회코드']))

#도시별 축제일정 불러오기
Festivaldata_filename = fr'2023_festival_schedule.csv'
Festival_Schedule_df = pd.read_csv(Festivaldata_filename, encoding='utf-8').sort_values('축제시작일자')
Festival_Schedule_df['소재지주소'] = Festival_Schedule_df['소재지도로명주소'].str.split().str[:2].str.join(' ')
Festival_Schedule_df.loc[Festival_Schedule_df['소재지주소'].isnull(), '소재지주소'] = Festival_Schedule_df['소재지지번주소'].str.split().str[:2].str.join(' ')
Festival_Schedule_df['소재지주소'] = Festival_Schedule_df['소재지주소'].fillna('')
Festival_Schedule_df['축제시작일자'] = pd.to_datetime(Festival_Schedule_df['축제시작일자'])
Festival_Schedule_df['축제종료일자'] = pd.to_datetime(Festival_Schedule_df['축제종료일자'])
Festival_Schedule_df['축제일'] = Festival_Schedule_df.apply(lambda row: pd.date_range(row['축제시작일자'], row['축제종료일자'], closed='left'),axis=1)
Festival_Schedule_df = Festival_Schedule_df.explode('축제일').reset_index(drop=True)
Festival_Schedule_df['축제일'] = Festival_Schedule_df['축제일'].astype(str)
Festival_Schedule_df_result = Festival_Schedule_df[['축제명', '소재지주소','축제시작일자','축제종료일자', '축제일']].dropna(subset=['축제일'])
city_names = Travel_Place_df['도시이름'].tolist()

filtered_result = Festival_Schedule_df_result[Festival_Schedule_df_result['소재지주소'].str.contains('|'.join(city_names))]

for station_name, station_param in station.items():
    def Weather_API():
        Weather_result_df = pd.DataFrame()
        last_successful_year = 0
        last_successful_month = 0

        # 2021년~현재날짜 까지 조회

        for year in range(2023, 2024):
            for month in range(1, 5):
                # 만약 connection refused로 인한 API 조회 실패시 현재시점에서 재시도
                while True:
                    try:
                        go_url = fr'http://apis.data.go.kr/1360000/SfcMtlyInfoService/getDailyWthrData?serviceKey=Pm03tXCB2ZJ%2BbD7FGDUmckrH2bJUO51xVBAEbNMTc1roEH2S91LuL%2BmMmEhmVvf5BxAqk2%2BLbrI3WUhtF1O%2BnA%3D%3D&numOfRows=10&dataType=JSON&pageNo=1&year={year}&month={str(month).zfill(2)}&station={station_param}'
                        response = requests.get(go_url)

                        Weather_data = json.loads(response.content)
                        Weather_items = Weather_data['response']['body']['items']['item'][0]['stndays']['stn_ko']
                        Weather_info = Weather_data['response']['body']['items']['item'][0]['stndays']['info']
                        Weather_info_Filter = []

                        # garbage 데이터 걸러내기(날짜만)
                        for item in Weather_info:
                            if item['tm'] not in ['상순', '중순', '하순', 'null']:
                                Weather_info_Filter.append(item)

                        # 데이터 결과값(날짜,최저기온,최고기온,풍량)
                        Weather_result = pd.DataFrame({
                            'ta_min': [item['ta_min'] for item in Weather_info_Filter],
                            'ta_max': [item['ta_max'] for item in Weather_info_Filter],
                        })

                        Weather_result_df = pd.concat([Weather_result_df, Weather_result],ignore_index = True)
                        last_successful_year = year
                        last_successful_month = month

                        break

                    except Exception as e:
                        if str(e) in fr"'body'":
                            break
                        else:
                            print(f"예외사항 발생 :  {str(e)}")
                            print(f"API를 재호출합니다. 연도 : {last_successful_year}, 월 : {last_successful_month}")
                            continue

            else:
                continue

            break

        return Weather_result_df

    year = 2023#dtime.now().year
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


    def classify_holiday(date):
        if date.weekday() in [5, 6]:
            return "holiday"
        else:
            holidays = get_kr_HOLI_holidays(date.year)
            for value in holidays.values():
                if date.strftime("%Y%m%d") in [str(v) for v in value]:
                    return "holiday"
            return "non-holiday"

    start_date = dtime(year, 1, 1).date()
    end_date = dtime(year, 12, 31).date()

    Weather_df = Weather_API()
    date_list = pd.date_range(start_date, end_date)

    holiday_df = pd.DataFrame({"ds": date_list}).astype('object')
    holiday_df["holiday"] = holiday_df["ds"].apply(classify_holiday)
    print(holiday_df)
    print(Weather_df)
    result1 = pd.concat([holiday_df,Weather_df], axis = 1, ignore_index = True)
    result1.columns = ["날짜","휴일여부","최저온도","최고온도"]
    print(result1.to_string())
