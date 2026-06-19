import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="서울 기온 타임머신 아카이브",
    page_icon="🌤️",
    layout="wide"
)

# 2. 화창하고 세련된 기상청 감성 CSS 주입 (폰트, 색상, 그림자 및 효과)
st.markdown("""
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
    <style>
        /* 전체 기본 폰트 설정 */
        html, body, [class*="css"], .stMarkdown {
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, thon, sans-serif !important;
        }
        
        #root > div:nth-child(1) > div:nth-child(1) > div > div {
            background-color: #f7faff; /* 아주 연한 청량한 하늘빛 배경 */
        }
        
        /* 메인 타이틀 스타일 꾸미기 */
        .main-title {
            font-size: 2.6rem !important;
            font-weight: 800 !important;
            color: #2b5c8f !important; /* 기상청 느낌의 차분한 네이비 블루 */
            margin-bottom: 5px !important;
            letter-spacing: -0.05rem;
        }
        
        /* 서브 텍스트 스타일 */
        .sub-title {
            color: #5a738e !important;
            font-size: 1.1rem !important;
            margin-bottom: 25px !important;
        }
        
        /* 대시보드 카드(st.metric) 상자 예쁘게 꾸미기 */
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #384d6b !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: #7b93b0 !important;
        }
        
        /* Metric 카드를 감싸는 부모 컨테이너에 부드러운 흰색 카드 효과 부여 */
        div[data-testid="metric-container"] {
            background-color: #ffffff;
            border: 1px solid #e3edf7;
            padding: 15px 20px !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 12px rgba(43, 92, 143, 0.04) !important;
            transition: all 0.3s ease-in-out !important;
        }
        
        /* 마우스를 올렸을 때 화창하게 떠오르는 효과 (Hover Effect) */
        div[data-testid="metric-container"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 20px rgba(43, 92, 143, 0.08) !important;
            border-color: #bcd4ec;
        }
        
        /* 탭 스타일 고급화 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 45px;
            white-space: pre;
            background-color: #eef4fc;
            border-radius: 10px 10px 0px 0px;
            color: #5a738e;
            font-weight: 600;
            padding: 0px 20px;
            border: none;
            transition: all 0.2s;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #e2edf9;
            color: #2b5c8f;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            color: #2b5c8f !important;
            font-weight: 700 !important;
            border-top: 3px solid #5fa4e6 !important;
            box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.02);
        }
        
        /* 알림창(st.info, st.success) 라운드 처리 */
        .stAlert {
            border-radius: 14px !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.02) !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 캐싱 및 전처리 함수
@st.cache_data
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    df['날짜'] = df['날짜'].astype(str).str.strip()
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    df = df.dropna(subset=['날짜'])
    
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    return df

# 데이터 로드
csv_filename = "ta_20260619190504.csv"
try:
    data = load_and_preprocess_data(csv_filename)
except Exception as e:
    st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 4. 상단 타이틀 부문 (HTML로 주입하여 CSS 디자인 적용)
st.markdown('<p class="main-title">🌤️ 서울 기온 타임머신 아카이브</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">1907년부터 2026년까지, 120년 서울의 푸른 기상 역사를 탐독합니다.</p>', unsafe_allow_html=True)

# 5. 탭 구성
tab1, tab2 = st.tabs(["📅 나의 특별한 날 타임머신", "📈 내 기념일의 120년 역사 추이"])

# ==============================================================================
# Tab 1: 나의 특별한 날 타임머신
# ==============================================================================
with tab1:
    st.markdown("<h3 style='color:#384d6b; font-size:1.4rem; font-weight:700; margin-bottom:10px;'>📅 역사 속 그날의 날씨는 어땠을까요?</h3>", unsafe_allow_html=True)
    
    min_date = datetime.date(1907, 10, 1)
    max_date = datetime.date(2026, 6, 18)
    
    selected_date = st.date_input(
        "조회할 날짜를 선택해 주세요",
        value=datetime.date(2000, 1, 1),
        min_value=min_date,
        max_value=max_date
    )
    
    target_date = pd.to_datetime(selected_date)
    day_info = data[data['날짜'] == target_date]
    
    if not day_info.empty and not day_info[['평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].isna().all().all():
        row = day_info.iloc[0]
        avg_temp = row['평균기온(℃)']
        min_temp = row['최저기온(℃)']
        max_temp = row['최고기온(℃)']
        
        st.write("")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="📉 최저 기온", value=f"{min_temp} ℃" if not pd.isna(min_temp) else "데이터 없음")
        with col2:
            st.metric(label="🌡️ 평균 기온", value=f"{avg_temp} ℃" if not pd.isna(avg_temp) else "데이터 없음")
        with col3:
            st.metric(label="  최고 기온", value=f"{max_temp} ℃" if not pd.isna(max_temp) else "데이터 없음")
            
        if not pd.isna(avg_temp):
            valid_avg_temps = data['평균기온(℃)'].dropna().sort_values().reset_index(drop=True)
            rank_idx = valid_avg_temps.searchsorted(avg_temp)
            percentile_cool = (rank_idx / len(valid_avg_temps)) * 100
            percentile_warm = 100 - percentile_cool
            
            st.markdown("<h4 style='color:#384d6b; font-size:1.15rem; font-weight:700; margin-top:25px;'>📝 기상 분석 스토리</h4>", unsafe_allow_html=True)
            if percentile_warm <= 10:
                story_text = f"선택하신 날의 평균 기온({avg_temp}℃)은 서울 기상 관측 사상 **상위 {percentile_warm:.1f}%** 내에 드는 **매우 따뜻하고 열정적인 날**이었습니다! 🔥"
            elif percentile_cool <= 10:
                story_text = f"선택하신 날의 평균 기온({avg_temp}℃)은 서울 기상 관측 사상 **하위 {percentile_cool:.1f}%** 내에 드는 **손이 꽁꽁 얼어붙을 만큼 추운 날**이었습니다! ❄️"
            else:
                story_text = f"선택하신 날의 평균 기온({avg_temp}℃)은 서울 기상 사상 **약 상위 {percentile_warm:.1f}%** 지점에 위치하며, 아주 **포근하고 화창한 기후의 평범한 날**이었습니다. 🌱"
                
            st.info(story_text)
    else:
        st.warning("⚠️ 선택하신 날짜는 누락 기간입니다. 다른 날짜를 선택해 주세요.")

# ==============================================================================
# Tab 2: 내 기념일의 120년 역사 추이
# ==============================================================================
with tab2:
    st.markdown("<h3 style='color:#384d6b; font-size:1.4rem; font-weight:700; margin-bottom:10px;'>📈 매년 돌아오는 나만의 기념일 기온 흐름</h3>", unsafe_allow_html=True)
    
    col_m, col_d = st.columns(2)
    with col_m:
        selected_month = st.selectbox("월 선택", list(range(1, 13)), index=4) # 5월 기본
    with col_d:
        selected_day = st.selectbox("일 선택", list(range(1, 31)), index=4) # 5일 기본
        
    anniversary_df = data[(data['월'] == selected_month) & (data['일'] == selected_day)].sort_values('연도')
    
    if anniversary_df.empty:
        st.error("❌ 유효한 달력 날짜를 조합해 주세요.")
    else:
        chart_df = anniversary_df.dropna(subset=['평균기온(℃)', '최저기온(℃)', '최고기온(℃)'])
        
        if not chart_df.empty:
            # 화창한 느낌의 파스텔 블루 테마로 차트 컬러 매칭 (#79a6d2: 최저기온, #ff9e80: 최고기온)
            fig = px.line(
                chart_df, 
                x='연度' if '연度' in chart_df.columns else '연도', 
                y=['최저기온(℃)', '최고기온(℃)'],
                labels={'value': '기온 (℃)', 'variable': '구분'},
                color_discrete_sequence=['#79a6d2', '#ff9e80'],
                hover_data={'연도': True, 'value': ':.1f'}
            )
            
            # 추세선 추가
            fig_trend = px.scatter(chart_df, x='연도', y='평균기온(℃)', trendline="ols")
            trendline = fig_trend.data[1]
            trendline.name = "백개년 평균기온 추세선"
            trendline.line.dash = "dot"
            trendline.line.color = "rgba(43, 92, 143, 0.4)" # 연한 블루그레이 투명 추세선
            fig.add_trace(trendline)
            
            # 차트 내부 스타일도 깔끔하게 커스텀
            fig.update_layout(
                plot_bgcolor='rgba(255,255,255,0.6)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(showgrid=True, gridcolor='#eef4fc'),
                yaxis=dict(showgrid=True, gridcolor='#eef4fc')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 극값 요약 아카이브
            max_row = chart_df.loc[chart_df['최고기온(℃)'].idxmax()]
            min_row = chart_df.loc[chart_df['최저기온(℃)'].idxmin()]
            
            st.markdown(f"<h4 style='color:#384d6b; font-size:1.15rem; font-weight:700; margin-top:15px;'>🏅 역사 속 {selected_month}월 {selected_day}일의 특별한 기동 기록</h4>", unsafe_allow_html=True)
            sum_col1, sum_col2 = st.columns(2)
            
            with sum_col1:
                st.info(f"☀️ **가장 따뜻했던 해 ({max_row['연도']}년)**\n\n"
                        f"- 최고 기온: **{max_row['최고기온(℃)']} ℃**\n"
                        f"- 평균 기온: {max_row['평균기온(℃)']} ℃")
            with sum_col2:
                st.success(f"❄️ **가장 선선했던 해 ({min_row['연도']}년)**\n\n"
                           f"- 최저 기온: **{min_row['최저기온(℃)']} ℃**\n"
                           f"- 평균 기온: {min_row['평균기온(℃)']} ℃")
