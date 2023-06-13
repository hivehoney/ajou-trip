import pandas as pd


class travel_place:

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

    def Festival_Schedule(self, city):
        Festivaldata_filename = fr'festival_schedule.csv'
        Festival_Schedule_df = pd.read_csv(Festivaldata_filename, encoding='cp949').sort_values('fstvlStartDate')

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
        festival_dates = pd.concat([pd.DataFrame({'fstvlNm': row['fstvlNm']
                                                    , 'fstvlDate': pd.date_range(row['fstvlStartDate'], row['fstvlEndDate'])
                                                    , 'addr': row['addr']
                                                    , 'latitude': row['latitude']
                                                    , 'longitude': row['longitude']
                                                    , 'etc': row['fstvlNm']
                                                     }) for i, row in Festival_Schedule_df.iterrows()])

        # 인기여행지인 곳만 생성
        festival_dates = festival_dates[festival_dates['addr'].str.contains(city)]

        # 데이터 포맷
        festival_dates['fstvlDate'] = pd.to_datetime(festival_dates['fstvlDate']).dt.strftime('%Y-%m-%d')
        festival_dates_grouped_1 = festival_dates.groupby(['fstvlNm', 'addr']).agg({'fstvlDate': list,
                                                                                    'latitude': 'first',
                                                                                    'longitude': 'first',
                                                                                    'etc': 'first'
                                                                                    }).reset_index()

        # festival_dates_grouped_2 = festival_dates.groupby(['addr']).agg(fstvlDate=('fstvlDate', lambda x: list(x)))

        return festival_dates_grouped_1


    def Tourist(self, city):
        Touristdata_filename = fr'Tourist.csv'
        Tourist_Schedule_df = pd.read_csv(Touristdata_filename, encoding='cp949')

        # addr(소재지주소) 컬럼으로 병합 -- 문제 포인트 (etc를 지우고있음)
        Tourist_Schedule_df['addr'] = Tourist_Schedule_df['rdnmadr'].str.split().str[:2].str.join(' ')
        Tourist_Schedule_df.loc[Tourist_Schedule_df['addr'].isnull(), 'addr'] = Tourist_Schedule_df['lnmadr'].str.split().str[:2].str.join(' ')

        del Tourist_Schedule_df['rdnmadr']
        del Tourist_Schedule_df['lnmadr']

        # 데이터 format
        Tourist_Schedule_df['addr'] = Tourist_Schedule_df['addr'].fillna('')

        # 인기여행지인 곳만 생성
        # 선택한 도시
        Tourist_Schedule_df = Tourist_Schedule_df[Tourist_Schedule_df['addr'].str.contains(city)]
        return Tourist_Schedule_df


#
# travel_place = travel_place()
#
# travel_place.Festival_Schedule("부산")