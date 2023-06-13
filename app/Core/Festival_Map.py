# def FESTIVAL(CITY_PARM):
#     import requests
#     import pandas as pd
#     import re
#     # import folium #pip install folium
#     import os
#     festival_schedule_lat_lng = '2023_festival_schedule_lat_lng.csv'
#     input_city = CITY_PARM
#     if os.path.isfile(festival_schedule_lat_lng):
#         print("File is exists.")
#     else:
#         #데이터 정제
#         Festivaldata_filename = fr'2023_festival_schedule.csv'
#         Festival_Schedule_df = pd.read_csv(Festivaldata_filename, encoding='utf-8').sort_values('축제시작일자')
#         Festival_Schedule_df['소재지주소'] = Festival_Schedule_df['소재지도로명주소'].str.split().str[0:4].str.join(' ')
#         Festival_Schedule_df.loc[Festival_Schedule_df['소재지주소'].isnull(), '소재지주소'] = Festival_Schedule_df['소재지지번주소'].str.split().str[0:4].str.join(' ')
#         pattern = r'\([^)]*\)'
#         Festival_Schedule_df['소재지주소'] = Festival_Schedule_df['소재지주소'].apply(lambda x: re.sub(pattern, '', x))
#
#         #구글 맵 API 호출(위도경도)
#         def get_lat_lng(address, api_key):
#             base_url = "https://maps.googleapis.com/maps/api/geocode/json"
#             params = {"address": address, "key": api_key}
#             response = requests.get(base_url, params=params)
#             if response.status_code == 200:
#                 data = response.json()
#                 if 'results' in data and len(data['results']) > 0:
#                     lat_lng = data["results"][0]["geometry"]["location"]
#                     return lat_lng["lat"], lat_lng["lng"]
#             return None, None
#
#         address = Festival_Schedule_df['소재지주소']
#         api_key = "AIzaSyC1ZQXbvmO4tecLZzR8OssfYaLLnG8Y6TI"
#         Festival_Schedule_df['위도'], Festival_Schedule_df['경도'] = zip(*Festival_Schedule_df['소재지주소'].apply(lambda x: get_lat_lng(x, api_key)))
#         Festival_Schedule_df.to_csv(festival_schedule_lat_lng, encoding='utf-8-sig', index=False)
#
#     Festival_Schedule_df = pd.read_csv(festival_schedule_lat_lng, encoding='utf-8')
#
#
#     def Festival_folium(input_city):
#
#         Festival_Schedule_df_filtered = Festival_Schedule_df[Festival_Schedule_df['소재지주소'].str.contains(input_city)]
#         Festival_map = folium.Map(location=[37.5665, 126.9780], zoom_start=11)
#
#         for idx, row in Festival_Schedule_df_filtered.iterrows():
#             folium.Marker(
#                 tooltip=str(row['축제명']),
#                 location=[row['위도'], row['경도']],
#                 popup=folium.Popup(('축제명: ' + str(row['축제명']) + '<br>'
#                                     '소재지주소: ' + str(row['소재지주소']) + '<br>'
#                                     '축제기간: ' + str(row['축제시작일자']) + ' ~ ' + str(row['축제종료일자'])),
#                                    max_width=250)
#             ).add_to(Festival_map)
#
#         return Festival_map
#
#     MAP = Festival_folium(input_city)
#     return MAP
