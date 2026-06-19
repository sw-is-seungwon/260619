import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="🌸 봄날의 진로 탐험 🌸",
    page_icon="🌱",
    layout="centered",
)

# 2. 봄 느낌 파스텔 CSS 스타일
st.html(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poor+Story&display=swap');

    .stApp {
        background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%);
        font-family: 'Poor Story', cursive;
    }
    .main-title {
        color: #FF8E9E;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.5);
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #77A605;
        font-size: 1.3rem;
        margin-bottom: 30px;
    }
    .mbti-result-card {
        background-color: rgba(255, 255, 255, 0.75);
        padding: 25px;
        border-radius: 20px;
        border: 2px dashed #FFB7B2;
        margin-bottom: 25px;
        color: #444;
    }
    .tag {
        display: inline-block;
        background-color: #E8F0FE;
        color: #1A73E8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.95rem;
        margin-right: 6px;
        font-weight: bold;
        border: 1px solid #D2E3FC;
    }
    /* 더 예뻐진 방명록 메모 카드 스타일 */
    .memo-card {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 12px;
        border-left: 5px solid #FF8E9E;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
    }
    .memo-header {
        font-size: 1.05rem;
        color: #444;
        margin-bottom: 8px;
    }
    .memo-badge {
        background-color: #FFF0F2;
        color: #FF6B6B;
        padding: 2px 8px;
        border-radius: 5px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .memo-content {
        font-size: 1rem;
        color: #333;
        line-height: 1.5;
    }
    </style>
    """
)

# 💾 실시간 공용 메모 저장소 데이터 구조 업데이트
if "shared_memos" not in st.session_state:
    st.session_state["shared_memos"] = [
        {
            "nickname": "체리블라썸 🌸", 
            "mbti": "ENFP", 
            "fav_job": "🎨 광고 기획자", 
            "real_dream": "웹툰 작가 ✍️", 
            "text": "광고 기획도 제 아이디어를 쓸 수 있어서 재밌을 것 같아요!"
        },
        {
            "nickname": "코딩하는 새싹 🌱", 
            "mbti": "INTJ", 
            "fav_job": "🤖 AI 연구원", 
            "real_dream": "화이트해커 💻", 
            "text": "AI 연구원 설명 보니까 관련 학과인 컴퓨터공학과로 진학하고 싶어졌어요."
        }
    ]

# 3. MBTI별 상세 직업 데이터
mbti_info = {
    "ISTJ": {
        "title": "⚖️ 신중하고 완벽한 탐험가",
        "tags": ["#책임감", "#정확성", "#신뢰주의", "#꼼꼼함"],
        "desc": "한 번 시작한 일은 끝까지 완수하는 책임감의 대명사! 질서 정연한 환경에서 빛이 나요.",
        "jobs": {
            "📈 데이터 분석가": {"info": "수치를 통해 세상을 해석하고 예측하는 전문가", "majors": "통계학과, 경영학과, 수학과"},
            "⚖️ 변리사": {"info": "아이디어와 기술의 권리를 보호하는 법률 전문가", "majors": "법학과, 공학계열"},
            "🕵️ 과학 수사관": {"info": "현장의 증거를 과학적으로 분석하여 진실을 밝히는 직업", "majors": "경찰행정학과, 화학과, 생명공학과"}
        }
    },
    "ISFJ": {
        "title": "💖 다정하고 헌신적인 수호자",
        "tags": ["#세심함", "#이타심", "#따뜻함", "#서포터"],
        "desc": "주변 사람들을 세심하게 살피고 돕는 따뜻한 마음을 가졌어요. 안정감 있는 지원이 특기!",
        "jobs": {
            "👩‍⚕️ 간호사": {"info": "환자의 곁에서 건강 회복을 돕는 숭고한 직업", "majors": "간호학과"},
            "🏫 초등교사": {"info": "어린이들의 성장을 돕고 올바른 길로 이끄는 교육자", "majors": "초등교육과"},
            "🖼️ 큐레이터": {"info": "전시를 기획하고 작품의 가치를 전달하는 예술 관리자", "majors": "예술학과, 미술사학과"}
        }
    },
    "INFJ": {
        "title": "🔮 영감을 주는 통찰가",
        "tags": ["#통찰력", "#선한영향력", "#조용한리더", "#신비로움"],
        "desc": "사람의 내면을 깊이 들여다보는 지혜로운 눈을 가졌어요. 세상에 조용한 변화를 일으킵니다.",
        "jobs": {
            "🧠 심리상담사": {"info": "마음의 상처를 치유하고 건강한 성장을 돕는 안내자", "majors": "심리학과, 교육학과"},
            "✍️ 소설가": {"info": "글을 통해 새로운 세계를 창조하고 가치를 전하는 작가", "majors": "국어국문학과, 문예창작과"},
            "🎓 교육학 연구원": {"info": "더 나은 교육 시스템을 고민하고 연구하는 전문가", "majors": "교육학과"}
        }
    },
    "INTJ": {
        "title": "🦅 지혜로운 전략가",
        "tags": ["#전략가", "#완벽주의", "#논리력", "#독립심"],
        "desc": "멀리 내다보고 완벽한 계획을 세우는 지적인 탐험가! 복잡한 문제도 척척 해결해요.",
        "jobs": {
            "🤖 AI 연구원": {"info": "인공지능 기술을 개발하고 미래를 설계하는 기술자", "majors": "컴퓨터공학과, 인공지능학과"},
            "🚀 우주공학자": {"info": "미지의 우주를 탐사할 발사체와 위성을 연구하는 직업", "majors": "항공우주공학과"},
            "♟️ 게임 기획자": {"info": "논리적인 규칙과 시스템으로 즐거움을 설계하는 사람", "majors": "컴퓨터공학과, 콘텐츠디자인과"}
        }
    },
    "ISTP": {
        "title": "🛠️ 만능 재주꾼 탐험가",
        "tags": ["#손재주", "#적응력", "#실용주의", "#위기탈출"],
        "desc": "도구와 기계를 잘 다루며 관찰력이 뛰어나요. 효율적이고 실용적인 해결책을 찾아내죠.",
        "jobs": {
            "🏎️ 카레이서": {"info": "최고의 집중력으로 한계를 돌파하는 드라이버", "majors": "자동차공학과, 스포츠레저학과"},
            "🛠️ 기계 엔지니어": {"info": "기계 장치를 설계하고 고치는 기술 전문가", "majors": "기계공학과"},
            "🎮 프로게이머": {"info": "순간적인 판단력과 기술로 승부를 가르는 경기인", "majors": "e스포츠학과, 게임학과"}
        }
    },
    "ISFP": {
        "title": "🎨 예술적인 감수성 탐험가",
        "tags": ["#미적감각", "#자유로운영혼", "#온화함", "#자연친화"],
        "desc": "자유로운 영혼과 미적 감각을 지닌 예술가! 겸손하고 조용하게 자신만의 색을 드러내요.",
        "jobs": {
            "🎨 일러스트레이터": {"info": "그림을 통해 감성과 메시지를 전달하는 시각 예술가", "majors": "디자인학과, 회화과"},
            "💐 플로리스트": {"info": "꽃으로 아름다운 공간과 순간을 디자인하는 직업", "majors": "원예학과, 환경디자인과"},
            "🐾 사육사": {"info": "동물과 소통하며 생명을 돌보는 소중한 직업", "majors": "동물자원학과, 수의학과"}
        }
    },
    "INFP": {
        "title": "🦄 꿈꾸는 이상주의자",
        "tags": ["#상상력", "#신념", "#공감왕", "#감수성"],
        "desc": "나만의 가치와 신념을 중요하게 생각해요. 따뜻한 상상력으로 세상을 아름답게 봅니다.",
        "jobs": {
            "🎬 영화 감독": {"info": "이야기에 생명력을 불어넣어 영상으로 담아내는 예술가", "majors": "연극영화과, 영상제작과"},
            "🎨 웹툰 작가": {"info": "상상력 넘치는 스토리와 그림으로 즐거움을 주는 창작자", "majors": "만화애니메이션학과"},
            "🌍 NGO 활동가": {"info": "더 나은 세상을 위해 가치 있는 일에 힘쓰는 활동가", "majors": "사회복지학과, 정치외교학과"}
        }
    },
    "INTP": {
        "title": "🧐 논리적인 아이디어뱅크",
        "tags": ["#호기심", "#분석력", "#독창성", "#비판적사고"],
        "desc": "분석하고 비평하는 것을 즐기는 호기심 천국! 독창적인 사고로 새로운 길을 열어요.",
        "jobs": {
            "🧬 이론 물리학자": {"info": "세상의 근본 원리를 수식으로 풀어내는 과학자", "majors": "물리학과"},
            "💻 소프트웨어 개발자": {"info": "효율적인 코드로 세상을 움직이는 프로그램을 만드는 사람", "majors": "컴퓨터공학과"},
            "🔍 변리사": {"info": "지적 재산권을 보호하는 기술 법률 전문가", "majors": "공학계열, 법학과"}
        }
    },
    "ESTP": {
        "title": "🔥 거침없는 활동가",
        "tags": ["#모험심", "#순발력", "#에너지", "#행동파"],
        "desc": "현재를 즐기며 문제를 즉각적으로 해결하는 능력자! 활동적이고 에너지가 넘쳐요.",
        "jobs": {
            "🚒 소방관": {"info": "위험한 현장에서 생명을 구하는 용감한 직업", "majors": "소방행정학과"},
            "💼 창업가": {"info": "기회를 포착하여 새로운 비즈니스를 개척하는 리더", "majors": "경영학과"},
            "🎤 스포츠 캐스터": {"info": "생동감 넘치는 목소리로 현장의 열기를 전하는 아나운서", "majors": "신문방송학과"}
        }
    },
    "ESFP": {
        "title": "🎉 자유로운 연예인",
        "tags": ["#스타성", "#친화력", "#즐거움", "#인싸"],
        "desc": "인생은 파티! 주변을 즐겁게 만드는 분위기 메이커입니다. 사람들과 어울리는 게 제일 좋아요.",
        "jobs": {
            "🕺 공연 예술가": {"info": "무대 위에서 에너지와 감동을 선사하는 아티스트", "majors": "연극영화과, 무용과"},
            "📹 콘텐츠 크리에이터": {"info": "기발한 영상으로 대중과 소통하는 창작자", "majors": "미디어학부, 영상학과"},
            "✈️ 항공 승무원": {"info": "하늘 위에서 승객의 안전과 편안함을 책임지는 직업", "majors": "항공운항과"}
        }
    },
    "ENFP": {
        "title": "🦋 재기발랄한 활동가",
        "tags": ["#열정", "#아이디어", "#긍정왕", "#스파크"],
        "desc": "창의적이고 열정적이며 사람들을 기분 좋게 만들어요. 무궁무진한 가능성을 꿈꿉니다.",
        "jobs": {
            "🎨 광고 기획자": {"info": "사람들의 마음을 움직이는 캠페인을 만드는 아이디어맨", "majors": "광고홍보학과"},
            "🌍 여행 작가": {"info": "세상의 곳곳을 탐험하며 기록을 남기는 탐험가", "majors": "관광학과, 국어국문학과"},
            "🎭 레크리에이션 강사": {"info": "즐거운 활동으로 사람들에게 웃음을 주는 직업", "majors": "체육학과, 사회복지학과"}
        }
    },
    "ENTP": {
        "title": "💡 뜨거운 논쟁을 즐기는 변론가",
        "tags": ["#브레인", "#고정관념타파", "#말재주", "#혁신가"],
        "desc": "지적인 도전이 즐거운 발명가 타입! 고정관념을 깨는 새로운 시각을 제시합니다.",
        "jobs": {
            "🧠 빅데이터 전문가": {"info": "복잡한 정보 속에서 인사이트를 찾아내는 전략가", "majors": "데이터사이언스학과, 컴퓨터학과"},
            "🗣️ 정치가": {"info": "더 나은 사회를 위해 정책을 제안하고 토론하는 리더", "majors": "정치외교학과"},
            "🎮 게임 디렉터": {"info": "새로운 게임의 세계관과 구조를 설계하는 총괄 기획자", "majors": "게임공학과, 경영학과"}
        }
    },
    "ESTJ": {
        "title": "👑 엄격한 관리자",
        "tags": ["#리더십", "#조직화", "#솔선수범", "#공정함"],
        "desc": "현실적이고 구체적인 계획을 세워 조직을 이끄는 리더! 체계적인 관리가 특기예요.",
        "jobs": {
            "🏢 경영 관리자": {"info": "조직의 효율성을 높이고 목표를 달성하는 관리자", "majors": "경영학과"},
            "⚖️ 경찰관": {"info": "사회의 질서와 법을 수호하는 정의로운 직업", "majors": "경찰행정학과"},
            "📰 기자": {"info": "정확한 사실을 취재하여 대중에게 전달하는 언론인", "majors": "언론정보학과, 국어국문학과"}
        }
    },
    "ESFJ": {
        "title": "🤝 사교적인 외교관",
        "tags": ["#배려심", "#마당발", "#하모니", "#의리파"],
        "desc": "사람들과 협력하며 조화를 이루는 것을 좋아해요. 주변에 따스한 관심을 보냅니다.",
        "jobs": {
            "🏨 호텔리어": {"info": "최고의 서비스로 고객에게 감동을 주는 전문가", "majors": "호텔경영학과"},
            "🤝 상담 전문가": {"info": "타인의 고민에 공감하고 실질적인 도움을 주는 사람", "majors": "상담심리학과, 사회복지학과"},
            "🏫 유치원 교사": {"info": "아이들의 첫 배움을 따뜻하게 이끄는 교육자", "majors": "유아교육과"}
        }
    },
    "ENFJ": {
        "title": "☀️ 정의로운 사회운동가",
        "tags": ["#선한영향력", "#카리스마", "#성장도우미", "#열정리더"],
        "desc": "타인의 성장을 돕고 이끄는 카리스마 넘치는 리더! 사람들의 마음을 움직이는 힘이 있어요.",
        "jobs": {
            "🏛️ 외교관": {"info": "국가를 대표하여 국제 관계를 조율하는 전문가", "majors": "정치외교학과, 국제학과"},
            "🎙️ 아나운서": {"info": "정확하고 신뢰감 있는 목소리로 소식을 전하는 사람", "majors": "신문방송학과"},
            "🧑‍🏫 라이프 코치": {"info": "개인의 잠재력을 발견하고 성장을 돕는 안내자", "majors": "교육심리학과"}
        }
    },
    "ENTJ": {
        "title": "🦁 대담한 통솔자",
        "tags": ["#야망", "#추진력", "#목표지향", "#비전제시"],
        "desc": "비전과 전략을 가지고 목표를 향해 돌진하는 CEO 타입! 도전적인 일을 즐깁니다.",
        "jobs": {
            "👔 기업 경영인(CEO)": {"info": "회사의 비전을 세우고 조직을 승리로 이끄는 수장", "majors": "경영학과, 경제학과"},
            "⚖️ 법조인": {"info": "법적 정의를 실현하고 논리로 변론하는 전문가", "majors": "법학과"},
            "🏗️ 투자 분석가": {"info": "시장의 흐름을 읽고 투자의 방향을 결정하는 전문가", "majors": "경제학과, 금융공학과"}
        }
    }
}

# 4. 메인 화면 구성
st.html("<div class='main-title'>🌸 봄날의 진로 탐험대 🌸</div>")
st.html("<div class='sub-title'>새싹 같은 당신의 꿈, MBTI로 찾아볼까요? 🌱✨</div>")

# 5. MBTI 선택 섹션
st.markdown("### 🍃 나의 성향 선택하기")
c1, c2, c3, c4 = st.columns(4)
with c1: e_i = st.select_slider("에너지", options=["I", "E"])
with c2: n_s = st.select_slider("인식", options=["S", "N"])
with c3: t_f = st.select_slider("판단", options=["T", "F"])
with c4: j_p = st.select_slider("생활", options=["P", "J"])

selected_mbti = e_i + n_s + t_f + j_p

st.write("---")

# 6. 결과 출력
if selected_mbti in mbti_info:
    res = mbti_info[selected_mbti]
    
    # 성향 매칭 요약 가이드 (해시태그)
    tags_html = "".join([f"<span class='tag'>{tag}</span>" for tag in res['tags']])
    
    st.html(f"""
        <div class='mbti-result-card'>
            <h2 style='color: #FF8E9E; margin-top:0; margin-bottom: 8px;'>✨ {selected_mbti}: {res['title']}</h2>
            <div style='margin-bottom: 15px;'>{tags_html}</div>
            <p style='font-size: 1.1rem; line-height: 1.6;'>{res['desc']}</p>
        </div>
    """)
    
    st.markdown(f"#### 🌸 {selected_mbti}에게 추천하는 '찰떡' 직업 (클릭해 보세요!)")
    
    # 직업 리스트 추출 (셀렉트박스 및 메모용)
    job_list = list(res['jobs'].keys())
    
    # 직업별 정보 출력 (Expander 형태)
    for job_name, job_detail in res['jobs'].items():
        with st.expander(f"{job_name}"):
            st.write(f"🔍 **직업 설명:** {job_detail['info']}")
            st.write(f"🎓 **관련 학과:** {job_detail['majors']}")

    # 📝 7. 실시간 익명 진로 방명록 (상세 입력 버전)
    st.write("")
    st.write("---")
    st.markdown("#### 💬 친구들과 나누는 진로 한 줄 메모장")
    
    # 메모 입력란 (Form 구조)
    with st.form(key="memo_form", clear_on_submit=True):
        col_inputs1, col_inputs2 = st.columns(2)
        
        with col_inputs1:
            nick = st.text_input("👤 나의 닉네임", placeholder="예: 멋진꿈나무")
            fav = st.selectbox("🎯 가장 맘에 드는 추천 직업", options=job_list)
            
        with col_inputs2:
            dream = st.text_input("🌟 실제 나의 장래희망", placeholder="예: 과학자 (없다면 '탐색 중' 입력 가능)")
            
        memo_txt = st.text_input("✍️ 하고 싶은 한 마디", placeholder="진로에 대한 다짐이나 소감을 적어주세요!")
        
        submit_button = st.form_submit_button(label="📌 진로 카드 등록하기")
        
        # 유효성 검사 후 데이터 저장
        if submit_button:
            if not nick.strip() or not memo_txt.strip() or not dream.strip():
                st.warning("⚠️ 모든 칸을 채워주셔야 진로 카드를 등록할 수 있어요!")
            else:
                st.session_state["shared_memos"].append({
                    "nickname": nick,
                    "mbti": selected_mbti,
                    "fav_job": fav,
                    "real_dream": dream,
                    "text": memo_txt
                })
                st.toast("📝 친구들과 공유하는 진로 방명록에 등록되었어요!", icon="✨")

    # 다른 사람들이 남긴 메모 예쁜 디자인 카드 형태로 노출
    st.write("**🔽 친구들의 생생한 진로 고민 및 다짐 목록**")
    for memo in reversed(st.session_state["shared_memos"][-5:]):
        st.html(f"""
            <div class='memo-card'>
                <div class='memo-header'>
                    <strong>{memo['nickname']}</strong> 
                    <span class='memo-badge'>{memo['mbti']}</span> | 
                    <span>🎯 추천 원픽: {memo['fav_job']}</span> | 
                    <span>🌟 장래희망: {memo['real_dream']}</span>
                </div>
                <div class='memo-content'>“ {memo['text']} ”</div>
            </div>
        """)

# 8. 푸터
st.write("")
st.write("")
st.html("<div style='text-align: center; color: #888; font-size: 0.9rem;'>🌼 당신의 꿈이 꽃피는 그날까지 응원할게요! 🌼</div>")
