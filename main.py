from fastapi import FastAPI
import requests

app = FastAPI()
url = '?'
params ={'serviceKey' : '서비스키', 'pageNo' : '1', 'numOfRows' : '10', 'dataType' : 'JSON', 'stnId' : '108', 'tmFc' : '201310170600' }


headers = {
    "accept": "application/json",
    "appkey": "?"
}
# async def request(client):
#     response = await client.get(URL, headers=headers)
#     return response.text
#
#
# async def task():
#     async with httpx.AsyncClient() as client:
#         tasks = [request(client) for i in range(100)]
#         result = await asyncio.gather(*tasks)
#         print(result)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hellos {name}"}


@app.get("/test")
def get_peole():
    response = requests.get(url, headers=headers)
    return response.text
