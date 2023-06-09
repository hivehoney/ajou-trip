from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hellos {name}"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)