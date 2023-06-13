import datetime as dt
import pandas as pd
class utilChk:
    # 계절체크
    def classify_season(self, date):
        month = date.month

        if month in [3, 4, 5]:
            return "Spring"  # Spring
        elif month in [6, 7, 8]:
            return "Summer"  # Summer
        elif month in [9, 10, 11]:
            return "Autumn"  # Autumn
        else:
            return "Winter"  # Winter

    # 휴일체크
    def classify_holiday(self, holidays, date):
        if date.weekday() in [5, 6] or date.strftime("%Y%m%d") in holidays.values():
            return "holiday"
        else:
            return "non-holiday"


    def find_max_range(self, data, range_value):
        rank_result = data.sort_values('rank')  # rank 기준으로 데이터 정렬
        ranks = rank_result['rank'].tolist()  # rank 리스트 추출

        max_range = int(range_value)
        max_length = len(ranks)

        start_index = 0  # 연속된 범위의 시작 인덱스
        max_sum = 0  # 가장 높은 점수 합계
        curr_sum = sum(rank_result.iloc[:max_range]['score'])  # 현재 연속된 범위의 점수 합계

        for i in range(max_length - max_range + 1):
            if curr_sum > max_sum:
                max_sum = curr_sum
                start_index = i

            if i + max_range < max_length:
                curr_sum = curr_sum - rank_result.iloc[i]['score'] + rank_result.iloc[i + max_range]['score']

        return rank_result.iloc[start_index:start_index + max_range]['baseYmd'].tolist()


