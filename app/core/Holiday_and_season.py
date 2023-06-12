import pandas as pd
from datetime import datetime as dt
from common.api import API
from common.util import utilChk

api = API()
util = utilChk()

# 인기여행지/휴일
global Travel_Place_df, holidays
Travel_Place_df = api.get_travel_place()
holidays = api.get_kr_HOLI_holidays(2023)

class travel_place:
    """
    fstvlHolYear: 년 휴일/축제 정보
    hlYN: 휴일여부
    date: 날짜
    fstvlCnt: 축제 갯수
    season: 계절
    """
    def fstvlHolYear(self, visit, year):
        # 인기여행지 축제정보
        festival_dates_grouped_1, festival_dates_grouped_2 = self.Festival_Schedule()
        City_list = {value for _, value in Travel_Place_df.items() if visit in value}
        print(festival_dates_grouped_1)
        print(festival_dates_grouped_2)
        year = dt.now().year

        def calculate_festival_count(date, City_list, festival_dates_grouped_2):
            count = 0
            for place in City_list:
                if place in festival_dates_grouped_2.index:
                    festival_dates = festival_dates_grouped_2.loc[place, 'fstvlDate']
                    if date in festival_dates:
                        count += 1
            return count

        Festival_place = list(festival_dates_grouped_2.index)
        #for _, value in City_list.items():
        # 휴일데이터생성
        '''
        holiday_df['fstvlCnt'] = holiday_df['date'].apply(lambda x: sum(
            str(x.split()[0]) in festival_dates for festival_dates in
            festival_dates_grouped_2.loc['addr', 'fstvlDate']) if visit in Festival_place else 0)
        result_df = holiday_df
        '''
        date_list = pd.date_range(f'{year}-01-01', f'{year}-12-31')
        holiday_df = pd.DataFrame({"date": date_list})
        holiday_df["hlYN"] = holiday_df["date"].apply(lambda date: util.classify_holiday(holidays, date))
        holiday_df['date'] = holiday_df['date'].dt.strftime('%Y-%m-%d')

        places_in_visit = [place for place in Festival_place if visit in place]
        holiday_df['fstvlCnt'] = holiday_df['date'].apply(
            lambda x: calculate_festival_count(x, places_in_visit, festival_dates_grouped_2)
        )
        result_df = holiday_df
        print(result_df.to_string())

        return result_df
        # folder_path = f'{year}_holidayandseason_data'
        # if not os.path.exists(folder_path):
        #     os.makedirs(folder_path)
        #
        # result_df.to_csv(os.path.join(folder_path, f'{year}_result_data({value}).csv'), encoding='utf-8-sig', index=False)


    """
    Festival_Schedule: 축제일정
    fstvlNm: 축제명
    addr: 소재지주소
    rdnmadr: 소재지도로명주소
    lnmadr: 소재지지번주소
    fstvlStartDate: 축제시작일자
    fstvlEndDate: 축제종료일자
    fstvlDate: 축제일
    """

    def Festival_Schedule(self):
        # Festivaldata_filename = fr'2023_festival_schedule.csv'
        # Festival_Schedule_df = pd.read_csv(Festivaldata_filename, encoding='utf-8').sort_values('축제시작일자')
        Festival_Schedule_df = pd.DataFrame(api.get_festival())

        # addr(소재지주소) 컬럼으로 병합
        Festival_Schedule_df['addr'] = Festival_Schedule_df['rdnmadr'].str.split().str[:2].str.join(' ')
        Festival_Schedule_df.loc[Festival_Schedule_df['addr'].isnull(), 'addr'] = Festival_Schedule_df['lnmadr'].str.split().str[:2].str.join(' ')

        del Festival_Schedule_df['rdnmadr']
        del Festival_Schedule_df['lnmadr']

        # 데이터 format
        Festival_Schedule_df['addr'] = Festival_Schedule_df['addr'].fillna('')
        Festival_Schedule_df['fstvlStartDate'] = pd.to_datetime(Festival_Schedule_df['fstvlStartDate'])
        Festival_Schedule_df['fstvlEndDate'] = pd.to_datetime(Festival_Schedule_df['fstvlEndDate'])

        # 시작일~종료일 날짜 생성
        festival_dates = pd.concat([pd.DataFrame(
            {'fstvlNm': row['fstvlNm'], 'fstvlDate': pd.date_range(row['fstvlStartDate'], row['fstvlEndDate'])
                , 'addr': row['addr']}) for i, row in Festival_Schedule_df.iterrows()])

        # 인기여행지인 곳만 생성
        festival_dates = festival_dates[festival_dates['addr'].isin(Travel_Place_df.values())]

        # 데이터 포맷
        festival_dates['fstvlDate'] = pd.to_datetime(festival_dates['fstvlDate']).dt.strftime('%Y-%m-%d')
        festival_dates_grouped_1 = festival_dates.groupby(['fstvlNm', 'addr']).agg({'fstvlDate': list})
        festival_dates_grouped_2 = festival_dates.groupby(['addr']).agg(fstvlDate=('fstvlDate', lambda x: list(x)))

        return festival_dates_grouped_1, festival_dates_grouped_2

