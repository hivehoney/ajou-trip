def HUMANDATA(CITY_PARM):
    import pandas as pd
    import seaborn as sns #pip install seaborn
    import matplotlib.pyplot as plt #pip install matplotlib
    import mpld3

    plt.rcParams['font.family'] = 'Malgun Gothic'
    Citydata_filename = fr'Citydata_2023-05-20.csv'
    All_City_df = pd.read_csv(Citydata_filename, usecols=['도시이름'])
    City_list = All_City_df['도시이름'].tolist()
    print(City_list)

    input_city = CITY_PARM
    # 계절 추출
    def get_season(month):
        if month in [3, 4, 5]:
            return '봄'
        elif month in [6, 7, 8]:
            return '여름'
        elif month in [9, 10, 11]:
            return '가을'
        else:
            return '겨울'


    def Human_data_3_years(input_city):
        for city in [x for x in City_list if input_city in x]:
            #3년치 유동인구 데이터 병합
            csv_file_2020 = fr"2020_holidayandseason_data\2020_result_data({city}).csv"
            csv_file_2021 = fr"2021_holidayandseason_data\2021_result_data({city}).csv"
            csv_file_2022 = fr"2022_holidayandseason_data\2022_result_data({city}).csv"
            csv_files = [csv_file_2020,csv_file_2021,csv_file_2022]
            HolidayAndSeason_df = [pd.read_csv(file, encoding='utf-8') for file in csv_files]
            HolidayAndSeason_Merge_df = pd.concat(HolidayAndSeason_df, ignore_index=True)
            HolidayAndSeason_Merge_df.set_index('날짜', inplace=True)
            HolidayAndSeason_Merge_df['월'] = pd.to_datetime(HolidayAndSeason_Merge_df.index).month

            #데이터 정제
            HolidayAndSeason_Merge_df['계절'] = HolidayAndSeason_Merge_df['월'].apply(get_season)
            correlation = HolidayAndSeason_Merge_df.groupby('계절')['유동인구수'].mean().reset_index()

            #가시화
            fig = plt.figure(figsize=(8, 6))
            sns.barplot(data=correlation, x='계절', y='유동인구수', palette='Set1')
            plt.title('계절별 유동인구수 평균')
            plt.xlabel('계절')
            plt.ylabel('유동인구수')
            plt.show()
            mpld3.save_html(fig, fr"{city}_Season_Tour_Human.html")
    Human_data_3_years(input_city)