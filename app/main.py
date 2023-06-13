import pandas as pd
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from Core.Scoring import RECOMMEND_DATA
from Core.Human_data import visitor
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

@app.get("/hello")
def hello(id: str, start_date: str, end_date: str, range: str):
    # 인기여행지/휴일
    Travel_Place_df = api.get_travel_place()
    start_date = start_date
    end_date = end_date
    visit = visitor.local_visitor(id, start_date, end_date, Travel_Place_df)
    result = RECOMMEND_DATA(id, start_date, end_date, visit, range)

    return {"message": f"Hellossss {start_date}"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)


hello("부산광역시", "2023-06-15", "2023-07-15", "2")