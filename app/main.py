import pandas as pd
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from Core.Scoring import RECOMMEND_DATA
from Core.Human_data import visitor
from Core.Folium_Map import Folium
from Common.ApiUtil import API

app = FastAPI()
visitor = visitor()
api = API()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3302"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recomand/trip")
def hello(id: str, start_date: str, end_date: str, range: str):
    # 인기여행지/휴일
    # Travel_Place_df = api.get_travel_place()
    # start_date = start_date
    # end_date = end_date
    # visit = visitor.local_visitor(id, start_date, end_date, Travel_Place_df)
    # result = RECOMMEND_DATA(id, start_date, end_date, visit, range)
    #
    # # 시각화 자료 생성
    # Folium(result)
    result = [{'title': '20230701', 'duration': [{'festivalName': '제18회 국제매직페스티벌', 'addr': '부산광역시 해운대구', 'latitude': 35.1629739, 'longitude': 129.1637236, 'etc': '제18회 국제매직페스티벌'}, {'festivalName': '제7회 반송한마음축제', 'addr': '부산광역시 해운대구', 'latitude': 35.1629739, 'longitude': 129.1637236, 'etc': '제7회 반송한마음축제'}, {'festivalName': '만화체험관', 'addr': '부산광역시 동구', 'latitude': 35.13778041, 'longitude': 129.0497944, 'etc': '관광객의 볼거리와 재래시장 활성화를 위해 조성된 웹툰거리 내에 위치한 체험관'}]}, {'title': '20230702', 'duration': [{'festivalName': '임시수도기념관', 'addr': '부산광역시 서구', 'latitude': 35.10374876, 'longitude': 129.0175954, 'etc': '6.25 당시 임시수도로서 국난극복의 역사적 현장을 길이 보전하여,후세에 물려줌으로서 민족사의 암울한 시기를 깨닫게 하고 조국통일과 번영의 산교육장으로 활용하고 있다.'}, {'festivalName': '장림포구', 'addr': '부산광역시 사하구', 'latitude': 35.07915955, 'longitude': 128.9513486, 'etc': '배가 드나드는 강의 어귀로 조선시대 군사요충지였으며, 부네치아라 불림'}, {'festivalName': '요트올림픽동산지구', 'addr': '부산광역시 해운대구', 'latitude': 35.16578256, 'longitude': 129.1350266, 'etc': '360여척의 요트를 계류할  수 있는 요트경기장이 있는 곳으로 요트와 보트 등이 파란 바다와 마린시티의 마천루를 배경으로 어우러져 이국적인 풍경을 자아내는 곳이다. 각종 국제대회는 물론 해양스포츠와 국제영화제를 비롯한 다양한 문화행사가 개최된다'}]}, {'title': '20230703', 'duration': [{'festivalName': '장림포구', 'addr': '부산광역시 사하구', 'latitude': 35.07915955, 'longitude': 128.9513486, 'etc': '배가 드나드는 강의 어귀로 조선시대 군사요충지였으며, 부네치아라 불림'}, {'festivalName': '요트올림픽동산지구', 'addr': '부산광역시 해운대구', 'latitude': 35.16578256, 'longitude': 129.1350266, 'etc': '360여척의 요트를 계류할  수 있는 요트경기장이 있는 곳으로 요트와 보트 등이 파란 바다와 마린시티의 마천루를 배경으로 어우러져 이국적인 풍경을 자아내는 곳이다. 각종 국제대회는 물론 해양스포츠와 국제영화제를 비롯한 다양한 문화행사가 개최된다'}]}, {'title': '20230704', 'duration': [{'festivalName': '용호 Sea-Side 관광지', 'addr': '부산광역시 남구', 'latitude': 35.101225, 'longitude': 129.120361, 'etc': '천혜의 자연경관을 가지고 있고, 인근 오륙도 스카이워그 등 기존의 관광 인프라가 구축'}, {'festivalName': '황령산관광지', 'addr': '부산광역시 수영구', 'latitude': 35.1552432, 'longitude': 129.1029084, 'etc': '부산광역시 금련산청소년수련원 일대이며, 부산 도심 속 천혜의 황령산 자락에 위치하고 있어 부산의 랜드마크인 광안리 해수욕장, 광안대교, 해운대를 한눈에 바라볼 수 있음.'}]}, {'title': '20230705', 'duration': [{'festivalName': '황령산관광지', 'addr': '부산광역시 수영구', 'latitude': 35.1552432, 'longitude': 129.1029084, 'etc': '부산광역시 금련산청소년수련원 일대이며, 부산 도심 속 천혜의 황령산 자락에 위치하고 있어 부산의 랜드마크인 광안리 해수욕장, 광안대교, 해운대를 한눈에 바라볼 수 있음.'}, {'festivalName': '영도관광안내센터', 'addr': '부산광역시 영도구', 'latitude': 35.09454127, 'longitude': 129.0387847, 'etc': '부산의 새로운 관광명소로 각광받고있는 영도대교의 도개모습을 감상하고 영도관광에 필요한 종합서비스를 제공받을 수 있다.'}]}]


    return result

@app.get("/download/map")
def read_item(filename: str):
    Target_file = fr'Downloads/{filename}.html'

    print(f"File Download : {filename}")
    return FileResponse(Target_file, media_type='text/html', filename=filename)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

#
# hello("부산광역시", "2023-06-15", "2023-07-15", "2")