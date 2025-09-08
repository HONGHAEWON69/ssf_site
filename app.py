import streamlit as st

st.title("첫 번째 스트림릿 앱 🎉")
st.write("안녕하세요! GitHub → Streamlit Cloud 연습입니다.")

name = st.text_input("이름을 입력해 주세요:")

if st.button("인사하기"):
    st.success(f"반갑습니다, {name}님!")
