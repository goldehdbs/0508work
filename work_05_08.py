# 5월 8일 과제

#  - 현재 페이지의 모든 시각화 내용을 streamlit으로 구현

#  - 세부 내용은 주석 참고

# 1

# Pandas 함수로 2개 데이터 파일을 읽고 합쳐서 1개의 데이터프레임 변수명 df에 할당하는 코드를 작성하세요.

#  - heart_failure_a.json파일을 읽어 데이터프레임 변수명 df_a에 할당하세요.

#  - heart_failure_b.json 파일을 읽어 데이터 프레임 변수명 df_b에 할당하세요.

#  - df_a, df_b를 합쳐서 하나의 데이터프레임으로 만드세요. 판다스의 merge를 활용하세요

#     - 기준 열 (on) : 'person_id'

#     - 합치는 방법(how) : 'inner'

import streamlit as st

import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt



df_a = pd.read_json(r'./heart_failure_a.json')

df_b = pd.read_json(r'./heart_failure_b.json')


st.title(" 심부전증 데이터 분석 대시보드")

# --- 1. 데이터 불러오기 및 병합 ---
df = pd.merge(df_a, df_b, on='person_id', how='inner')

# 사라진 데이터 개수 계산
dropped_num = len(df_a) - len(df) + len(df_b) - len(df)
st.info(f"데이터 병합 과정에서 제외된 데이터 개수(dropped_num): {dropped_num}개")

st.divider()

# --- 2. Jointplot ---
st.subheader("1. 박출계수(ejection_fraction)와 나이(age)의 상관관계")
g = sns.jointplot(data=df, x='ejection_fraction', y='age', hue='DEATH_EVENT')
st.pyplot(g.figure)

st.divider()


st.subheader("2. 죽음과 당뇨, 흡연의 상관관계")

smoke_option = st.radio(
    "흡연 여부를 선택하세요:", 
    ("전체 (Split 비교)", "흡연자 (1)", "비흡연자 (0)")
)

fig2, ax2 = plt.subplots()

if smoke_option == "전체 (Split 비교)":
  
    sns.violinplot(data=df, x='DEATH_EVENT', y='platelets', hue='smoking', split=True, ax=ax2)
elif smoke_option == "흡연자 (1)":
  
    df_smoke = df[df['smoking'] == 1]
    sns.violinplot(data=df_smoke, x='DEATH_EVENT', y='platelets', ax=ax2)
else:
    # 비흡연자만 필터링
    df_no_smoke = df[df['smoking'] == 0]
    sns.violinplot(data=df_no_smoke, x='DEATH_EVENT', y='platelets', ax=ax2)

st.pyplot(fig2)

st.divider()

# --- 4. Histplot (Slider 연동) ---
st.subheader("3. 시간(time)에 따른 히스토그램")
min_ef = float(df['ejection_fraction'].min())
max_ef = float(df['ejection_fraction'].max())

ef_range = st.slider(
    "심박출(ejection_fraction) 범위를 선택하세요:",
    min_value=min_ef, 
    max_value=max_ef, 
    value=(min_ef, max_ef) 
)

df_filtered = df[(df['ejection_fraction'] >= ef_range[0]) & (df['ejection_fraction'] <= ef_range[1])]

fig3, ax3 = plt.subplots()
sns.histplot(data=df_filtered, x='time', bins=20, hue='DEATH_EVENT', ax=ax3)
st.pyplot(fig3)