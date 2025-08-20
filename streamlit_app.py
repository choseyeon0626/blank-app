streamlit```

---

### **[streamlit_app.py 전체 코드]**

아래 코드를 전부 복사해서 `streamlit_app.py` 라는 이름의 파이썬 파일로 저장하세요.

```python
# streamlit_app.py

import streamlit as st

# --- 앱의 기본 설정 ---
st.set_page_config(
    page_title="MBTI 학습 유형 진단 (5점 척도)",
    page_icon="🧠",
)

# --- 세션 상태 초기화 ---
# 'submitted' 키가 세션 상태에 없으면 False로 초기화합니다.
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

def calculate_mbti(answers):
    """
    사용자의 5점 척도 답변을 바탕으로 MBTI 유형을 계산하는 함수.
    (1점: 매우 아니다, 3점: 보통, 5점: 매우 그렇다)
    각 점수를 E, N, F, J 성향에 대한 점수로 변환하여 합산합니다.
    """
    # 점수 변환 맵: 1점 -> -2점, 2점 -> -1점, 3점 -> 0점, 4점 -> 1점, 5점 -> 2점
    score_map = {1: -2, 2: -1, 3: 0, 4: 1, 5: 2}

    # 각 차원별 점수를 계산합니다.
    # 점수가 양수(+)면 E, N, F, J 성향, 음수(-)면 I, S, T, P 성향입니다.
    ei_score = score_map[answers['q1']] + score_map[answers['q5']]
    sn_score = score_map[answers['q2']] + score_map[answers['q6']]
    tf_score = score_map[answers['q3']] + score_map[answers['q7']]
    jp_score = score_map[answers['q4']] + score_map[answers['q8']]
    
    # 각 차원별로 더 높은 점수를 받은 유형을 선택합니다.
    mbti = ""
    mbti += "E" if ei_score >= 0 else "I"
    mbti += "N" if sn_score >= 0 else "S"
    mbti += "F" if tf_score >= 0 else "T"
    mbti += "J" if jp_score >= 0 else "P"
    
    return mbti

def get_learning_style(mbti):
    """
    계산된 MBTI 유형에 맞는 학습 스타일 설명을 반환하는 함수. (이전과 동일)
    """
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
st.caption("`(1: 전혀 그렇지 않다, 3: 보통이다, 5: 매우 그렇다)`")

# st.form을 사용하여 여러 위젯을 그룹화하고, 제출 버튼을 누를 때만 앱이 다시 실행되도록 합니다.
with st.form("mbti_form"):
    
    # st.slider(레이블, 최소값, 최대값, 기본값)
    # 각 질문은 E, N, F, J 성향에 "그렇다"고 답하는 방향으로 구성되었습니다.
    
    st.subheader("에너지 방향 (E/I)")
    q1 = st.slider("나는 여러 사람과 어울리며 에너지를 얻는다.", 1, 5, 3)
    q5 = st.slider("나는 생각을 말로 표현하면서 정리하는 편이다.", 1, 5, 3)

    st.subheader("인식 기능 (S/N)")
    q2 = st.slider("나는 나무보다 숲을 보는 경향이 있으며, 미래의 가능성을 중요하게 생각한다.", 1, 5, 3)
    q6 = st.slider("나는 추상적이고 비유적인 설명을 더 쉽게 이해한다.", 1, 5, 3)
    
    st.subheader("결정 방식 (T/F)")
    q3 = st.slider("나는 결정을 내릴 때 객관적인 사실보다 사람들과의 관계를 더 고려한다.", 1, 5, 3)
    q7 = st.slider("나는 '다른 사람에게 어떤 영향을 미칠까'를 더 중요하게 생각한다.", 1, 5, 3)

    st.subheader("생활 양식 (J/P)")
    q4 = st.slider("나는 계획을 세우고 체계적으로 생활하는 것을 선호한다.", 1, 5, 3)
    q8 = st.slider("나는 마감 기한을 지키기 위해 미리 계획을 세운다.", 1, 5, 3)
    
    # st.form_submit_button은 form 내에서 사용되어야 합니다.
    submitted = st.form_submit_button("결과 확인하기")
    if submitted:
        # 제출 버튼이 눌리면, submitted 상태를 True로 변경합니다.
        st.session_state.submitted = True

        # 각 슬라이더의 값을 세션 상태에 저장합니다.
        st.session_state.answers = {
            'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4,
            'q5': q5, 'q6': q6, 'q7': q7, 'q8': q8,
        }

# 제출 버튼이 눌린 후에만 결과 섹션을 표시합니다.
if st.session_state.submitted:
    # 세션 상태에서 답변을 가져옵니다.
    user_answers = st.session_state.answers
    
    # MBTI 유형 계산 및 학습 스타일 설명 가져오기
    user_mbti = calculate_mbti(user_answers)
    learning_style = get_learning_style(user_mbti)
    
    st.markdown("---") # 구분선 추가
    st.subheader("🎉 진단 결과")
    
    st.success(f"당신의 MBTI 학습 유형은 **{user_mbti}** 입니다!")
    st.write(learning_style)

    # 다시 검사하고 싶을 경우를 대비한 버튼
    if st.button("다시 검사하기"):
        # 세션 상태를 초기화합니다.
        st.session_state.submitted = False
        del st.session_state.answers
        st.experimental_rerun() # 앱을 새로고침하여 초기 상태로 돌아갑니다.