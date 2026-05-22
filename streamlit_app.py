import streamlit as st

st.title("🎈 My new app")
st.write(
    "This is a placeholder app."
)
import random
import streamlit as st

st.set_page_config(page_title="초등 사칙연산 연습", layout="centered")

st.title("초등학교 사칙연산 연습 프로그램")

ops_map = {
    "덧셈": "+",
    "뺄셈": "-",
    "곱셈": "×",
    "나눗셈": "÷",
}

with st.sidebar:
    st.header("설정")
    selected_ops = st.multiselect("연습할 연산을 선택하세요", list(ops_map.keys()), default=["덧셈", "뺄셈"])
    min_val, max_val = st.slider("피연산자 범위", 0, 100, (0, 20))
    qcount = st.slider("문제 수", 5, 30, 10)
    allow_negative = st.checkbox("뺄셈에서 음수 허용", value=False)

def make_question(op, a_min, a_max):
    if op == "덧셈":
        a = random.randint(a_min, a_max)
        b = random.randint(a_min, a_max)
        return (a, b, "+", a + b)
    if op == "뺄셈":
        a = random.randint(a_min, a_max)
        b = random.randint(a_min, a_max)
        if not allow_negative and a < b:
            a, b = b, a
        return (a, b, "-", a - b)
    if op == "곱셈":
        a = random.randint(max(a_min, 0), a_max)
        b = random.randint(max(a_min, 0), a_max)
        return (a, b, "×", a * b)
    if op == "나눗셈":
        # 나눗셈은 나머지가 없는 문제로 생성
        # 분모는 1..12, 몫은 0..12 범위에서 선택하고 피연산자 범위를 넘지 않도록 조정
        b = random.randint(1, min(12, max(1, a_max)))
        q = random.randint(1, min(12, max(1, a_max // b)))
        a = b * q
        return (a, b, "÷", q)

def init_session():
    if "started" not in st.session_state:
        st.session_state.started = False
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "index" not in st.session_state:
        st.session_state.index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

init_session()

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### 준비")
    st.write("설정에서 연산, 범위, 문제 수를 골라 '연습 시작'을 누르세요.")
with col2:
    if st.button("연습 시작"):
        if not selected_ops:
            st.warning("최소 하나의 연산을 선택하세요.")
        else:
            st.session_state.questions = [make_question(random.choice(selected_ops), min_val, max_val) for _ in range(qcount)]
            st.session_state.index = 0
            st.session_state.score = 0
            st.session_state.started = True
            st.session_state.last_result = None

if not st.session_state.started:
    st.info("연습을 시작하려면 오른쪽 상단의 '연습 시작' 버튼을 누르세요.")
    st.stop()

# 문제 표시
q = st.session_state.questions[st.session_state.index]
a, b, sym, answer = q

st.markdown(f"## 문제 {st.session_state.index + 1} / {len(st.session_state.questions)}")
st.markdown(f"### {a} {sym} {b} = ?")

col_a, col_b = st.columns([3, 1])
with col_a:
    user_input = st.text_input("정답을 입력하세요", key=f"ans_{st.session_state.index}")
with col_b:
    if st.button("제출", key=f"submit_{st.session_state.index}"):
        try:
            user_ans = int(user_input.strip())
        except Exception:
            st.error("정수로 입력해 주세요.")
            user_ans = None
        if user_ans is not None:
            if user_ans == answer:
                st.success("정답입니다!")
                st.session_state.score += 1
                st.session_state.last_result = True
            else:
                st.error(f"틀렸습니다. 정답은 {answer} 입니다.")
                st.session_state.last_result = False

if st.session_state.last_result is not None:
    if st.session_state.index + 1 < len(st.session_state.questions):
        if st.button("다음 문제"):
            st.session_state.index += 1
            st.session_state.last_result = None
            st.experimental_rerun()
    else:
        st.markdown("---")
        st.markdown("## 결과")
        st.markdown(f"- 맞춘 문제: {st.session_state.score} / {len(st.session_state.questions)}")
        pct = int(st.session_state.score / len(st.session_state.questions) * 100)
        st.markdown(f"- 점수: {pct}%")
        if st.button("다시 시작"):
            st.session_state.started = False
            st.session_state.questions = []
            st.session_state.index = 0
            st.session_state.score = 0
            st.session_state.last_result = None
            st.experimental_rerun()

st.sidebar.markdown("---")
st.sidebar.write("앱 사용법: 연산과 범위를 선택하고 문제 수를 정한 뒤 '연습 시작'을 누르세요. 각 문제에 답을 입력하고 '제출'을 누른 뒤 '다음 문제'로 진행하세요.")
