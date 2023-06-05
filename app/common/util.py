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
