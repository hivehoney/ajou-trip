# 공공데이터로부터 유동인구를 불러옵니다.
import pandas as pd
from app.common.api import API

api = API()
# 인기여행지/휴일
global Travel_Place_df, holidays
Travel_Place_df = api.get_travel_place()


class visitor:
    """
    get_local_visitor: 지역별 방문자수
    baseYmd:  기준연월일
    signguCode: 시군구코드
    signguNm: 시군구명
    daywkDivCd: 요일구분코드
    daywkDivNm: 요일구분명
    touDivCd: 관광객구분코드
    touDivNm: 관광객구분명
    touNum: 관광객수
    """

    def get_local_visitor(self, st, ed):
        data = api.get_local_visitor(st, ed)

        # 특정 키 값들로 데이터프레임 생성
        select_key = ['baseYmd', 'signguCode', 'signguNm', 'daywkDivCd', 'touNum']
        df = pd.DataFrame(data).filter(select_key, axis=1)
        df['touNum'] = df['touNum'].astype(float).astype(int)

        # 'signguCode'와 'baseYmd'를 기준으로 합치기
        local_visitor = df.groupby(['baseYmd', 'signguCode']).agg(
            {'signguNm': 'first', 'touNum': 'sum', 'daywkDivCd': 'first'}).reset_index()

        # 인기여행지 값들만 가져오기
        local_visitor = local_visitor[local_visitor['signguCode'].isin(Travel_Place_df.keys())]

        return local_visitor
