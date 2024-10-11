# -*- coding: utf-8 -*-
"""김.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qmeYV9_54_XKd-3wyO1UDGb__bObGWj0

소비자물가 지수 (2020 ~ 2024, 8월)

2020 = 100
"""

import matplotlib.pyplot as plt
import pandas as pd

cpi = pd.read_csv('품목별_소비자물가지수_품목성질별_2020100__20241009222935.csv')

# 열 이름에 '08'이 포함된 열을 필터링
columns_with_08 = [col for col in cpi.columns if '08' in col]

# '김' 행에서 8월 데이터만 추출하고 소수점 첫째 자리까지 반올림
laver = [round(value, 1) for value in cpi.loc[0, columns_with_08].values.tolist()]
# '맛김' 행에서 8월 데이터만 추출하고 소수점 첫째 자리까지 반올림
s_laver = [round(value, 1) for value in cpi.loc[1, columns_with_08].values.tolist()]

print(laver)
print(s_laver)

# x축 위치 설정 (막대의 위치를 조정)
x = range(len(columns_with_08))
width = 0.3  # 막대의 폭 설정
gap = 0.02    # 막대 간격 추가

# 막대 그래프 그리기 (간격을 위해 x 위치를 조정)
plt.bar([p - (width / 2 + gap) for p in x], laver, width=width, label='laver', color='black')
plt.bar([p + (width / 2 + gap) for p in x], s_laver, width=width, label='seasoned laver', color='g')

# x축에 연도 레이블 추가
years = [2020, 2021, 2022, 2023, 2024]
plt.xticks(x, years)

# y축 범위 설정 (90부터 최대값보다 조금 더 높게)
plt.ylim(90, max(laver + s_laver) + 20)

# 그래프 설정
plt.xlabel('Year')
plt.ylabel('CPI')
plt.title('Laver CPI (2020 - 2024, August)')
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.7) # y축에 격자 추가 (보조선이 점선 형태로 표시되도록 설정)
plt.tight_layout()  # 그래프 레이아웃 조정 (항목이 잘리지 않도록 자동으로 간격 조정)

# 값 레이블 추가
for i in range(len(laver)):
    plt.text(x[i] - (width / 2 + gap), laver[i] + 2, str(laver[i]), ha='center', color='black', fontweight='bold', fontsize= 8)
    plt.text(x[i] + (width / 2 + gap), s_laver[i] + 2, str(s_laver[i]), ha='center', color='green', fontweight='bold', fontsize= 8)

# 그래프 표시
plt.show()

"""고흥 연도별 평균 수온 (2020 ~ 2024)"""

import matplotlib.pyplot as plt
import pandas as pd

temp_df = pd.read_csv('평균수온_고흥.csv', encoding='euc-kr')

# '일시' 컬럼을 날짜 형식으로 변환
temp_df['일시'] = pd.to_datetime(temp_df['일시'])

# 연도별 평균 수온 계산
years = temp_df['일시'].dt.year.unique()  # 연도 목록을 가져옴
temp = []  # 연평균 수온을 저장할 리스트

for year in years:
    avg = temp_df[temp_df['일시'].dt.year == year]['평균 수온(°C)'].mean()
    temp.append(round(avg, 1))  # 소수점 첫째 자리까지 반올림하여 추가

print(temp)

# 선 그래프 생성
plt.figure(figsize=(10, 6))
plt.plot(years, temp, marker='o', color='skyblue', linestyle='-', linewidth=2, markersize=8)

# 그래프 레이블 설정
plt.xticks(years)
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.title('Average Sea Temperature (2020 - 2024)')

# y축 범위 설정
plt.ylim([min(temp) - 1, max(temp) + 1])

# 값 라벨 추가
for i, v in enumerate(temp):
    plt.text(years[i], v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

"""김 수출량 웹크롤링"""

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

webpage = requests.get("https://www.kati.net/product/basisInfo.do?lcdCode=MD178")
soup = BeautifulSoup(webpage.content, 'html.parser')

# 최근 5개년 수출입
table = soup.find_all("table")[0]  # 첫 번째 테이블을 선택
rows = table.find_all("tr")[2:]  # 헤더를 제외한 데이터 행 선택

# 데이터를 저장할 리스트 초기화
years = []
weights = []
amounts = []

# 데이터 추출
for row in rows:
    cols = row.find_all("td")
    years.append(row.find("th").text.strip())
    weights.append(int(cols[0].text.strip().replace(',', '')))
    amounts.append(int(cols[1].text.strip().replace(',', '')))
years.reverse()
weights.reverse()
amounts.reverse()

print("Year:", years)
print("Weight (ton):", weights)
print("Amount (1000USD):", amounts)

# 막대 그래프 시각화
fig, ax1 = plt.subplots(figsize=(10, 6))  # 그래프 크기 설정

# 수출 중량 막대 그래프
ax1.bar(years, weights, color='skyblue', label='Weight (ton)', alpha=0.7)
ax1.set_ylabel('Weight (ton)', color='skyblue')
ax1.tick_params(axis='y', labelcolor='skyblue')
ax1.set_ylim(20000, max(weights) + 3000)  # y축 범위 설정

# 두 번째 y축 생성
ax2 = ax1.twinx()
ax2.plot(years, amounts, color='orange', marker='o', label='Amount (1000USD)', linewidth=2)
ax2.set_ylabel('Amount (1000USD)', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# 그래프 레이블 및 제목 설정
ax1.set_xlabel('Year')  # x축 레이블
plt.title('Export Weight and Amount of Laver (2020 - 2024)')  # 그래프 제목

# 격자선 추가
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# 범례 추가
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9), bbox_transform=ax1.transAxes)

# 그래프 표시
plt.tight_layout()  # 레이아웃 조정
plt.show()