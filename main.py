import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정 및 제목
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 2. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 열 전처리: 세로막대 기호(|)로 분리되어 있는 경우 첫 번째 장르만 extraction
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    return df

df = load_data()

st.markdown("---")

# 3. 첫 번째 그래프: 장르별 영화 편수 (Plotly 도넛 차트)
st.header("1. 장르별 영화 편수 분포")

# 장르별 빈도수 계산
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화 편수']

# Plotly 도넛 차트 생성
fig = px.pie(
    genre_counts,
    values='영화 편수',
    names='장르',
    hole=0.4,
    title="장르별 영화 비율 및 편수"
)

# 마우스오버(Hover) 시 편수와 비율이 함께 표시되도록 설정
fig.update_traces(
    textposition='inside',
    textinfo='percent+label',
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}"
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 그래프 하단 구역 구분 및 알 수 있는 점 안내
st.divider()
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("박스오피스 상위권 영화 중 특정 장르(예: 드라마, 액션 등)가 차지하는 비중과 전체적인 장르 분포 편중을 한눈에 파악할 수 있습니다.")
