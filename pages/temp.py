import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# 1. 페이지 기본 설정 및 스타일 지정
st.set_page_config(
    page_title="서울 기온 타임머신 아카이브",
    page_icon="🌡️",
    layout="wide"
)

# 2. 데이터 캐싱 및 전처리 함수 정의
@st.cache_data
def load_and_preprocess_data(file_path):
    # utf-8 인코딩으로 데이터 로드
    df = pd.read_csv(file_path, encoding='utf-8')
    
    # '날짜' 컬럼 문자열 공백 및 탭 기호('\t') 제거
    df['날짜'] = df['날짜'].astype(str).str.strip()
    
    # 날짜 데이터 변환 (파싱 에러 발생 시 NaT로 처리)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 날짜가 결측치인 행 제거
    df = df.dropna(subset=['날짜'])
    
    # 분석에 필요한 월, 일, 연도 파생 변수 추가
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

# 3. 상단 타이틀 및 설명문
st.title("🌡️ 서울 기온 타임머신 아카이브 (1907 ~ 2026)")
st.markdown("""
이 웹 애플리케이션은 **1907년부터 2026년까지 약 120년간의 서울 기온 역사 데이터**를 기반으로 만들어졌습니다.
과거 속 내가 태어난 날의 날씨를 확인하거나, 매년 반복되는 나만의 특별한 기념일 기온이 어떻게 변화해 왔는지 타임머신을 타고 확인해 보세요!
""")
st.write("---")

# 4. 탭 구성을 활용한 레이아웃 분리
tab1, tab2 = st.tabs(["📅 나의 특별한 날 타임머신", "📈 내 기념일의 120년 역사 추이"])

