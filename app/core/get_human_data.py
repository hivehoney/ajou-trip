import pandas as pd
from datetime import datetime, timedelta

from app.common.api import API

api = API()

# 인기여행지/휴일
global Travel_Place_df, holidays
# Travel_Place_df = api.get_travel_place()


class visitor:
    """
    local_visitor: 지역별 방문자수
    baseYmd:  기준연월일
    signguCode: 시군구코드
    signguNm: 시군구명
    daywkDivCd: 요일구분코드
    daywkDivNm: 요일구분명
    touDivCd: 관광객구분코드
    touDivNm: 관광객구분명
    touNum: 관광객수
    """

    def get_visitor(self, city, st, ed):
        st = datetime.strptime(st, "%Y-%m-%d").strftime("%Y%m%d")
        ed = datetime.strptime(ed, "%Y-%m-%d").strftime("%Y%m%d")

        data = api.get_local_visitor(st, ed)

        # 특정 키 값들로 c 데이터프레임 생성
        select_key = ['baseYmd', 'signguCode', 'signguNm', 'daywkDivCd', 'touNum']
        df = pd.DataFrame(data).filter(select_key, axis=1)
        df['touNum'] = df['touNum'].astype(float).astype(int)

        # 'signguCode'와 'baseYmd'를 기준으로 합치기
        local_visitor = df.groupby(['baseYmd', 'signguCode']).agg({'signguNm': 'first', 'touNum': 'sum', 'daywkDivCd': 'first'}).reset_index()

        # 인기여행지 값들만 가져오기
        local_visitor = local_visitor[local_visitor['signguCode'].isin(Travel_Place_df.keys())]

        # signguNm 시/도 병합처리
        local_visitor.loc[:, 'signguNm'] = local_visitor['signguCode'].map(Travel_Place_df)

        # 선택한 도시
        local_visitor = local_visitor[local_visitor['signguNm'].str.contains(city)]

        return local_visitor

    """
    local_visitor: 3년치 유동인구 데이터
    """
    def local_visitor(self, city, st, ed):
    # def local_visitor(self):
    #     city = "서울특별시"
    #     st = "2022-01-14"
    #     ed = "2022-01-18"

        # 날짜 계산
        st1, ed1 = [datetime.strptime(date, "%Y-%m-%d") - timedelta(days=365) for date in [st, ed]]
        st2, ed2 = [datetime.strptime(date, "%Y-%m-%d") - timedelta(days=365*2) for date in [st, ed]]

        """
        미래여서 없음
        """
        # visitor1 = self.get_visitor(city, st, ed)
        visitor2 = self.get_visitor(city, st1, ed1)
        visitor3 = self.get_visitor(city, st2, ed2)

        print(visitor2)
        return visitor2, visitor3
