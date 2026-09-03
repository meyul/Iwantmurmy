import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 감성 도감", layout="wide", page_icon="🎬")

# 2. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    return df

df = load_data()

# 3. 🎨 폰트 설정
FONTS = {
    "Pretendard (트렌디한 산세리프)": {
        "family": "'Pretendard', -apple-system, sans-serif",
        "import_url": "@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');"
    },
    "Noto Sans KR (깔끔한 산세리프)": {
        "family": "'Noto Sans KR', sans-serif",
        "import_url": "@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;600;700&display=swap');"
    },
    "고운바탕 (감성적인 세리프/바탕)": {
        "family": "'Gowun Batang', serif",
        "import_url": "@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');"
    },
    "나눔고딕 (클래식 고딕)": {
        "family": "'Nanum Gothic', sans-serif",
        "import_url": "@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');"
    }
}

# 4. 🎨 4가지 테마 팔레트 정의
THEMES = {
    "🌸 봄날의 벚꽃 (Cherry Blossom)": {
        "bg": "linear-gradient(135deg, #FFFBFC 0%, #FCE4EC 50%, #F3E5F5 100%)",
        "card_bg": "rgba(255, 255, 255, 0.8)",
        "card_border": "rgba(248, 187, 208, 0.6)",
        "text_main": "#4A154B",
        "text_sub": "#AD1457",
        "highlight": "#D81B60",
        "palette": ["#F8BBD0", "#F48FB1", "#CE93D8", "#B39DDB", "#9FA8DA", "#90CAF9", "#80CBC4", "#A5D6A7", "#FFE082", "#FFAB91"]
    },
    "🌃 시티팝 나이트 (City Pop)": {
        "bg": "linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #311042 100%)",
        "card_bg": "rgba(30, 27, 75, 0.65)",
        "card_border": "rgba(192, 132, 252, 0.4)",
        "text_main": "#F3E8FF",
        "text_sub": "#C084FC",
        "highlight": "#F472B6",
        "palette": ["#F472B6", "#C084FC", "#818CF8", "#38BDF8", "#34D399", "#FBBF24", "#FB7185", "#A78BFA", "#4ADE80", "#E879F9"]
    },
    "☕ 따뜻한 우드 라떼 (Warm Latte)": {
        "bg": "linear-gradient(135deg, #FAF8F5 0%, #F5EBE6 50%, #EBD9CE 100%)",
        "card_bg": "rgba(255, 253, 250, 0.85)",
        "card_border": "rgba(215, 186, 167, 0.6)",
        "text_main": "#3D2B1F",
        "text_sub": "#8C6D58",
        "highlight": "#B85B35",
        "palette": ["#D7BAA7", "#B85B35", "#8C6D58", "#E6C5B8", "#A3B18A", "#588157", "#D4A373", "#CCD5AE", "#E9EDC9", "#FAEDCD"]
    },
    "🌊 에메랄드 오션 (Emerald Ocean)": {
        "bg": "linear-gradient(135deg, #F0FDF4 0%, #E0F2FE 50%, #E0E7FF 100%)",
        "card_bg": "rgba(255, 255, 255, 0.8)",
        "card_border": "rgba(125, 211, 252, 0.6)",
        "text_main": "#0F172A",
        "text_sub": "#0284C7",
        "highlight": "#0D9488",
        "palette": ["#38BDF8", "#2DD4BF", "#34D399", "#818CF8", "#A78BFA", "#F472B6", "#FBBF24", "#67E8F9", "#6EE7B7", "#93C5FD"]
    }
}

# 사이드바 컨트롤러
st.sidebar.markdown("## 🎨 디자인 커스텀")

selected_font_name = st.sidebar.selectbox("🔤 폰트 스타일 선택", list(FONTS.keys()), index=0)
selected_theme_name = st.sidebar.selectbox("🌈 테마 분위기 선택", list(THEMES.keys()), index=0)

current_font = FONTS[selected_font_name]
current_theme = THEMES[selected_theme_name]
PASTEL_PALETTE = current_theme["palette"]

