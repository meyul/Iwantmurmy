import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2", layout="wide")

# 2. 커스텀 폰트 및 디자인 CSS 적용 (전체 배경색, 폰트, 카드 스타일)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 전체 배경색 - 은은한 파스텔 라벤더/그레이 */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }

    /* 섹션별 카드 스타일 */
    .graph-card {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }

    /* 제목 스타일 */
    .main-title {
        color: #4A5568;
        font-weight: 700;
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
        border-bottom: 2px solid #CBD5E0;
    }

    /* 알 수 있는 것 박스 */
    .insight-container {
        background-color: #F7FAFC;
        border-left: 6px solid #BEE3F8;
        padding: 15px 20px;
        margin-top: 20px;
        border-radius: 5px;
        font-size: 1.05rem;
        color: #2D3748;
    }
    
    .highlight {
        color: #3182CE;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀
st.markdown("<h1 class='main-title'>🎨 영화 데이터 그래프 도감 2 - 분포와 관계</h1>", unsafe_allow_html=True)

# 3. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    return df

df = load_data()

# 파스텔 컬러 팔레트
PASTEL_PALETTE = ["#A0CED9", "#ADF7B6", "#FFEE93", "#FFC09F", "#D1B3FF", "#BEE3F8", "#FFD1DC"]

# ---------------------------------------------------------
# [그래프 1] 도넛 그래프 - 장르 분포
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.header("1. 어떤 장르의 영화가 가장 많을까?")
    
    genre_counts = df['genre'].value_counts().reset_index()
    genre_counts.columns = ['장르', '영화 편수']

    fig1 = px.pie(
        genre_counts, values='영화 편수', names='장르', hole=0.5,
        color_discrete_sequence=PASTEL_PALETTE
    )
    fig1.update_traces(hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}")
    fig1.update_layout(margin=dict(t=20, b=20), paper_bgcolor='rgba(0,0,0,0)')
    
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown(f"""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것:</b><br>
        영화 시장에서 <span class='highlight'>{genre_counts.iloc[0]['장르']}</span> 장르가 가장 높은 빈도를 차지하고 있으며, 
        전체적인 장르 다양성을 한눈에 파악할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# [그래프 2] 트리맵 - 장르별 흥행 규모
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.header("2. 장르별 흥행 영화 상세 도감")
    
    fig2 = px.treemap(
        df, path=[px.Constant("전체"), 'genre', 'movieNm'], values='total_audi',
        color_discrete_sequence=PASTEL_PALETTE
    )
    fig2.update_traces(hovertemplate="<b>영화명:</b> %{label}<br><b>총 관객수:</b> %{value:,}명")
    fig2.update_layout(margin=dict(t=30, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
    
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것:</b><br>
        칸의 크기를 통해 장르별 관객 동원력을 비교할 수 있으며, 
        각 장르 내에서 어떤 영화가 가장 <span class='highlight'>압도적인 흥행</span>을 거두었는지 직관적으로 보여줍니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# [그래프 3] 히스토그램 - 관객수 분포
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.header("3. 흥행 실적의 분포 (히스토그램)")
    
    # 히스토그램 생성
    fig3 = px.histogram(
        df, x="total_audi", nbins=30,
        labels={'total_audi': '총 관객수', 'count': '영화 수'},
        color_discrete_sequence=["#A0CED9"]
    )
    fig3.update_layout(
        bargap=0.1,
        xaxis_title="총 관객수",
        yaxis_title="영화 편수",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # 데이터 분석
    max_movie = df.loc[df['total_audi'].idxmax()]
    # 가장 많이 몰려있는 구간 (대략적인 수치 계산)
    counts, bins = pd.cut(df['total_audi'], bins=10, retbins=True)
    most_common_range = counts.value_counts().idxmax()
    
    st.markdown(f"""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것:</b><br>
        대부분의 영화는 관객수 <span class='highlight'>{most_common_range}</span> 구간에 밀집되어 있는 '롱테일' 분포를 보입니다.<br>
        분석 데이터 중 가장 관객수가 많은 영화는 <span class='highlight'>{max_movie['movieNm']}</span> (약 {max_movie['total_audi']/10000:.0f}만 명)입니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("데이터 출처: KOBIS 영화관 입장권 통합전산망")