# ==============================================================================
# Tab 1: 나의 특별한 날 타임머신
# ==============================================================================
with tab1:
    st.header("📅 내가 태어난 날 혹은 특별한 기념일의 날씨는?")
    st.write("원하는 날짜를 지정하면 역사 속 그날의 정확한 기온과 데이터 기반 스토리텔링을 제공합니다.")
    
    # 입력 날짜 제한 설정
    min_date = datetime.date(1907, 10, 1)
    max_date = datetime.date(2026, 6, 18)
    
    # 사용자 날짜 입력받기
    selected_date = st.date_input(
        "날짜를 선택하세요 (1907년 10월 1일 ~ 2026년 6월 18일)",
        value=datetime.date(2000, 1, 1),
        min_value=min_date,
        max_value=max_date
    )
    
    # 선택된 날짜 데이터 필터링
    target_date = pd.to_datetime(selected_date)
    day_info = data[data['날짜'] == target_date]
    
    if not day_info.empty and not day_info[['평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].isna().all().all():
        row = day_info.iloc[0]
        avg_temp = row['평균기온(℃)']
        min_temp = row['최저기온(℃)']
        max_temp = row['최고기온(℃)']
        
        # 기온 카드 대시보드 시각화
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="최저 기온", value=f"{min_temp} ℃" if not pd.isna(min_temp) else "데이터 없음")
        with col2:
            st.metric(label="평균 기온", value=f"{avg_temp} ℃" if not pd.isna(avg_temp) else "데이터 없음")
        with col3:
            st.metric(label="최고 기온", value=f"{max_temp} ℃" if not pd.isna(max_temp) else "데이터 없음")
            
        # 백분위 스토리텔링 계산 (전체 기간 대비 해당 날짜의 평균기온 위치 계산)
        if not pd.isna(avg_temp):
            valid_avg_temps = data['평균기온(℃)'].dropna().sort_values().reset_index(drop=True)
            # 해당 기온보다 낮거나 같은 날의 비율 계산
            rank_idx = valid_avg_temps.searchsorted(avg_temp)
            percentile_cool = (rank_idx / len(valid_avg_temps)) * 100
            percentile_warm = 100 - percentile_cool
            
            st.subheader("📝 기상 기록 분석 레포트")
            if percentile_warm <= 10:
                story_text = f"선택하신 날의 평균 기온({avg_temp}℃)은 서울 기상 관측 사상 **상위 {percentile_warm:.1f}%** 내에 드는 **매우 무덥고 따뜻한 날**이었습니다! 🔥"
            elif percentile_cool <= 10:
                story_text = f"선택하신 날의 평균 기온({avg_temp}℃)은 서울 기상 관측 사상 **하위 {percentile_cool:.1f}%** 내에 드는 **매우 혹독하고 추운 날**이었습니다! ❄️"
            else:
                story_text = f"선택하신 날의 평균 기온({avg_temp}℃)은 서울 기상 사상 **약 상위 {percentile_warm:.1f}%** 지점에 위치하는 비교적 **평온하고 평범한 기후의 날**이었습니다. 😊"
                
            st.info(story_text)
    else:
        st.warning("⚠️ 선택하신 날짜는 역사적 사건(예: 한국전쟁 시기) 또는 기상관측소 사정으로 기온 기록이 누락되어 있습니다. 다른 날짜를 선택해 주세요.")


# ==============================================================================
# Tab 2: 내 기념일의 120년 역사 추이
# ==============================================================================
with tab2:
    st.header("📈 내 기념일의 120년 기온 변화 추이")
    st.write("연도를 제외한 '월'과 '일'을 지정하여 1907년부터 현재까지 서울의 기온 변화 추세와 극값을 확인합니다.")
    
    col_m, col_d = st.columns(2)
    with col_m:
        month_list = list(range(1, 13))
        selected_month = st.selectbox("월을 선택하세요", month_list, index=4)  # 기본값 5월
    with col_d:
        day_list = list(range(1, 32))
        selected_day = st.selectbox("일을 선택하세요", day_list, index=4)      # 기본값 5일
        
    # 특정 월/일 데이터 필터링 후 정렬
    anniversary_df = data[(data['월'] == selected_month) & (data['일'] == selected_day)].sort_values('연도')
    
    # 데이터가 아예 없는 경우 방어 처리 (예: 2월 30일 등 유효하지 않은 날짜 방지)
    if anniversary_df.empty:
        st.error("❌ 입력하신 날짜(월/일)가 달력에 존재하지 않거나 데이터가 없습니다. 유효한 날짜를 조합해 주세요.")
    else:
        st.subheader(f"📊 {selected_month}월 {selected_day}일 기온 타임라인 차트")
        
        # 선 그래프 시각화용 데이터 정제 (결측 데이터 드롭)
        chart_df = anniversary_df.dropna(subset=['평균기온(℃)', '최저기온(℃)', '최고기온(℃)'])
        
        if not chart_df.empty:
            # 최고기온, 최저기온 시각화 및 평균기온 기준 투명한 OLS 추세선(trendline) 추가
            fig = px.line(
                chart_df, 
                x='연도', 
                y=['최저기온(℃)', '최고기온(℃)'],
                labels={'value': '기온 (℃)', 'variable': '구분'},
                title=f"1907 ~ 2026년 서울의 {selected_month}월 {selected_day}일 기온 변화 추이",
                hover_data={'연도': True, 'value': ':.1f'}
            )
            
            # 평균 기온 추세선 분석을 위한 Plotly Express 임시 그래프 생성 후 추세선만 추출하여 기존 그래프에 병합
            fig_trend = px.scatter(chart_df, x='연도', y='평균기온(℃)', trendline="ols")
            trendline = fig_trend.data[1]
            
            # 추세선 디자인 요구사항 반영: '평균기온 추세선' 명명 및 반투명(투명도 0.4) 투입
            trendline.name = "평균기온 장기 추세선"
            trendline.line.dash = "dash"
            trendline.line.color = "rgba(128, 128, 128, 0.5)"
            fig.add_trace(trendline)
            
            # 차트 레이아웃 레이블 커스텀화
            fig.update_layout(
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 통계 요약 및 최고/최저 기온 기록 찾기
            max_row = chart_df.loc[chart_df['최고기온(℃)'].idxmax()]
            min_row = chart_df.loc[chart_df['최저기온(℃)'].idxmin()]
            
            st.subheader(f"🏅 역사 속 {selected_month}월 {selected_day}일의 기온 기록관")
            sum_col1, sum_col2 = st.columns(2)
            
            with sum_col1:
                st.info(f"☀️ **가장 무더웠던 해 ({max_row['연도']}년)**\n\n"
                        f"- 최고 기온: **{max_row['최고기온(℃)']} ℃**\n"
                        f"- 당해 평균 기온: {max_row['평균기온(℃)']} ℃")
            with sum_col2:
                st.beta_container if hasattr(st, 'beta_container') else st.container()
                st.success(f"❄️ **가장 추웠던 해 ({min_row['연도']}년)**\n\n"
                           f"- 최저 기온: **{min_row['최저기온(℃)']} ℃**\n"
                           f"- 당해 평균 기온: {min_row['평균기온(℃)']} ℃")
        else:
            st.warning("선택하신 기념일 날짜에 온전한 기온 시각화 데이터가 부족합니다.")
