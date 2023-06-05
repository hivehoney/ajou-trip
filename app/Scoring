import Season_Tour_Human
import os
import pandas as pd
import requests
import json
import datetime as dt

#코드 결과를 보고자 하시면 다음을 맨 아래에 추가하여 실행하세요

#RECOMMEND_DATA("부산광역시",2,3)

#부산광역시 소속의 3개 소도시의 2박 3일 여행지일정을 추천하고, 딕셔너리형태로 변환하여 리턴합니다.


def RECOMMEND_DATA(CITY_PARM,DATE_N,DATE_M):
    print(f"{CITY_PARM}에서 {DATE_N}박 {DATE_M}일을 여행하실 거군요!")
    print(f"{CITY_PARM}에서 {DATE_N}박 {DATE_M}일을 여행하기 위한 최적의 일정과 여행지를 제공하겠습니다.")
    print(f"저희가 제공하는 데이터는 아래의 분석 사항을 따릅니다.\n"
          f"1. SK Telecom에서 분석한 인기 관광지역 123개 도시를 선정하여 보여드립니다.\n"
          f"2. Holiday Trip이라는 이름에 걸맞게 휴일 위주의 일정을 먼저 제공합니다.\n"
          f"3. 여행은 역시 축제죠? 지역 축제 일정을 고려하여 축제명/기간/장소 정보를 제공합니다.\n"
          f"4. 최근 3년간 여행인구가 많고, 적었던 계절을 선정하여 보여드리니 여행하실 때 고려해보시면 되겠습니다.\n")

    #축제 일정 데이터 호출
    Citydata_filename = fr'Citydata_2023-05-20.csv'
    All_City_df = pd.read_csv(Citydata_filename, usecols=['도시이름'])
    City_list = All_City_df['도시이름'].tolist()
    Score_list = []

    #스코어링 수행 for문
    #축제가 있는지 여부, 축제가 있는 날에 휴일이 얼마나 들어잇는지 여부 등 점검
    for city in [x for x in City_list if CITY_PARM in x]:
        csv_file_2023 = fr"2023_holidayandseason_data\2023_result_data({city}).csv"
        df = pd.read_csv(csv_file_2023,encoding='utf-8')
        # '축제갯수'가 1 이상인 행만 추출
        df_holiday_with_festivals = df[df['축제갯수'] >= 1]
        df_holiday_with_festivals_sorted = df_holiday_with_festivals.sort_values(by='계절')
        df_holidays = df.loc[df['휴일여부'] == 'holiday']
        #print(df_holiday_with_festivals_sorted.to_string())
        #스코어링
        Holiday_Score = len(df_holiday_with_festivals_sorted) * 10
        Festival_Score = df_holiday_with_festivals_sorted['축제갯수'].sum() * 5
        Score = {city: Holiday_Score+Festival_Score}
        Score_list.append(Score)

    #순위 추출
    Score_list_sorted_top3 = sorted(Score_list, key=lambda x: list(x.values())[0], reverse=True)[:3]
    Score_list_sorted_top3 = [list(item.keys())[0] for item in Score_list_sorted_top3]


    #각 도시 유동인구 추출
    Season_Tour_Human_DATA_LIST = Season_Tour_Human.HUMANDATA(CITY_PARM)
    Season_Tour_Human_DATA_LIST = [{name: item[name]} for name in Score_list_sorted_top3 for item in Season_Tour_Human_DATA_LIST if name in item]
    Season_Tour_Human_DATA_LIST_TOP = []
    for item in Season_Tour_Human_DATA_LIST:
        for name in Score_list_sorted_top3:
            if name in item:
                sorted_item = dict(sorted(item[name].items(), key=lambda x: x[1], reverse=True))
                Season_Tour_Human_DATA_LIST_TOP.append({name: sorted_item})
                print(Season_Tour_Human_DATA_LIST_TOP)

    TOP1_City = TOP2_City = TOP3_City = 0

    #스코어링 기법으로 형성된 도시별 랭킹에 대한 변수형성
    #TOP1_City : 스코어점수가 가장 높은 도시 ~ TOP3 : 스코어점수가 3등인 도시
    if len(Score_list_sorted_top3) > 0:
        TOP1_City = Score_list_sorted_top3[0]
    if len(Score_list_sorted_top3) > 1:
        TOP2_City = Score_list_sorted_top3[1]
    if len(Score_list_sorted_top3) > 2:
        TOP3_City = Score_list_sorted_top3[2]

    #요일과 요일이름 넣기
    #요일 : 각요일마다 dayofweek에 인식될 번호(월요일 : 0 ~ 일요일 : 6)
    #요일이름 : 월요일, 화요일 같은 요일이름
    def insert_week(df_season_sort):
        days = {0: '월요일', 1: '화요일', 2: '수요일', 3: '목요일', 4: '금요일', 5: '토요일', 6: '일요일'}
        df_season_sort = df_season_sort.copy()
        df_season_sort['요일'] = df_season_sort['날짜'].dt.dayofweek
        df_season_sort['요일이름'] = df_season_sort['요일'].apply(lambda x: days[x])
        return df_season_sort

    #당일치기 전용 여행지 추출(평일을 제외하거나 주말에 인접한날만 추천하도록 수행)
    def get_TOP123_Schedule_01(df_season_sort):
        df_season_sort['요일순위'] = df_season_sort['요일이름'].map({'토요일': 1, '일요일': 2, '금요일': 3, '월요일': 4}).fillna(5)
        grouped = df_season_sort.groupby('계절')
        df_season_sort = grouped.apply(lambda g: g.nlargest(1, ['축제갯수', '요일순위', '날짜']))  # nlargest : 정렬 후 추출하는 함수
        df_season_sort = df_season_sort.reset_index(drop=True)
        df_season_sort = df_season_sort.groupby('계절').first().reset_index()
        return df_season_sort

    # 날짜 형식 변경 함수
    def format_date(date):
        formatted_date = date.strftime('%Y-%m-%d')
        return formatted_date

    # 봄, 여름, 가을, 겨울 각 계절에 대해 추천하기 / 최종리턴값 반환을 위한 데이터 형성
    def recommend_trip_1(df_season_sort, day):
        seasons = ['봄', '여름', '가을', '겨울']

        for season in seasons:
            df_season_filtered = df_season_sort[df_season_sort['계절'] == season]
            max_festival_count = 0
            recommended_trip = None

            for index, row in df_season_filtered.iterrows():
                if row['축제갯수'] > max_festival_count:
                    max_festival_count = row['축제갯수']
                    recommended_trip = row

            if recommended_trip is not None:
                departure_date = format_date(pd.to_datetime(recommended_trip['날짜']))
                return_date = format_date(pd.to_datetime(recommended_trip['날짜']) + pd.DateOffset(days=day))

                RECOMENDED_SCHEDULE = {city: #도시
                                           {"season": season, #봄/여름/가을/겨울
                                            "Start_date": departure_date, ##2023-06-11
                                            "End_date": return_date, #2023-06-14
                                            "Start_week": recommended_trip['요일'],  # 0 = 월, 1 = 화 ----- 금 = 4, 토 = 5, 일 = 6
                                            "End_week": (recommended_trip['요일']+day) % 7, # 0 = 월, 1 = 화 ----- 금 = 4, 토 = 5, 일 = 6
                                            "Festival": recommended_trip['축제갯수']}}
            else:
                continue

            return RECOMENDED_SCHEDULE

    #후보가 적은이유로 도시가 3개 미만일 때 Garbage 데이터를 리스트에 할당하지 않도록 수행
    if TOP2_City == 0 and TOP3_City == 0:
        TOP_City_List = [TOP1_City]
    elif TOP3_City == 0:
        TOP_City_List = [TOP1_City, TOP2_City]
    else:
        TOP_City_List = [TOP1_City, TOP2_City, TOP3_City]

    RECOMMEND_SCHEDULE_DATA_LIST = []
    #봄/여름/가을/겨울 및 N박 M일 일정에 맞는 여행일정 제공
    for city in TOP_City_List:
        csv_file_2023 = fr"2023_holidayandseason_data\2023_result_data({city}).csv"
        df = pd.read_csv(csv_file_2023, encoding='utf-8')
        df['날짜'] = pd.to_datetime(df['날짜'])
        for season in ['봄','여름','가을','겨울']:
            df_season = df.loc[(df['계절'] == season) & (df['축제갯수'] >= 1)]

            if DATE_N == 0 and DATE_M == 1:
                #토(5), 일(6)
                df_season_sort = df_season[(df_season['휴일여부'] == 'holiday') &
                                 (df_season['축제갯수'] == df_season['축제갯수'].max())]
                df_season_sort = insert_week(df_season_sort)
                df_season_sort = get_TOP123_Schedule_01(df_season_sort)
                RECOMMEND_SCHEDULE_DATA = recommend_trip_1(df_season_sort,0)
                RECOMMEND_SCHEDULE_DATA_LIST.append(RECOMMEND_SCHEDULE_DATA)

            elif DATE_N == 1 and DATE_M == 2:
                df_season_sort = df_season[(df_season['축제갯수'] == df_season['축제갯수'].max())]
                df_season_sort = insert_week(df_season_sort)
                RECOMMEND_SCHEDULE_DATA = recommend_trip_1(df_season_sort, 1)
                RECOMMEND_SCHEDULE_DATA_LIST.append(RECOMMEND_SCHEDULE_DATA)

            elif DATE_N == 2 and DATE_M == 3:
                df_season_sort = df_season[(df_season['축제갯수'] == df_season['축제갯수'].max())]
                df_season_sort = insert_week(df_season_sort)
                RECOMMEND_SCHEDULE_DATA = recommend_trip_1(df_season_sort, 2)
                RECOMMEND_SCHEDULE_DATA_LIST.append(RECOMMEND_SCHEDULE_DATA)

            elif DATE_N == 3 and DATE_M == 4:
                df_season_sort = df_season[(df_season['축제갯수'] == df_season['축제갯수'].max())]
                df_season_sort = insert_week(df_season_sort)
                RECOMMEND_SCHEDULE_DATA = recommend_trip_1(df_season_sort, 3)
                RECOMMEND_SCHEDULE_DATA_LIST.append(RECOMMEND_SCHEDULE_DATA)

    RECOMMEND_SCHEDULE_DATA_LIST = [item for item in RECOMMEND_SCHEDULE_DATA_LIST if item is not None]
    print(RECOMMEND_SCHEDULE_DATA_LIST)
    return RECOMMEND_SCHEDULE_DATA_LIST

