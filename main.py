import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2", layout="wide")

# 2. 고품질 파스텔 매거진 스타일 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }

    /* 은은하고 고상한 핑크-라벤더 파스텔 배경 */
    .stApp {
        background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
    }

    /* 카드 헤더 및 서브타이틀 */
    .section-title {
        color: #2D3748;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .section-subtitle {
        color: #718096;
        font-size: 0.95rem;
        margin-bottom: 20px;
    }

    /* 화이트 유리 질감 카드 디자인 */
    .graph-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 24px;
        padding: 32px;
        box-shadow: 0 10px 30px rgba(160, 175, 200, 0.12);
        margin-bottom: 35px;
    }

    /* 메인 타이틀 배너 */
    .hero-banner {
        text-align: center;
        padding: 40px 20px 20px 20px;
        margin-bottom: 30px;
    }
    
    .hero-title {
        font-size: 2.3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4A5568 0%, #718096 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .hero-desc {
        color: #A0AEC0;
        font-size: 1rem;
    }

    /* 알 수 있는 것 박스 (Soft Pastel Callout) */
    .insight-container {
        background: #F7FAFC;
        border-radius: 16px;
        border-left: 5px solid #CBD5E0;
        padding: 18px 22px;
        margin-top: 20px;
        font-size: 0.98rem;
        color: #4A5568;
        line-height: 1.6;
    }
    
    .highlight {
        color: #4C51BF;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀 배너
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🎬 영화 데이터 그래프 도감 2</div>
        <div class="hero-desc">박스오피스 상위권 영화 216편의 분포와 스크린·관객수 관계 시각화</div>
    </div>
""", unsafe_allow_html=True)

# 3. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    return df

df = load_data()

# 세련된 파스텔 팔레트
PASTEL_PALETTE = [
    "#9AE6B4", "#90CDF4", "#FBB6CE", "#FBD38D", "#E9D8FD",
    "#FEB2B2", "#CBD5E0", "#B2F5EA", "#FAF089", "#D6BCFA"
]

# ---------------------------------------------------------
# [그래프 1] 도넛 차트 - 장르 분포
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>1. 장르별 영화 편수 분포</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>영화 시장에서 각 장르가 차지하는 비중과 도넛 구조</div>", unsafe_allow_html=True)
    
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
        <b>💡 이 그래프로 알 수 있는 것</b><br>
        박스오피스 주요 영화 중 <span class='highlight'>{genre_counts.iloc[0]['장르']}</span> 장르가 가장 높은 편수를 기록하고 있으며, 전체적인 장르 치우침 현상을 한눈에 파악할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# [그래프 2] 트리맵 - 장르 및 영화별 총 관객수
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>2. 장르 및 개별 영화 흥행 규모 (트리맵)</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>장르 영역 및 개별 영화 박스의 크기로 비교하는 관객수</div>", unsafe_allow_html=True)
    
    fig2 = px.treemap(
        df, path=[px.Constant("전체"), 'genre', 'movieNm'], values='total_audi',
        color_discrete_sequence=PASTEL_PALETTE
    )
    fig2.update_traces(
        hovertemplate="<b>영화명:</b> %{label}<br><b>총 관객수:</b> %{value:,}명",
        marker=dict(cornerradius=4)
    )
    fig2.update_layout(margin=dict(t=20, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
    
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것</b><br>
        각 장르의 전체 파급력과 더불어 특정 장르 내에서 어떤 영화가 메가 히트를 기록하여 관객 비중을 이끌었는지 비교 분석할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# [그래프 3] 히스토그램 - 관객수 분포
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>3. 관객수 구간별 분포 (히스토그램)</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>대부분의 영화가 집중된 관객수 구간 탐색</div>", unsafe_allow_html=True)
    
    fig3 = px.histogram(
        df, x="total_audi", nbins=25,
        labels={'total_audi': '총 관객수', 'count': '영화 수'},
        color_discrete_sequence=["#B2F5EA"]
    )
    fig3.update_traces(marker=dict(line=dict(width=1, color='white')))
    fig3.update_layout(
        bargap=0.1,
        xaxis_title="총 관객수 (명)",
        yaxis_title="영화 수 (편)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    max_movie = df.loc[df['total_audi'].idxmax()]
    counts, bins = pd.cut(df['total_audi'], bins=10, retbins=True)
    most_common_range = counts.value_counts().idxmax()
    
    st.markdown(f"""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것</b><br>
        대부분의 영화는 관객수 <span class='highlight'>{most_common_range}</span> 구간에 밀집되어 있으며,<br>
        분석 대상 중 최대 흥행작은 <span class='highlight'>{max_movie['movieNm']}</span>(총 관객수 약 {max_movie['total_audi']/10000:.0f}만 명)입니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# [그래프 4] 산점도 - 개봉일 스크린수 vs 총 관객수
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>4. 개봉일 스크린수와 총 관객수의 관계 (산점도)</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>스크린 확보 수와 최종 흥행 결과 간 상관관계 분석</div>", unsafe_allow_html=True)
    
    fig4 = px.scatter(
        df,
        x='first_scrn',
        y='total_audi',
        color='genre',
        hover_name='movieNm',
        labels={'first_scrn': '개봉일 스크린수', 'total_audi': '총 관객수', 'genre': '장르'},
        color_discrete_sequence=PASTEL_PALETTE
    )
    fig4.update_traces(
        marker=dict(size=11, opacity=0.85, line=dict(width=1, color='white')),
        hovertemplate="<b>%{hovertext}</b><br><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명"
    )
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(200, 200, 200, 0.2)', title="개봉일 스크린수 (개)"),
        yaxis=dict(gridcolor='rgba(200, 200, 200, 0.2)', title="총 관객수 (명)"),
        legend_title_text="장르"
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것</b><br>
        개봉일 스크린수를 많이 확보한 영화일수록 대체로 높은 총 관객수를 달성하는 양의 상관관계를 보이지만, 스크린수 대비 폭발적인 흥행 성과를 거둔 영화(아웃라이어)도 존재함을 확인할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# [그래프 5] 상자 그림(Box Plot) - 주요 장르별 관객수 분포 (신규 추가)
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>5. 주요 장르별 총 관객수 분포 비교 (상자 그림)</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>영화 수 10편 이상인 장르의 관객수 중앙값 및 이상치(Outlier) 확인</div>", unsafe_allow_html=True)
    
    # 영화 수가 10편 이상인 장르 필터링
    genre_counts = df['genre'].value_counts()
    major_genres = genre_counts[genre_counts >= 10].index
    df_major = df[df['genre'].isin(major_genres)]
    
    fig5 = px.box(
        df_major,
        x='genre',
        y='total_audi',
        color='genre',
        hover_name='movieNm',
        points='outliers',  # 박스 바깥의 이상치 개별 포인트 표시
        labels={'genre': '장르', 'total_audi': '총 관객수'},
        color_discrete_sequence=PASTEL_PALETTE
    )
    
    fig5.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>장르: %{x}<br>총 관객수: %{y:,}명"
    )
    
    fig5.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(200, 200, 200, 0.2)', title="주요 장르"),
        yaxis=dict(gridcolor='rgba(200, 200, 200, 0.2)', title="총 관객수 (명)"),
        showlegend=False
    )
    
    st.plotly_chart(fig5, use_container_width=True)
    
    st.markdown("""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것</b><br>
        주요 장르별 관객수의 중앙값과 상하위 편차를 한눈에 파악할 수 있으며, 상자 밖으로 멀리 떨어진 점(이상치)을 통해 동일 장르 내에서 대흥행을 기록한 대표 영화를 찾아낼 수 있습니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("데이터 출처: KOBIS 영화관 입장권 통합전산망")