# 5. Dynamic CSS 적용 (글래스모피즘 + 폰트 + 애니메이션)
st.markdown(f"""
    <style>
    {current_font['import_url']}

    html, body, [class*="css"], .stMarkdown, .stButton button {{
        font-family: {current_font['family']} !important;
    }}

    /* 선택된 테마 배경 */
    .stApp {{
        background: {current_theme['bg']};
        transition: background 0.8s ease;
    }}

    /* 글래스모피즘 카드 & Floating 호버 애니메이션 */
    .graph-card {{
        background: {current_theme['card_bg']};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {current_theme['card_border']};
        border-radius: 28px;
        padding: 36px;
        box-shadow: 0 16px 40px 0 rgba(0, 0, 0, 0.04);
        margin-bottom: 35px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}

    .graph-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 24px 48px 0 rgba(0, 0, 0, 0.12);
        border-color: {current_theme['highlight']};
    }}

    /* 메인 타이틀 & 글자 색상 */
    .hero-banner {{
        text-align: center;
        padding: 40px 20px 20px 20px;
        margin-bottom: 30px;
    }}
    
    .hero-title {{
        font-size: 2.7rem;
        font-weight: 700;
        color: {current_theme['text_main']};
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }}
    
    .hero-desc {{
        color: {current_theme['text_sub']};
        font-size: 1.1rem;
    }}

    .section-title {{
        color: {current_theme['text_main']};
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 6px;
    }}
    
    .section-subtitle {{
        color: {current_theme['text_sub']};
        font-size: 0.95rem;
        margin-bottom: 22px;
    }}

    .insight-container {{
        background: rgba(255, 255, 255, 0.45);
        border-radius: 20px;
        border-left: 5px solid {current_theme['highlight']};
        padding: 20px 24px;
        margin-top: 24px;
        font-size: 0.98rem;
        color: {current_theme['text_main']};
        line-height: 1.6;
    }}
    
    .highlight {{
        color: {current_theme['highlight']};
        font-weight: 700;
    }}

    /* 랜덤 뽑기 감성 영화 카드 */
    .movie-poster-card {{
        background: linear-gradient(135deg, {current_theme['highlight']}18, rgba(255,255,255,0.75));
        border: 2px dashed {current_theme['highlight']};
        border-radius: 24px;
        padding: 28px;
        text-align: center;
        margin-top: 15px;
        animation: fadeIn 0.6s ease-in-out;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(12px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>
""", unsafe_allow_html=True)

