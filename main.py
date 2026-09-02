import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정 및 제목
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

# 2. 커스텀 CSS 적용 (파스텔톤 테마)
st.markdown("""
    <style>
    /* 배경 및 기본 폰트 색상 */
    .main {
        background-color: #F9F9FB;
    }
    /* 타이틀 및 헤더 파스텔 컬러 스타일링 */
    h1 {
        color: #5B6B82 !important;
        font-family: 'Malgun Gothic', sans-serif;
    }
    h2, h3 {
        color: #72829D !important;
    }
    /* 알 수 있는 것 안내 박스 파스텔톤 스타일링 */
    .insight-box {
        background-color: #EEF2F6;
        border-left: 5px solid #A2B5CD;
        padding: 15px;
        border-radius: 8px;
        color: #4A5568;
        font-size: 15px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

# 파스텔톤 Plotly 컬러 팔레트 정의
PASTEL_COLORS = [
    "#B3CDE3", "#CCEBC5", "#DECBE4", "#FED9A6", 
    "#FFFFCC", "#E5D8BD", "#FDDAEC", "#F2F2F2"
]

# 3. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 열 전처리: 세로막대 기호(|)로 분리되어 있는 경우 첫 번째 장르만 추출
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    return df

df = load_data()

st.markdown("---")

# ---------------------------------------------------------
# 1번 그래프: 장르별 영화 편수 (Plotly 도넛 차트)
# ---------------------------------------------------------
st.header("1. 장르별 영화 편수 분포")

# 장르별 빈도수 계산
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화 편수']

# Plotly 도넛 차트 생성 (파스텔톤 적용)
fig_donut = px.pie(
    genre_counts,
    values='영화 편수',
    names='장르',
    hole=0.4,
    title="장르별 영화 비율 및 편수",
    color_discrete_sequence=PASTEL_COLORS
)

# 마우스오버(Hover) 설정
fig_donut.update_traces(
    textposition='inside',
    textinfo='percent+label',
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}"
)

# 그래프 레이아웃 파스텔톤에 맞춰 깔끔하게 정리
fig_donut.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color="#4A5568")
)

st.plotly_chart(fig_donut, use_container_width=True)

# 하단 정보 구역
st.subheader("💡 이 그래프로 알 수 있는 것")
st.markdown("""
<div class="insight-box">
    박스오피스 상위권 영화 중 특정 장르(예: 드라마, 액션 등)가 차지하는 비중과 전체적인 장르 분포 편중을 한눈에 파악할 수 있습니다.
</div>
""", unsafe_allow_html=True)

st.write("")
st.divider()
st.write("")

# ---------------------------------------------------------
# 2번 그래프: 장르-영화별 총 관객수 (Plotly 트리맵)
# ---------------------------------------------------------
st.header("2. 장르 및 영화별 총 관객수 (트리맵)")

# Plotly 트리맵 생성 (장르 -> 영화명 위계 구조, 크기는 total_audi)
fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체 장르"), 'genre', 'movieNm'],
    values='total_audi',
    title="장르 및 영화별 총 관객수 분포",
    color_discrete_sequence=PASTEL_COLORS
)

# 마우스오버(Hover) 시 영화명과 총 관객수가 깔끔하게 표시되도록 설정
fig_treemap.update_traces(
    hovertemplate="<b>영화명:</b> %{label}<br><b>총 관객수:</b> %{value:,}명",
    marker=dict(cornerradius=3)  # 파스텔톤에 어울리도록 살짝 모서리 라운딩
)

# 그래프 레이아웃 배경 투명화
fig_treemap.update_layout(
    margin=dict(t=40, l=10, r=10, b=10),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color="#4A5568")
)

st.plotly_chart(fig_treemap, use_container_width=True)

# 하단 정보 구역
st.subheader("💡 이 그래프로 알 수 있는 것")
st.markdown("""
<div class="insight-box">
    각 장르가 전체 흥행(관객수)에서 차지하는 규모뿐만 아니라, 특정 장르 내에서 어떤 영화가 흥행을 주도했는지 세부 비중을 한눈에 비교할 수 있습니다.
</div>
""", unsafe_allow_html=True)
