import openpyxl

# 엑셀 파일 열기
wb = openpyxl.load_workbook('C:\\Python\\Python311\\excel_sample.xlsx')  # 파일 경로와 이름을 적절히 수정해주세요

# 시트 선택
sheet = wb['sheet1']  # 시트 이름을 적절히 수정해주세요

# 셀 읽기
value = sheet['A1'].value  # A1 셀의 값을 읽어옵니다
print(f'A1 셀 값: {value}')

# 셀 쓰기
sheet['B1'] = 'Hello, World!'  # B1 셀에 'Hello, World!'라는 값 씁니다

# 엑셀 파일 저장
wb.save('C:\\Python\\Python311\\excel_sample.xlsx')  # 저장할 파일 경로와 이름을 적절히 수정해주세요

# 엑셀 파일 닫기
wb.close()
