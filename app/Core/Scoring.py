import datetime
import datetime as dt
import numpy as np
import pandas as pd
from Common.ApiUtil import API
from Common.Util import utilChk
from Core.Holiday_and_season import travel_place


api = API()
travel_place = travel_place()
util = utilChk()

#코드 결과를 보고자 하시면 다음을 맨 아래에 추가하여 실행하세요
# Score_list = []

def RECOMMEND_DATA(city, st, ed, visit, range):

    # 일자별 유동인구
    visit_dates = visit.groupby('baseYmd')['touNum'].sum().reset_index()

    # 지역별 유동인구
    rcmnd_local = visit.groupby(['signguCode', 'signguNm'])['touNum'].sum().reset_index()

    # 휴일데이터
    holidays = api.get_kr_HOLI_holidays(st[:4])

    if st[:4] != ed[:4]:
        holidays += api.get_kr_HOLI_holidays(ed[:4])
    else:
        visit_dates['baseYmd'] = st[:4] + visit_dates['baseYmd']

    # 데이터프레임에 holiday 열 추가
    visit_dates['holiday'] = np.nan

    holidayList = [value for sublist in holidays.values() for value in sublist]

    # 휴일 여부 판단 및 값 설정
    for index, row in visit_dates.iterrows():
        baseYmd_str = row['baseYmd']
        if baseYmd_str in holidayList or dt.datetime.strptime(baseYmd_str, '%Y%m%d').weekday() in [5, 6]:
            visit_dates.at[index, 'holiday'] = 'Y'
        else:
            visit_dates.at[index, 'holiday'] = 'N'

    # 축제 및 관광지 데이터
    fstvl = travel_place.Festival_Schedule(city)
    tour = travel_place.Tourist(city)
    fstvl = fstvl.reset_index()
    tour = tour.reset_index(drop=True)

    # 일자별 축제 개수 구하기
    visit_dates['fstvlIndex'] = None
    visit_dates['fstvlDate'] = None

    for index, row in visit_dates.iterrows():
        date_to_check = dt.datetime.strptime(row['baseYmd'], '%Y%m%d')
        count = fstvl['fstvlDate'].apply(lambda dates: date_to_check.strftime("%Y-%m-%d") in dates).sum()
        visit_dates.at[index, 'fstvlCnt'] = count

        # 해당하는 축제 index, 시간 정제
        if count > 0:
            max_indices = [i for i, dates in enumerate(fstvl['fstvlDate']) if date_to_check.strftime("%Y-%m-%d") in dates]
            sorted_indices = sorted(max_indices, key=lambda x: fstvl.at[x, 'fstvlDate'], reverse=True)[:3]
            dates = [fstvl.at[i, 'fstvlDate'] for i in sorted_indices]
            visit_dates.at[index, 'fstvlIndex'] = sorted_indices
            visit_dates.at[index, 'fstvlDate'] = dates
        else:
            visit_dates.at[index, 'fstvlIndex'] = []
            visit_dates.at[index, 'fstvlDate'] = []

    # 지역별 관광지 갯수
    for index, row in rcmnd_local.iterrows():
        date_to_check = row['signguNm']
        count = tour['addr'].apply(lambda dates: date_to_check in dates).sum()
        rcmnd_local.at[index, 'tourCnt'] = count

    # 일자별 가중치 score
    # touNum: 유동인구
    # holiday: 휴일여부
    # fstvlCnt: 축제 갯수
    visit_dates['score'] = (visit_dates['touNum'] * 0.0000005 +
                            visit_dates['holiday'].apply(lambda x: 10 if x == 'Y' else 0) +
                            visit_dates['fstvlCnt'] * 5)

    # interval로 랭킹 재정의
    visit_result = visit_dates.sort_values('score', ascending=False)

    visit_result['rank'] = visit_result['score'].rank(method='dense', ascending=False)

    # score 높은 기준으로 range 날짜
    date = util.find_max_range(visit_result, range)

    # 제일 점수가 높은 날짜로 range
    start_date = date[0]
    date_range = pd.date_range(start=start_date, periods=5, freq='D')
    date_range_str = date_range.strftime('%Y%m%d').tolist()

    # 지역 가중치 score
    # tourCnt: 관광지 개수
    # touNum: 유동인구
    rcmnd_local['score'] = (rcmnd_local['tourCnt'] * 5) + (rcmnd_local['touNum'] * 0.0000005)
    rcmnd_result = rcmnd_local.sort_values(['score', 'touNum'], ascending=[False, False])

    filtered_result = visit_result[visit_result['baseYmd'].isin(date_range_str)]

    fstvl = fstvl.reset_index(drop=True)
    result = []

    data_index = 0
    for index, row in filtered_result.iterrows():
        if data_index >= len(rcmnd_result):
            data_index = 0
        duration = []
        fstvl_indices = row['fstvlIndex']
        if len(fstvl_indices) > 3:
            fstvl_indices = fstvl_indices[:3]
        for fstvl_index in fstvl_indices:
            festival_data = fstvl.loc[fstvl_index, ['fstvlNm', 'addr', 'latitude', 'longitude', 'etc']].squeeze().to_dict()
            duration.append({
                'festivalName': festival_data['fstvlNm'],
                'addr': festival_data['addr'],
                'latitude': festival_data['latitude'],
                'longitude': festival_data['longitude'],
                'etc': festival_data['etc']
            })
        if len(duration) < 3:
            festival_name = rcmnd_result.iloc[data_index:data_index + 3 - len(duration)].to_dict('records')
            for festival in festival_name:
                addr = festival['signguNm']
                tour_data = tour[tour['addr'] == addr]
                if not tour_data.empty:
                    festival_info = {
                        'festivalName': tour_data.iloc[0]['fstvlNm'],
                        'addr': tour_data.iloc[0]['addr'],
                        'latitude': tour_data.iloc[0]['latitude'],
                        'longitude': tour_data.iloc[0]['longitude'],
                        'etc': tour_data.iloc[0]['etc']
                    }
                    duration.append(festival_info)
            data_index += 3 - len(duration)
        day = {
            'title': row['baseYmd'],
            'duration': duration
        }
        result.append(day)
        data_index += 1

    return result