import streamlit as st
import math

st.set_page_config(page_title="비밀번호 경우의 수 계산기", layout="centered")

st.title("비밀번호 조건에 따른 경우의 수와 예상 시간 계산기")
st.write("비밀번호 조건을 선택하면 가능한 경우의 수와 예상 추측 시간을 계산합니다.")

menu = st.radio(
    "기능 선택",
    ["경우의 수 계산", "비밀번호 예상 시간 계산"]
)

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f}초"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.2f}분"
    hours = minutes / 60
    if hours < 24:
        return f"{hours:.2f}시간"
    days = hours / 24
    if days < 365:
        return f"{days:.2f}일"
    years = days / 365
    return f"{years:.2e}년"

def permutation(n, r):
    if r > n:
        return 0
    result = 1
    for i in range(r):
        result *= n - i
    return result

if menu == "경우의 수 계산":
    st.subheader("조건별 경우의 수 계산")

    length = st.slider("비밀번호 길이", 4, 20, 8)

    char_type = st.selectbox(
        "문자 종류",
        [
            "숫자만",
            "영어만",
            "영어 + 숫자",
            "영어 + 숫자 + 특수문자"
        ]
    )

    repeat = st.selectbox(
        "반복 사용 가능 여부",
        ["반복 가능", "반복 불가능"]
    )

    if char_type == "숫자만":
        char_count = 10
    elif char_type == "영어만":
        char_count = 52
    elif char_type == "영어 + 숫자":
        char_count = 62
    else:
        char_count = 94

    if repeat == "반복 가능":
        cases = char_count ** length
        formula = f"{char_count}^{length}"
    else:
        cases = permutation(char_count, length)
        formula = f"{char_count}P{length}"

    st.write("사용 가능한 문자 수:", char_count, "개")
    st.write("계산식:", formula)
    st.success(f"가능한 비밀번호 개수: {cases:,}가지")

    speed = st.number_input(
        "초당 시도 횟수",
        min_value=1,
        value=1000,
        step=1000
    )

    seconds = cases / speed
    st.info(f"예상 추측 시간: {format_time(seconds)}")

elif menu == "비밀번호 예상 시간 계산":
    st.subheader("내 비밀번호 예상 시간 계산")

    password = st.text_input("비밀번호 입력", type="password")
    speed = st.number_input(
        "초당 시도 횟수",
        min_value=1,
        value=100000000,
        step=1000000
    )

    if password:
        char_count = 0

        if any(ch.isdigit() for ch in password):
            char_count += 10
        if any(ch.islower() for ch in password):
            char_count += 26
        if any(ch.isupper() for ch in password):
            char_count += 26
        if any(not ch.isalnum() for ch in password):
            char_count += 32

        cases = char_count ** len(password)
        seconds = cases / speed

        st.write("비밀번호 길이:", len(password), "자리")
        st.write("사용 문자 집합 크기:", char_count, "개")
        st.success(f"예상 경우의 수: {cases:,}가지")
        st.info(f"예상 추측 시간: {format_time(seconds)}")

        if seconds < 60:
            level = "낮음"
        elif seconds < 86400:
            level = "보통"
        elif seconds < 31536000:
            level = "높음"
        else:
            level = "매우 높음"

        st.warning(f"보안 등급: {level}")
