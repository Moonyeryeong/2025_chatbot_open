import streamlit as st
import os
import sys
import datetime

if not st.session_state.get("logged_in", False):
    st.warning("🔒 로그인 해주세요.")
    st.stop()

username = st.session_state["username"]

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import save_patient_info, load_patient_info

st.markdown("<h2>📝 당뇨병 맞춤 건강 리포트</h2>", unsafe_allow_html=True)
st.markdown("<p>건강 정보를 입력하고 맞춤 리포트를 받아보세요.</p>", unsafe_allow_html=True)

# 해당 유저의 기존 데이터 불러오기
all_users = load_patient_info(username)

if all_users:
    prev = all_users[0]
else:
    prev = {}

# 출생년도 리스트 (1920~현재년도)
current_year = datetime.datetime.now().year
years = list(range(current_year, 1919, -1))

# 사용자 입력 폼
with st.form("user_info", clear_on_submit=False):
    st.markdown("### 👤 기본 정보")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("이름", value=prev.get("name", ""))
        birth_year = st.selectbox("출생년도", years, index=years.index(prev.get("birth_year")) if prev.get("birth_year") else 0)
        age = current_year - birth_year + 1  # 한국식 나이
        gender = st.selectbox("성별", ["남성", "여성"], index=0 if prev.get("gender", "남성") == "남성" else 1)
    with col2:
        height = st.selectbox("키 (cm)", list(range(120, 251)), index=prev.get("height", 170)-120 if prev.get("height") else 50)
        weight = st.selectbox("몸무게 (kg)", list(range(30, 201)), index=prev.get("weight", 60)-30 if prev.get("weight") else 30)

    st.divider()
    st.markdown("### 🩸 건강 정보")
    col3, col4 = st.columns(2)
    with col3:
        fasting_glucose = st.number_input("공복 혈당 (mg/dL)", min_value=50, max_value=300, value=int(prev.get("fasting_glucose", 100)))
        hba1c = st.number_input("당화혈색소 (%)", min_value=3.0, max_value=15.0, step=0.1, value=float(prev.get("hba1c", 5.6)))
    with col4:
        bp_sys = st.number_input("혈압 (수축기 mmHg)", min_value=80, max_value=200, value=int(prev.get("bp_sys", 120)))
        bp_dia = st.number_input("혈압 (이완기 mmHg)", min_value=50, max_value=130, value=int(prev.get("bp_dia", 80)))

    st.divider()
    st.markdown("### 💊 복약 및 진단 이력")
    on_medication = st.radio("당뇨약 또는 인슐린 투여 중인가요?", ["예", "아니오"], index=0 if prev.get("on_medication", "아니오") == "예" else 1)
    diabetes_type = st.selectbox("진단받은 당뇨 유형", ["없음", "제1형", "제2형", "임신성"],
                                 index=["없음", "제1형", "제2형", "임신성"].index(prev.get("diabetes_type", "없음")))

    submitted = st.form_submit_button("✅ 리포트 제출")

# 제출 처리
if submitted:
    user_data = {
        "name": name,
        "birth_year": birth_year,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "fasting_glucose": fasting_glucose,
        "hba1c": hba1c,
        "bp_sys": bp_sys,
        "bp_dia": bp_dia,
        "on_medication": on_medication,
        "diabetes_type": diabetes_type
    }


    all_users = [user_data]  
    save_patient_info(username, all_users, overwrite=True)
    st.session_state["diabetes_report"] = user_data
    st.success(f"✅ {name}님의 리포트가 저장되었습니다!")

# 삭제 처리
if all_users:
    if st.button("🗑️ 기존 리포트 삭제하기"):
        all_users.pop(0)
        save_patient_info(username, all_users, overwrite=True)
        st.success(f"🗑️ {prev['name']}님의 리포트가 삭제되었습니다.")
        st.rerun()
