import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from core.Scoring import RECOMMEND_DATA

# fsho = travel_place()
# visitor = visitor()
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# def main():
#     start = 20220101
#     end = 20221231
#     visit = visitor.local_visitor("서울특별시", "20220114", "20220118")
#     # fsho.fstvlHolYear(visit, start, end)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3302"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
def hello(id: str, start_date: str, end_date: str, range: str):
    start_date = start_date
    end_date = end_date
    result = RECOMMEND_DATA(id, start_date, end_date)
    return {"message": f"Hellossss {start_date}"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)


hello("부산광역시", "2023-06-15", "2023-07-15", "3")