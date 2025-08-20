# streamlit_app.py

import streamlit as st

# --- 앱의 기본 설정 ---
# 이 부분은 항상 코드 최상단에 위치해야 합니다.
st.set_page_config(
    page_title="MBTI 학습 유형 진단 (5점 척도)",
    page_icon="🧠",
)

# --- 세션 상태 초기화 ---
# st.session_state는 사용자의 답변이나 앱의 상태를 저장하는 메모리 공간입니다.
# 'submitted' 키가 없으면 False로 만들어, 아직 제출 전임을 표시합니다.
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
    st.session_state.answers = {}

def calculate_mbti(answers):
    """
    사용자의 5점 척도 답변을 바탕으로 MBTI 유형을 계산하는 함수.
    (1점: 왼쪽 성향, 3점: 중간, 5점: 오른쪽 성향)
    각 점수를 -2 ~ +2점으로 변환하여 합산합니다.
    """
    # 점수 변환 맵: 1점 -> -2점, 2점 -> -1점, 3점 -> 0점, 4점 -> 1점, 5점 -> 2점
    score_map = {1: -2, 2: -1, 3: 0, 4: 1, 5: 2}

    # 각 차원별 점수를 계산합니다.
    # 양수(+)면 오른쪽 유형(E, N, F, J), 음수(-)면 왼쪽 유형(I, S, T, P)입니다.
    ei_score = score_map[answers['q1']] + score_map[answers['q5']]  # E > 0 > I
    sn_score = score_map[answers['q2']] + score_map[answers['q6']]  # N > 0 > S
    tf_score = score_map[answers['q3']] + score_map[answers['q7']]  # F > 0 > T
    jp_score = score_map[answers['q4']] + score_map[answers['q8']]  # J > 0 > P
    
    # 각 차원별로 유형을 결정합니다.
    mbti = ""
    mbti += "E" if ei_score >= 0 else "I"
    mbti += "N" if sn_score >= 0 else "S"
    mbti += "F" if tf_score >= 0 else "T"
    mbti += "J" if jp_score >= 0 else "P"
    
    return mbti

def get_learning_style(mbti):
    """
    계산된 MBTI 유형에 맞는 학습 스타일 설명을 반환하는 함수.
    """
    # 이 부분은 이전과 동일합니다.
    styles = {
        "ISTJ": "실용적이고 체계적인 학습을 선호합니다. 사실에 근거하여 꾸준히 학습하는 스타일입니다.",
        "ISFJ": "온정적이고 책임감이 강하며, 다른 사람에게 도움이 되는 내용을 학습할 때 동기부여를 받습니다.",
        "INFJ": "통찰력이 있고, 아이디어의 이면에 있는 의미를 탐구하는 것을 좋아합니다. 거시적인 관점에서 학습합니다.",
        "INTJ": "독립적이고 논리적인 학습자입니다. 복잡한 이론과 아이디어를 이해하고 자신만의 비전을 만듭니다.",
        "ISTP": "논리적이고 실용적인 문제 해결을 즐깁니다. 직접 경험하고 분석하며 배우는 것을 선호합니다.",
        "ISFP": "호기심이 많고 개방적이며, 실제 경험을 통해 배우는 것을 중요하게 생각합니다. 유연한 학습 환경을 선호합니다.",
        "INFP": "이상주의적이며, 자신의 가치와 신념에 맞는 내용을 학습할 때 가장 큰 흥미를 느낍니다.",
        "INTP": "지적 호기심이 강하며, 논리적 분석과 추상적인 개념을 탐구하는 것을 즐깁니다.",
        "ESTP": "활동적이고 현실적인 학습을 선호합니다. 직접 참여하고 경험하며 문제를 해결하는 과정에서 배웁니다.",
        "ESFP": "사교적이며, 다른 사람들과 함께 배우고 협력하는 환경에서 능력을 발휘합니다.",
        "ENFP": "열정적이고 상상력이 풍부합니다. 다양한 가능성을 탐색하고 새로운 아이디어를 배우는 것을 즐깁니다.",
        "ENTP": "도전적인 과제를 즐기고, 논쟁과 토론을 통해 아이디어를 발전시키는 것을 좋아합니다.",
        "ESTJ": "체계적이고 조직적인 학습 환경을 선호합니다. 명확한 목표와 절차에 따라 학습하는 것을 효율적으로 생각합니다.",
        "ESFJ": "사람들과의 상호작용을 통해 배우는 것을 좋아하며, 조화로운 학습 분위기를 중요하게 생각합니다.",
        "ENFJ": "다른 사람의 성장을 돕는 것에 열정을 느끼며, 협력적인 학습 환경에서 큰 동기부여를 받습니다.",
        "ENTJ": "전략적이고 목표 지향적인 학습자입니다. 장기적인 비전을 가지고 지식을 체계적으로 습득합니다."
    }
    return styles.get(mbti, "결과를 찾을 수 없습니다.")

