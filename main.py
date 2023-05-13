from fastapi import FastAPI
import pandas as pd
import requests
import json

app = FastAPI()
sk_url = "https://apis.openapi.sk.com/puzzle/traveler-count/raw/daily/districts/5011000000?gender=all&ageGrp=all&companionType=all"
go_url = 'http://apis.data.go.kr/1360000/SfcMtlyInfoService/getDailyWthrData?serviceKey=Pm03tXCB2ZJ%2BbD7FGDUmckrH2bJUO51xVBAEbNMTc1roEH2S91LuL%2BmMmEhmVvf5BxAqk2%2BLbrI3WUhtF1O%2BnA%3D%3D&numOfRows=10&dataType=JSON&pageNo=1&year=2023&month=02&station=90'
params ={'serviceKey' : '서비스키', 'pageNo' : '1', 'numOfRows' : '10', 'dataType' : 'JSON', 'stnId' : '108', 'tmFc' : '201310170600' }


headers = {
    "accept": "application/json",
    "appkey": "l7xx846db5f3bc1e48d29b7275a745d501c8"
}
# async def request(client):
#     response = await client.get(URL, headers=headers)
#     return response.text
#
#
# async def task():
#     async with httpx.AsyncClient() as client:
#         tasks = [request(client) for i in range(100)]
#         result = await asyncio.gather(*tasks)s
#         print(result)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hellos {name}"}


#@app.get("/test")
#def get_peole():
#    response = requests.get(sk_url, headers=headers)
#    return response.text


@app.get("/test1")
def Weather_API():
    response = requests.get(go_url)
    Weather_data = json.loads(response.content)
    Weather_items = Weather_data['response']['body']['items']['item'][0]['stndays']['stn_ko']
    Weather_info = Weather_data['response']['body']['items']['item'][0]['stndays']['info']
    Weather_items_df = pd.DataFrame([Weather_items])
    Weather_info_df = pd.DataFrame(Weather_info)

    return Weather_items_df, Weather_info_df
