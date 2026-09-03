# ---------------------------------------------------------
# [그래프 8] 수평 막대 차트 - 장르별 평균 관객수 순위
# ---------------------------------------------------------
with st.container():
    st.markdown("<div class='graph-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>8. 장르별 평균 관객 동원력 (수평 막대 차트)</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>영화 1편당 기대할 수 있는 평균 관객수를 장르별로 비교합니다</div>", unsafe_allow_html=True)
    
    # 장르별 평균 관객수 계산 및 상위 10개 정렬
    genre_avg = df.groupby('genre')['total_audi'].mean().reset_index()
    genre_avg = genre_avg.sort_values(by='total_audi', ascending=True).tail(10)
    
    fig8 = px.bar(
        genre_avg,
        x='total_audi',
        y='genre',
        orientation='h',
        text_auto='.2s',
        labels={'total_audi': '평균 관객수', 'genre': '장르'},
        color_discrete_sequence=[PASTEL_PALETTE[0]]
    )
    fig8.update_traces(
        marker=dict(cornerradius=8),
        hovertemplate="<b>장르:</b> %{y}<br><b>평균 관객수:</b> %{x:,.0f}명"
    )
    fig8.update_layout(
        xaxis=dict(gridcolor='rgba(200, 200, 200, 0.2)', title="평균 관객수 (명)", color=current_theme['text_main']),
        yaxis=dict(title="장르", color=current_theme['text_main'])
    )
    fig8 = apply_chart_style(fig8)
    
    st.plotly_chart(fig8, use_container_width=True)
    
    top_genre = genre_avg.iloc[-1]
    st.markdown(f"""
    <div class='insight-container'>
        <b>💡 이 그래프로 알 수 있는 것</b><br>
        단순 전체 편수가 아닌, 작품 1편당 파급력이 가장 높은 장르는 <span class='highlight'>{top_genre['genre']}</span>(평균 약 {top_genre['total_audi']/10000:.0f}만 명)임을 확인할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