# --- 앱 UI 구성 ---
st.title("🧠 MBTI 기반 학습 유형 진단")
st.write("각 문항을 읽고, 자신과 얼마나 일치하는지 5점 척도로 선택해주세요.")
st.caption("`(1점: 왼쪽 설명에 가까움, 3점: 중간, 5점: 오른쪽 설명에 가까움)`")

# st.form을 사용하여 여러 위젯을 그룹화하고, 제출 버튼을 누를 때만 상호작용합니다.
with st.form("mbti_form"):
    
    # 각 슬라이더의 설명을 양쪽 극단으로 명확히 제시합니다.
    st.subheader("에너지 방향")
    q1 = st.slider("혼자 있을 때 (I) vs 함께 있을 때 (E) 에너지를 얻는다.", 1, 5, 3)
    q5 = st.slider("충분히 생각 후 말한다 (I) vs 말하면서 생각을 정리한다 (E)", 1, 5, 3)

    st.subheader("인식 기능")
    q2 = st.slider("현실적이고 구체적인 정보 (S) vs 직관과 미래의 가능성 (N)을 본다.", 1, 5, 3)
    q6 = st.slider("실제 경험을 중시한다 (S) vs 추상적인 아이디어를 중시한다 (N)", 1, 5, 3)
    
    st.subheader("결정 방식")
    q3 = st.slider("객관적 사실과 논리 (T) vs 사람과의 관계와 감정 (F)을 고려한다.", 1, 5, 3)
    q7 = st.slider("옳고 그름이 중요하다 (T) vs 타인에게 미칠 영향이 중요하다 (F)", 1, 5, 3)

    st.subheader("생활 양식")
    q4 = st.slider("상황에 따라 유연하게 대처 (P) vs 계획에 따라 체계적으로 진행 (J)", 1, 5, 3)
    q8 = st.slider("마감이 임박해야 집중 (P) vs 미리 계획하여 마감 준수 (J)", 1, 5, 3)
    
    # st.form_submit_button은 form 안에서 사용되어야 합니다.
    submitted = st.form_submit_button("결과 확인하기")
    if submitted:
        st.session_state.submitted = True
        st.session_state.answers = {
            'q1': q1, 'q5': q5, 'q2': q2, 'q6': q6,
            'q3': q3, 'q7': q7, 'q4': q4, 'q8': q8,
        }

# 제출 버튼이 눌렸다면, 이 아래의 코드가 실행됩니다.
if st.session_state.submitted:
    user_mbti = calculate_mbti(st.session_state.answers)
    learning_style = get_learning_style(user_mbti)
    
    st.markdown("---")
    st.subheader("🎉 진단 결과")
    st.success(f"당신의 MBTI 학습 유형은 **{user_mbti}** 입니다!")
    st.write(learning_style)

    if st.button("다시 검사하기"):
        # 세션 상태를 초기화하여 처음부터 다시 시작할 수 있도록 합니다.
        st.session_state.submitted = False
        st.session_state.answers = {}
        st.rerun() # 최신 Streamlit 앱 새로고침 함수