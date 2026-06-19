import streamlit as pd
import streamlit as st

# 1. 페이지 기본 설정 (가장 위에 위치해야 합니다!)
st.set_page_config(
    page_title="🌟몽글몽글 MBTI 진로 탐험대🌟",
    page_icon="🚀",
    layout="centered",
)

# 2. 귀여운 커스텀 CSS 스타일 적용 (화려하고 아기자기한 느낌)
st.markdown(
    """
    <style>
    .main {
        background-color: #F9F7F7;
    }
    h1 {
        color: #FF6B6B;
        text-align: center;
        font-family: 'Comic Sans MS', sans-serif;
    }
    .sub-title {
        text-align: center;
        color: #4EA8DE;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .mbti-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(255, 107, 107, 0.2);
        border: 2px solid #FFD166;
    }
    .job-card {
        background: linear-gradient(135deg, #FFEEF0 0%, #E8F0FE 100%);
        padding: 15px;
        border-radius: 12px;
        margin-top: 10px;
        border-left: 5px solid #FF6B6B;
    }
    </style>
    """,
    unsafe_allow_index=True,
)

# 3. MBTI별 진로 데이터 (학생 맞춤형)
mbti_jobs = {
    "ISTJ": {
        "title": "🧐 신중하고 완벽한 '소금형' 탐험가",
        "jobs": ["📈 데이터 분석가", "⚖️ 회계사 및 변리사", "💻 백엔드 개발자", "🕵️‍♂️ 과학 수사관"],
        "desc": "꼼꼼함과 책임감이 최고의 무기! 규칙이 명확하고 정확성을 요구하는 일에서 빛을 발해요. 💎",
    },
    "ISFJ": {
        "title": "💖 따뜻하고 헌신적인 '수호자' 탐험가",
        "jobs": ["👩‍⚕️ 간호사 및 의료인", "🏫 초등/유치원 교사", "🎨 사회복지사", "큐레이터"],
        "desc": "타인을 돕고 서포트하는 일에서 가장 큰 보람을 느껴요. 다정하고 섬세한 손길이 필요해요! 🧸",
    },
    "INFJ": {
        "title": "🔮 통찰력 넘치는 '예언자' 탐험가",
        "jobs": ["🧠 심리상담사", "✍️ 소설가/시인", "🌱 환경운동가", "🎓 교육학 연구원"],
        "desc": "사람의 마음을 읽는 눈을 가졌어요! 깊은 통찰력으로 세상에 긍정적인 변화를 주는 일에 어울려요. 🌈",
    },
    "INTJ": {
        "title": "🦅 전략을 세우는 '과학자' 탐험가",
        "jobs": ["🤖 AI 연구원", "📊 경영 전략 컨설턴트", "🚀 우주공학자", "♟️ 게임 기획자"],
        "desc": "복잡한 문제를 해결하는 천재적 두뇌! 거대한 시스템을 설계하고 미래를 예측하는 일에 강해요. ⚡",
    },
    "ISTP": {
        "title": "🛠️ 못하는 게 없는 '만능재주꾼' 탐험가",
        "jobs": ["🏎️ 카레이서", "🛠️ 엔지니어", "✈️ 항공기 조종사", "🎮 프로게이머"],
        "desc": "손재주가 좋고 상황 적응력이 최고! 직접 몸으로 부딪히고 도구를 다루는 짜릿한 직업이 딱이에요. ⚙️",
    },
    "ISFP": {
        "title": "🎨 감성이 흐르는 '예술가' 탐험가",
        "jobs": ["🎨 일러스트레이터", "🎵 작곡가/뮤지션", "💐 플로리스트", "🐾 동물 사육사"],
        "desc": "미적 감각과 따뜻한 감수성을 겸비했어요! 자유로운 분위기에서 나만의 예술을 펼쳐보세요. 🌸",
    },
    "INFP": {
        "title": "🦄 이상을 꿈꾸는 '잔다르크' 탐험가",
        "jobs": ["🎬 영화 감독", "🎨 웹툰 작가", "💌 카피라이터", " NGO 활동가"],
        "desc": "마음속에 나만의 아름다운 세계를 품고 있어요. 가치 있는 일이나 창작 활동에서 큰 에너지를 얻어요. ✨",
    },
    "INTP": {
        "title": "🧐 세상의 비밀을 푸는 '아이디어맨' 탐험가",
        "jobs": ["🧬 과학 연구원", "💻 소프트웨어 아키텍트", "🔍 경제학자", "🔮 철학가"],
        "desc": "끊임없이 '왜?'라는 질문을 던지는 호기심 천국! 독창적인 이론을 정립하거나 연구하는 일이 잘 맞아요. 🌌",
    },
    "ESTP": {
        "title": "🔥 에너지가 넘치는 '활동가' 탐험가",
        "jobs": ["🚒 소방관/경찰관", "💼 스타트업 창업가", "🎤 스포츠 캐스터", "📈 주식 트레이더"],
        "desc": "위험을 두려워하지 않는 용감한 심장! 스릴 있고 다이내믹하게 현장을 누비는 직업이 최고예요. ⚡",
    },
    "ESFP": {
        "title": "🎉 분위기 메이커 '연예인' 탐험가",
        "jobs": ["🕺 뮤지컬 배우", "📹 크리에이터(유튜버)", "🎈 이벤트 기획자", "✈️ 승무원"],
        "desc": "어디서나 스포트라이트를 받는 주인공! 사람들에게 즐거움과 행복을 주는 직업이 천직이에요. 🎈",
    },
    "ENFP": {
        "title": "🦋 통통 튀는 스파크 '활동가' 탐험가",
        "jobs": ["🎨 광고 기획자(AE)", "🎙️ 레크리에이션 강사", "🎭 연극배우", "🌍 여행 작가"],
        "desc": "지치지 않는 열정과 무한 긍정 에너지! 새로운 사람을 만나고 아이디어를 내는 일에서 날아올라요. 🧚",
    },
    "ENTP": {
        "title": "💡 세상을 뒤흔드는 '발명가' 탐험가",
        "jobs": ["💼 벤처 캐피탈리스트", "🗣️ 정치가/토론가", "🎮 게임 디렉터", "🧠 빅데이터 전문가"],
        "desc": "틀에 박힌 규칙은 거부한다! 신선한 아이디어로 새로운 패러다임을 만드는 혁신가 타입이에요. 🚀",
    },
    "ESTJ": {
        "title": "👑 완벽한 리더 '지휘관' 탐험가",
        "jobs": ["🏢 대기업 관리자", "💼 프로젝트 매니저(PM)", "👨‍기자", "🏛️ 공무원"],
        "desc": "체계적이고 조직적인 관리 능력의 끝판왕! 목표를 향해 사람들을 이끌고 결과를 만들어내는 데 탁월해요. 🏆",
    },
    "ESFJ": {
        "title": "🤝 모두에게 사랑받는 '마당발' 탐험가",
        "jobs": ["🏫 교사/상담사", "🏨 호텔리어", "🤝 인사(HR) 담당자", " PR 전문가"],
        "desc": "공감 능력 만렙! 주변 사람들을 챙기고 조화로운 환경을 만드는 커뮤니티의 중심 리더예요. 💌",
    },
    "ENFJ": {
        "title": "☀️ 정의로운 아이돌 '지도자' 탐험가",
        "jobs": ["🗣️ 아나운서/앵커", "🏛️ 정치/사회운동가", "🧑‍🏫 청소년 지도사", "🏢 외교관"],
        "desc": "사람들을 매료시키는 선한 영향력! 더 나은 세상을 위해 사람들을 이끌고 변화를 주도해요. ☀️",
    },
    "ENTJ": {
        "title": "🦁 거침없는 카리스마 'CEO' 탐험가",
        "jobs": ["👔 기업 CEO", "📊 경영 컨설턴트", "⚖️ 판사/검사", "🏗️ 투자 분석가"],
        "desc": "철저한 계획과 강력한 실행력! 높은 목표를 세우고 조직을 승리로 이끄는 타고난 대장이에요. 🦁",
    },
}

