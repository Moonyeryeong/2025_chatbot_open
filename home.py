import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="당뇨병 통합관리", page_icon="🩺")

# 메인 아이콘/타이틀
st.markdown(
    """
    <h1 style="display: flex; align-items: center; font-size: 2.3rem;">
        <span style="font-size: 2.8rem; margin-right: 0.7rem;">🩺</span>
        <span>당뇨병 통합관리</span>
    </h1>
    """,
    unsafe_allow_html=True
)

# 메인 환영 메시지 & 설명
st.markdown("""
---
### 😊 환영합니다!
**당신의 건강한 삶을 응원하는 당뇨병 통합관리 플랫폼**입니다.

여기서는 당뇨병 환자분들이 꼭 필요한 정보와  
쉽게 실천할 수 있는 건강관리 방법을 제공합니다.
""")

st.markdown("""
<div style="background-color: #F6F8FC; border-radius: 10px; padding: 20px; margin: 10px 0;">
    <b>이 플랫폼에서는…</b><br><br>
    <span style="font-size:1.1em">
    - 🤖 <b>AI 챗봇:</b> 언제든 궁금한 점을 쉽고 빠르게 상담<br>
    - 🔍 <b>맞춤 정보:</b> 증상·식습관·운동·치료 등 당뇨 관리에 꼭 필요한 내용만 담았어요<br>
    - 💊 <b>복약·혈당 관리:</b> 나의 복용 약, 혈당 기록을 손쉽게 저장 & 확인<br>
    - 📊 <b>건강 리포트:</b> 내 건강변화와 목표를 한눈에!<br>
    - 🤝 <b>심리적 동반자:</b> 당신은 혼자가 아닙니다. 항상 함께 할게요.</span>
</div>
""", unsafe_allow_html=True) 


st.markdown("---")

# 건강한 당부 & 다짐
st.markdown(
    """
    <div style="padding: 16px; background-color: #E6F7EC; border-radius: 10px; margin-bottom:10px;">
        <b>🎉 오늘부터 건강관리, 저희와 함께 시작해볼까요?</b><br>
        <span style="color: #277C5D;">조금씩 바꿔가는 생활습관이 여러분의 삶을 바꿉니다.</span>
    </div>
    """,
    unsafe_allow_html=True
)

# 안내 메시지
st.markdown(
    """
    <div style="padding: 13px; background-color: #e5f1ff; border-radius: 8px;">
        <b>👉 왼쪽 메뉴에서 원하는 기능을 선택해 주세요!</b><br>
        <span style="color: #2263ac;">개인정보 입력은 <b>[개인정보]</b> 메뉴에서, 챗봇 상담은 <b>[챗봇]</b> 메뉴에서 바로 가능합니다.</span>
    </div>
    """,
    unsafe_allow_html=True
)