# 6. 메인 타이틀 배너
st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title">🎬 영화 데이터 감성 도감</div>
        <div class="hero-desc">박스오피스 상위권 영화 216편의 프리미엄 아카이브</div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🎰 '오늘 뭐 볼까?' 랜덤 영화 뽑기 슬롯
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🎰 오늘 볼 영화 무작위 추천 슬롯</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>데이터 속 216편의 영화 중 한 편을 무작위로 추첨해 감성 카드로 보여줍니다</div>", unsafe_allow_html=True)
    
    col_btn, col_empty = st.columns([1, 3])
    with col_btn:
        pick_trigger = st.button("✨ 영화 추천 버튼 누르기", use_container_width=True)

    if pick_trigger:
        with st.spinner("🔮 우주가 당신에게 어울리는 영화를 점지하는 중..."):
            time.sleep(0.5)
            selected_movie = df.sample(1).iloc[0]
            
            audi = selected_movie['total_audi']
            if audi >= 10000000:
                badge = "👑 천만 관객 신화의 주인공"
            elif audi >= 5000000:
                badge = "🔥 폭발적 흥행 메가 히트작"
            elif audi >= 1000000:
                badge = "💎 입소문 자자한 인기 명작"
            else:
                badge = "🌱 알짜배기 매력 보유작"

            st.markdown(f"""
            <div class='movie-poster-card'>
                <span style='font-size: 0.88rem; background:{current_theme['highlight']}; color:white; padding:5px 14px; border-radius:14px; font-weight:600;'>{badge}</span>
                <h2 style='margin: 16px 0 8px 0; color:{current_theme['text_main']}; font-size: 1.8rem;'>{selected_movie['movieNm']}</h2>
                <p style='color:{current_theme['text_sub']}; font-size: 0.98rem; margin-bottom: 14px;'>
                    <b>장르:</b> {selected_movie['genre']} | <b>제작국가:</b> {selected_movie['nation']}
                </p>
                <div style='display:flex; justify-content:center; gap:24px; font-size:0.95rem; color:{current_theme['text_main']};'>
                    <div>🎟️ <b>총 관객수:</b> {selected_movie['total_audi']:,} 명</div>
                    <div>🖥️ <b>개봉 스크린:</b> {selected_movie['first_scrn']:,} 개</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Plotly 공통 폰트 및 스타일 헬퍼 함수
def apply_chart_style(fig):
    fig.update_layout(
        font=dict(family=current_font['family'].replace("'", ""), color=current_theme['text_main']),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

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
    fig1.update_layout(margin=dict(t=20, b=20))
    fig1 = apply_chart_style(fig1)
    
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown(f"""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것</b><br>
        박스오피스 주요 영화 중 <span class='highlight'>{genre_counts.iloc[0]['장르']}</span> 장르가 가장 높은 편수를 기록하고 있으며, 전체적인 장르 편중도를 확인할 수 있습니다.
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
        marker=dict(cornerradius=6)
    )
    fig2.update_layout(margin=dict(t=20, b=10, l=10, r=10))
    fig2 = apply_chart_style(fig2)
    
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것</b><br>
        각 장르의 파급력과 특정 장르 내에서 어떤 영화가 메가 히트를 기록하여 관객 비중을 이끌었는지 비교 분석할 수 있습니다.
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
        color_discrete_sequence=[PASTEL_PALETTE[1]]
    )
    fig3.update_traces(marker=dict(line=dict(width=1, color='white')))
    fig3.update_layout(
        bargap=0.1,
        xaxis=dict(title="총 관객수 (명)", color=current_theme['text_main']),
        yaxis=dict(title="영화 수 (편)", color=current_theme['text_main'])
    )
    fig3 = apply_chart_style(fig3)
    
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
        xaxis=dict(gridcolor='rgba(200, 200, 200, 0.2)', title="개봉일 스크린수 (개)", color=current_theme['text_main']),
        yaxis=dict(gridcolor='rgba(200, 200, 200, 0.2)', title="총 관객수 (명)", color=current_theme['text_main']),
        legend_title_text="장르"
    )
    fig4 = apply_chart_style(fig4)
    
    st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것</b><br>
        개봉일 스크린수를 많이 확보한 영화일수록 대체로 높은 총 관객수를 달성하는 양의 상관관계를 보이지만, 스크린수 대비 폭발적인 흥행 성과를 거둔 아웃라이어 영화도 찾아볼 수 있습니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# [그래프 5] 상자 그림(Box Plot) - 주요 장르별 관객수 분포
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>5. 주요 장르별 총 관객수 분포 비교 (상자 그림)</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>영화 수 10편 이상인 장르의 관객수 중앙값 및 이상치(Outlier) 확인</div>", unsafe_allow_html=True)
    
    genre_counts = df['genre'].value_counts()
    major_genres = genre_counts[genre_counts >= 10].index
    df_major = df[df['genre'].isin(major_genres)]
    
    fig5 = px.box(
        df_major,
        x='genre',
        y='total_audi',
        color='genre',
        hover_name='movieNm',
        points='outliers',
        labels={'genre': '장르', 'total_audi': '총 관객수'},
        color_discrete_sequence=PASTEL_PALETTE
    )
    fig5.update_traces(hovertemplate="<b>%{hovertext}</b><br>장르: %{x}<br>총 관객수: %{y:,}명")
    fig5.update_layout(
        xaxis=dict(gridcolor='rgba(200, 200, 200, 0.2)', title="주요 장르", color=current_theme['text_main']),
        yaxis=dict(gridcolor='rgba(200, 200, 200, 0.2)', title="총 관객수 (명)", color=current_theme['text_main']),
        showlegend=False
    )
    fig5 = apply_chart_style(fig5)
    
    st.plotly_chart(fig5, use_container_width=True)
    
    st.markdown("""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것</b><br>
        주요 장르별 관객수의 중앙값과 상하위 편차를 한눈에 파악할 수 있으며, 이상치 점을 통해 장르의 평균치를 훌쩍 뛰어넘은 대표 대흥행작을 식별할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# [그래프 6] 버블 차트 - 개봉일 스크린수 vs 총 관객수 (첫 주 관객수 크기)
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>6. 스크린수, 총 관객수, 첫 주 관객수의 입체적 분석 (버블 차트)</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>버블의 크기는 개봉 첫 주 관객수(first_week_audi)를 나타냅니다</div>", unsafe_allow_html=True)
    
    fig6 = px.scatter(
        df,
        x='first_scrn',
        y='total_audi',
        size='first_week_audi',
        color='genre',
        hover_name='movieNm',
        size_max=40,
        labels={'first_scrn': '개봉일 스크린수', 'total_audi': '총 관객수', 'first_week_audi': '첫 주 관객수', 'genre': '장르'},
        color_discrete_sequence=PASTEL_PALETTE
    )
    fig6.update_traces(
        marker=dict(opacity=0.75, line=dict(width=1, color='white')),
        hovertemplate="<b>%{hovertext}</b><br><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<br>첫 주 관객수: %{marker.size:,}명"
    )
    fig6.update_layout(
        xaxis=dict(gridcolor='rgba(200, 200, 200, 0.2)', title="개봉일 스크린수 (개)", color=current_theme['text_main']),
        yaxis=dict(gridcolor='rgba(200, 200, 200, 0.2)', title="총 관객수 (명)", color=current_theme['text_main']),
        legend_title_text="장르"
    )
    fig6 = apply_chart_style(fig6)
    
    st.plotly_chart(fig6, use_container_width=True)
    
    st.markdown("""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것</b><br>
        버블의 크기가 클수록 초반 흥행 동력이 강했음을 의미합니다. 개봉일 스크린수가 적었더라도 첫 주 관객수(버블 크기)가 커지며 입소문을 타고 최종 관객수가 급증한 모멘텀을 가진 영화를 발견할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# [그래프 7] 선버스트 차트 - 국가별 장르 분포 계층
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>7. 제작 국가 및 장르 계층 구조 (선버스트 차트)</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>안쪽 원(국가)에서 바깥쪽 원(장르)으로 이어지는 영화 편수 계층 구조</div>", unsafe_allow_html=True)
    
    fig7 = px.sunburst(
        df,
        path=['nation', 'genre'],
        color_discrete_sequence=PASTEL_PALETTE
    )
    fig7.update_traces(hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percentParent:.1%}")
    fig7.update_layout(margin=dict(t=10, l=10, r=10, b=10))
    fig7 = apply_chart_style(fig7)
    
    st.plotly_chart(fig7, use_container_width=True)
    
    st.markdown("""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것</b><br>
        국가별로 제작되거나 수입되는 주요 장르 구성의 차이를 확인할 수 있으며, 각 국가 내에서 특정 장르가 차지하는 비중을 한눈에 파악할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("데이터 출처: KOBIS 영화관 입장권 통합전산망")
