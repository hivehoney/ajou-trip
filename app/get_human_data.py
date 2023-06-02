#공공데이터로부터 유동인구를 불러옵니다.
import pandas as pd
import requests
import json
from datetime import datetime as dt, timedelta

Citydata_filename = fr'Citydata_2023-05-20.csv'
All_City_df = pd.read_csv(Citydata_filename, usecols=['도시코드', '도시이름'])
City_list = dict(zip(All_City_df['도시코드'], All_City_df['도시이름']))
print(City_list)

def get_human_data(date):


    url = fr'https://apis.data.go.kr/B551011/DataLabService/locgoRegnVisitrDDList?' \
          fr'serviceKey=Pm03tXCB2ZJ%2BbD7FGDUmckrH2bJUO51xVBAEbNMTc1roEH2S91LuL%2BmMmEhmVvf5BxAqk2%2BLbrI3WUhtF1O%2BnA%3D%3D' \
          fr'&numOfRows=740&pageNo=1&MobileOS=ETC&MobileApp=HOLIDAYTRIP&_type=json&startYmd={date}&endYmd={date}'

    response = requests.get(url)
    data = json.loads(response.content)

    result = {}
    for item in data["response"]["body"]["items"]["item"]:
        signgu_Code = item["signguCode"]
        tou_div_nm = item["touDivNm"]
        tou_num = int(float(item["touNum"]))

        if signgu_Code not in result:
            result[signgu_Code] = 0

        if tou_div_nm == "외지인(b)" or tou_div_nm == "외국인(c)":
            result[signgu_Code] += tou_num

    new_result = {}
    for key, value in result.items():
        if int(key) in City_list:
            new_key = City_list[int(key)]
            new_result[new_key] = value
    new_result = {key: [value] for key, value in new_result.items()}
    human_df = pd.DataFrame(new_result)

    return human_df



for year in [2022]:
    start_date = dt(year, 1, 1)
    end_date = dt(year, 12, 31)
    current_date = start_date
    date_list = []

    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y%m%d"))
        current_date += timedelta(days=1)

    print(date_list)

    concat_human_df = get_human_data(date_list[0])
    for date in date_list[1:]:
        while True:
            try:
                print(date)
                tmp = get_human_data(date)
                concat_human_df = pd.concat([concat_human_df,tmp],ignore_index=True)
                break
            except Exception as e:
                print(f"예외사항 발생 :  {str(e)}")
                print(f"API를 재호출합니다.")
                continue

    concat_human_df.to_csv(fr'{year}_human_data.csv', index=False)