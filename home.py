import streamlit as st
import base64

# 상단 Hero 배너 섹션
st.markdown(f"""
<style>
.hero {{
    position: relative;
    height: 90vh; 
    border-radius: 0;
    overflow: hidden;
    margin-bottom: 40px;
}}            
.hero .content {{
    position: relative;
    z-index: 2;
    text-align: center;
    padding-top: 200px;
    color: #222;
}}
.hero .content h1 {{
    font-size: 4.2rem;
    margin-bottom: 10px;
    background: linear-gradient(to right, #4a6cf7, #7acdf4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.hero .content p {{
    font-size: 1.3rem;
    max-width: 700px;
    margin: auto;
    color: #333;
}}
</style>
<div class="hero">
    <div class="background"></div>
    <div class="content">
        <h2 style="font-size: 1.8rem;">당뇨병 통합관리 서비스</h2>
        <h1>DiabetesCare service</h1>
        <p>당뇨병 환자를 위한 대화형 인공지능과<br>
        맞춤형 건강관리 기능이 결합된<br>
        스마트 통합 서비스</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 사용 흐름
st.markdown("""
<div style='text-align:center; margin:40px 0;'>
    <h4>🛠️ 서비스 사용 방법</h4>
</div>
<div style="display:flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 40px;">
    <div style="background:#f1f6ff;padding:20px;border-radius:12px;width:220px;">
        <h5 style="color:#4a6cf7;">① 시작하기</h5>
        <p style="font-size:0.88rem;">회원가입 후 <b>기본 건강정보</b>를 입력해요.</p>
    </div>
    <div style="background:#eaf9f0;padding:20px;border-radius:12px;width:220px;">
        <h5 style="color:#43b97f;">② 기록하기</h5>
        <p style="font-size:0.88rem;">식단, 혈당, 약물 이력을 <b>간편하게 기록</b>해요.</p>
    </div>
    <div style="background:#fff3e6;padding:20px;border-radius:12px;width:220px;">
        <h5 style="color:#ff944d;">③ 피드백 받기</h5>
        <p style="font-size:0.88rem;">챗봇과 리포트를 통해 <b>맞춤 건강관리</b>를 받아요!</p>
    </div>
</div>
""", unsafe_allow_html=True)

# CTA 메시지
st.markdown("""
<div style="text-align: center; padding: 20px; border-radius: 10px; margin: 30px 0;">
    <h4 style="color: #4a6cf7;">건강한 변화, 지금 당신과 함께 시작합니다.</h4>
    <p style="color: gray;">작은 기록이 큰 변화를 만들어냅니다.</p>
</div>
""", unsafe_allow_html=True)

# 기능 카드 섹션
def feature_card(title, icon, target):
    with st.container():
        if st.button(f"{icon} {title}", use_container_width=True, key=target):
            st.session_state["__page__"] = target
            st.rerun()

st.markdown("""
            <div style='text-align:center; margin:40px 0;'> <h4>🔎 주요 기능 바로가기</h4>
</div>""", unsafe_allow_html=True)
cols2 = st.columns(3)
features2 = [
    ("혈당관리", "🧪", "reports/glucose.py"),
    ("식단기록", "📋", "reports/personal_diet.py"),
    ("복용약", "💊", "reports/medication.py"),
]
for col, (title, icon, target) in zip(cols2, features2):
    with col:
        feature_card(title, icon, target)

# 페이지 이동 처리
if "__page__" in st.session_state:
    st.switch_page(st.session_state.pop("__page__"))

# 푸터
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
st.markdown("""
<hr>
<div style='text-align: center; font-size: 0.85rem; color: #aaa; margin-top:20px;'>
  © 2025 DiabetesCare service.
</div>
""", unsafe_allow_html=True)
