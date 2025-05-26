import streamlit as st
from openai import OpenAI

# (주의) st.set_page_config는 main.py에만 있음. 여기선 절대 쓰지 마세요!

# 상단 타이틀+슬로건
st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 18px;">
    <span style="font-size: 2.8rem;">🩺</span>
    <h1 style="margin-bottom: 0; font-size:2.1rem; color:#246189;">당뇨병 통합관리</h1>
    <div style="font-size: 1.15rem; color: #277C5D;">건강한 변화, 오늘부터 함께 시작해요</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 주요 기능 카드형 안내
st.markdown("""
<div style="display: flex; gap: 18px; justify-content: center; margin-bottom: 22px;">
    <div style="background:#F6F8FC; border-radius:15px; padding:18px 22px; width:210px; box-shadow:0 2px 7px #eef;">
        <div style="font-size:2.1rem; text-align:center;">🤖</div>
        <b style="font-size:1.07rem;">AI 건강챗봇</b>
        <div style="font-size:0.97rem; color:#555; margin-top:6px;">
            궁금증/고민 24시간 상담
        </div>
    </div>
    <div style="background:#E6F7EC; border-radius:15px; padding:18px 22px; width:210px; box-shadow:0 2px 7px #eef;">
        <div style="font-size:2.1rem; text-align:center;">💊</div>
        <b style="font-size:1.07rem;">복약·혈당관리</b>
        <div style="font-size:0.97rem; color:#555; margin-top:6px;">
            내 건강기록 간편 저장/확인
        </div>
    </div>
    <div style="background:#e5f1ff; border-radius:15px; padding:18px 22px; width:210px; box-shadow:0 2px 7px #eef;">
        <div style="font-size:2.1rem; text-align:center;">📊</div>
        <b style="font-size:1.07rem;">맞춤 건강리포트</b>
        <div style="font-size:0.97rem; color:#555; margin-top:6px;">
            목표·변화, 쉽고 알차게 분석
        </div>
    </div>
    <div style="background:#fff6ec; border-radius:15px; padding:18px 22px; width:210px; box-shadow:0 2px 7px #eef;">
        <div style="font-size:2.1rem; text-align:center;">💡</div>
        <b style="font-size:1.07rem; white-space:nowrap; display:block; text-align:center;">
            실천팁 & 동기부여
        </b>
        <div style="font-size:0.97rem; color:#555; margin-top:6px;">
            오늘의 건강 메시지와 동기부여
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 사용자 안내/행동 유도
st.markdown("""
<div style="text-align:center; margin-bottom:18px;">
    <span style="font-size: 1.08rem; color:#2263ac;"><b>왼쪽 메뉴에서 원하는 기능을 선택해 시작해보세요!</b></span><br>
    <span style="color: #396;">로그인하면 나만의 건강기록을 안전하게 저장할 수 있습니다.</span>
</div>
""", unsafe_allow_html=True)

# 따뜻한 메시지/동기부여
st.info("✨ 오늘부터 건강한 습관, 저희와 함께 만들어봐요!")