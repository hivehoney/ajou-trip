import pandas as pd

# 파일명
file_name = 'C:\\Python\\test.xlsx'

# Daraframe형식으로 엑셀 파일 읽기
df = pd.read_excel(file_name)

# 데이터 프레임 출력
print(df)