# 4. 메인 화면 구성
st.markdown("<h1>🌟 몽글몽글 MBTI 진로 탐험대 🌟</h1>", unsafe_allow_index=True)
st.markdown(
    "<div class='sub-title'>나의 MBTI를 선택하고 미래의 멋진 내 직업을 찾아 떠나볼까요? 🚀✨</div>",
    unsafe_allow_index=True,
)

# 풍선 효과로 화려하게 시작!
st.balloons()

# 5. 입력 섹션
st.markdown("### 🦄 나의 MBTI는 무엇인가요?")
col1, col2, col3, col4 = st.columns(4)

with col1:
    e_i = st.radio("⚡ 에너지", ["E (외향형) 😎", "I (내향형) 🧠"])
with col2:
    n_s = st.radio("🔮 인식", ["N (직관형) 💭", "S (감각형) 🎯"])
with col3:
    t_f = st.radio("⚖️ 판단", ["T (사고형) 🤖", "F (감정형) 💖"])
with col4:
    j_p = st.radio("📅 생활", ["J (계획형) 📅", "P (자율형) 🎲"])

# 선택된 MBTI 문자열 조합
selected_mbti = e_i[0] + n_s[0] + t_f[0] + j_p[0]

st.write("---")

# 6. 결과 출력 섹션
if selected_mbti in mbti_jobs:
    info = mbti_jobs[selected_mbti]

    # 귀여운 헤더 출력
    st.markdown(
        f"### 🎉 탐색 완료! 당신은 **{selected_mbti}** 타입이군요!"
    )
    st.success(f"**{info['title']}**")

    # 설명 레이아웃
    st.markdown(
        f"""
        <div class='mbti-box'>
            <p style='font-size: 1.1rem; line-height: 1.6;'>{info['desc']}</p>
        </div>
        """,
        unsafe_allow_index=True,
    )

    st.write("")
    st.markdown("#### 🛠️ 추천하는 찰떡궁합 직업군 LIST")

    # 추천 직업 리스트를 카드로 예쁘게 출력
    for job in info["jobs"]:
        st.markdown(
            f"""
            <div class='job-card'>
                <span style='font-size: 1.2rem; font-weight: bold;'>{job}</span>
            </div>
            """,
            unsafe_allow_index=True,
        )

    # 추가 축하 효과!
    st.snow()

# 7. 푸터 (Footer)
st.write("---")
st.markdown(
    "<p style='text-align: center; color: #aaa; font-size: 0.8rem;'>🎈 멋진 미래의 주인공은 바로 당신! 꿈을 향해 나아가세요 🎈</p>",
    unsafe_allow_index=True,
)
