import datetime as dt
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


    def find_consecutive_dates(self, data, range_value):
        sorted_data = data.sort_values('rank')
        ranks = sorted_data['rank'].tolist()
        dates = sorted_data['baseYmd'].tolist()

        consecutive_dates = []
        max_range = round(int(range_value) / 2)
        data_length = len(ranks)

        for i in range(data_length - int(range_value) + 1):
            rank_range = ranks[i:i+int(range_value)]
            date_range = [dt.datetime.strptime(date, '%Y%m%d') for date in dates[i:i+int(range_value)]]
            sorted_range = sorted(date_range)
            date_diff = [(sorted_range[j+1] - sorted_range[j]).days for j in range(int(range_value) - 1)]
            if all(diff == 1 for diff in date_diff) and all(rank_range[j] <= rank_range[j+1] for j in range(int(range_value) - 1)):
                consecutive_dates = date_range
                break

        return consecutive_dates