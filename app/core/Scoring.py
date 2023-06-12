import os
import pandas as pd
import requests
import json
import datetime as dt

from app.common.api import API

api = API()

#코드 결과를 보고자 하시면 다음을 맨 아래에 추가하여 실행하세요
global Travel_Place_df
Travel_Place_df = api.get_travel_place()
visitor = visitor()
travel_place = travel_place()
Score_list = []


def RECOMMEND_DATA(visit, st, ed):

    City_list = [value for value in Travel_Place_df.values() if value.startswith(visit)]
    #축제 일정 데이터 호출
    #스코어링 수행 for문
    #축제가 있는지 여부, 축제가 있는 날에 휴일이 얼마나 들어있는지 여부 등 점검
    seasons = ['Sprint', 'Summer', 'Autumn', 'Winter']
    year = 2023
    df = travel_place.fstvlHolYear(visit, year)

    for city in City_list:
        # '축제갯수'가 1 이상인 행만 추출
        df_holiday_with_festivals = df[df['fstvlCnt'] >= 1]
        df_holiday_with_festivals_sorted = df_holiday_with_festivals.sort_values(by='season')
        df_holidays = df.loc[df['hlYN'] == 'holiday']
        #스코어링
        Holiday_Score = len(df_holiday_with_festivals_sorted) * 10
        Festival_Score = df_holiday_with_festivals_sorted['fstvlCnt'].sum() * 5
        Score = {city: Holiday_Score+Festival_Score}
        Score_list.append(Score)
        print(Score_list)

    #순위 추출
    Score_list_sorted_top3 = sorted(Score_list, key=lambda x: list(x.values())[0], reverse=True)[:3]
    Score_list_sorted_top3 = [list(item.keys())[0] for item in Score_list_sorted_top3]


    #각 도시 유동인구 추출
    Season_Tour_Human_DATA_LIST = visitor.local_visitor(visit, st, ed)
    Season_Tour_Human_DATA_LIST = [{name: item[name]} for name in Score_list_sorted_top3 for item in Season_Tour_Human_DATA_LIST if name in item]
    Season_Tour_Human_DATA_LIST_TOP = []
    for item in Season_Tour_Human_DATA_LIST:
        for name in Score_list_sorted_top3:
            if name in item:
                sorted_item = dict(sorted(item[name].items(), key=lambda x: x[1], reverse=True))
                Season_Tour_Human_DATA_LIST_TOP.append({name: sorted_item})

    TOP1_City, TOP2_City, TOP3_City = 0

    #스코어링 기법으로 형성된 도시별 랭킹에 대한 변수형성
    #TOP1_City : 스코어점수가 가장 높은 도시 ~ TOP3 : 스코어점수가 3등인 도시
    if len(Score_list_sorted_top3) > 0:
        TOP1_City = Score_list_sorted_top3[0]
    if len(Score_list_sorted_top3) > 1:
        TOP2_City = Score_list_sorted_top3[1]
    if len(Score_list_sorted_top3) > 2:
        TOP3_City = Score_list_sorted_top3[2]




    #후보가 적은이유로 도시가 3개 미만일 때 Garbage 데이터를 리스트에 할당하지 않도록 수행
    if TOP2_City == 0 and TOP3_City == 0:
        TOP_City_List = [TOP1_City]
    elif TOP3_City == 0:
        TOP_City_List = [TOP1_City, TOP2_City]
    else:
        TOP_City_List = [TOP1_City, TOP2_City, TOP3_City]
    print(TOP_City_List)
    RECOMMEND_SCHEDULE_DATA_LIST = []


    RECOMMEND_SCHEDULE_DATA_LIST = [item for item in RECOMMEND_SCHEDULE_DATA_LIST if item is not None]
    print(RECOMMEND_SCHEDULE_DATA_LIST)
    return RECOMMEND_SCHEDULE_DATA_LIST

