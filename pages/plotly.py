import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. 페이지 설정
st.set_page_config(
    page_title="글로벌 시가총액 TOP 10 주식 대시보드",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 글로벌 시가총액 TOP 10 주식 대시보드 (최근 1년)")
st.markdown("Streamlit과 Plotly를 활용하여 구성한 글로벌 TOP 10 기업의 최근 1년간 주가 변화 대시보드입니다.")

# 2. 글로벌 시가총액 TOP 10 기업 데이터 정의 (티커 기준)
# 2026년 상반기 기준 시가총액 상위 주요 기업 리스트
TOP10_COMPANIES = {
    "NVIDIA (NVDA)": "NVDA",
    "Alphabet (GOOGL)": "GOOGL",
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Amazon (AMZN)": "AMZN",
    "TSMC (TSM)": "TSM",
    "Broadcom (AVGO)": "AVGO",
    "Saudi Aramco (2222.SR)": "2222.SR",
    "Tesla (TSLA)": "TSLA",
    "Meta (META)": "META"
}

# 3. 사이드바 - 사용자 입력 제어
st.sidebar.header("⚙️ 설정 및 필터")

# 기업 선택 (다중 선택 가능, 기본값은 전체 선택)
selected_company_names = st.sidebar.multiselect(
    "시각화할 기업을 선택하세요:",
    options=list(TOP10_COMPANIES.keys()),
    default=list(TOP10_COMPANIES.keys())
)

# 데이터 비교 방식 선택 (절대 가격 vs 수익률 비교)
chart_type = st.sidebar.radio(
    "차트 표시 방식:",
    ("실제 주가 (USD/SAR)", "누적 수익률 (%)")
)

# 4. 데이터 로드 함수 (캐싱 적용으로 속도 향상)
@st.cache_data(ttl=3600)  # 1시간 동안 캐시 유지
def load_stock_data(tickers):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    
    data = pd.DataFrame()
    for name, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            # 최근 1년 종가 데이터 가져오기
            hist = stock.history(start=start_date, end=end_date)['Close']
            if not hist.empty:
                data[name] = hist
        except Exception as e:
            st.error(f"{name} ({ticker}) 데이터를 가져오는 중 오류 발생: {e}")
    
    # 날짜 포맷 변경 (시간 제외)
    data.index = data.index.date
    return data

# 선택된 기업의 티커 딕셔너리 생성
selected_tickers = {name: TOP10_COMPANIES[name] for name in selected_company_names}

if selected_tickers:
    with st.spinner("Yahoo Finance에서 주가 데이터를 가져오는 중..."):
        df = load_stock_data(selected_tickers)
    
    if not df.empty:
        # 5. Plotly를 이용한 시각화
        fig = go.Figure()
        
        for col in df.columns:
            if chart_type == "누적 수익률 (%)":
                # 첫 번째 거래일 기준 누적 수익률 계산
                initial_price = df[col].dropna().iloc[0]
                display_data = ((df[col] - initial_price) / initial_price) * 100
                yaxis_title = "누적 수익률 (%)"
                hovertemplate = "%{y:.2f}%"
            else:
                display_data = df[col]
                yaxis_title = "주가 (원래 통화 기준)"
                hovertemplate = "$%{y:.2f}" if "Aramco" not in col else "%{y:.2f} SAR"
            
            fig.add_trace(go.Scatter(
                x=df.index,
                y=display_data,
                mode='lines',
                name=col,
                hovertemplate=f"<b>{col}</b><br>날짜: %{{x}}<br>{yaxis_title}: {hovertemplate}<extra></extra>"
            ))
            
        fig.update_layout(
            title=f"글로벌 TOP 10 기업 주가 추이 ({chart_type})",
            xaxis_title="날짜",
            yaxis_title=yaxis_title,
            hovermode="x unified",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=60, b=20),
            height=600
        )
        
        # Streamlit 화면에 차트 출력
        st.plotly_chart(fig, use_container_width=True)
        
        # 6. 최근 데이터 테이블 및 통계 요약
        st.subheader("📋 최근 주가 요약 데이터")
        
        # 최신 주가와 1년 전 대비 등락률을 요약 데이터프레임으로 표현
        summary_list = []
        for col in df.columns:
            valid_series = df[col].dropna()
            if not valid_series.empty:
                first_p = valid_series.iloc[0]
                last_p = valid_series.iloc[-1]
                pct_change = ((last_p - first_p) / first_p) * 100
                summary_list.append({
                    "기업명": col,
                    "1년 전 주가": round(first_p, 2),
                    "최근 종가": round(last_p, 2),
                    "1년간 등락률": f"{pct_change:+.2f}%"
                })
        
        summary_df = pd.DataFrame(summary_list)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
    else:
        st.warning("가져온 데이터가 없습니다. 선택한 기업을 다시 확인해 주세요.")
else:
    st.info("💡 왼쪽 사이드바에서 시각화할 기업을 최소 하나 이상 선택해 주세요.")
