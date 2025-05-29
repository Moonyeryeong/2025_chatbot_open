import streamlit as st
import os
import sys
import datetime
from utils import save_patient_info, load_patient_info, clear_glucose_data, clear_medications_data

if not st.session_state.get("logged_in", False):
    st.warning("🔒 로그인 해주세요.")
    st.stop()

username = st.session_state["username"]

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import save_patient_info, load_patient_info

st.markdown("""
<h2>📝 당뇨 개인정보 리포트</h2>
<p style="color:#555; margin-bottom:18px;">
건강 정보를 입력하고 맞춤 상담을 받아보세요.<br>
새로 검진 받은 결과나 겪은 증상을 입력하면 더 전문적인 챗봇 상담이 가능합니다.
</p>
""", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# 해당 유저의 기존 데이터 불러오기
all_users = load_patient_info(username)
if all_users:
    prev = all_users[0]
else:
    prev = {}

current_year = datetime.datetime.now().year
years = list(range(current_year, 1919, -1))

with st.form("user_info", clear_on_submit=False):
    st.markdown("### 👤 기본 정보")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("이름", value=prev.get("name", ""))
        birth_year = st.selectbox("출생년도", years, index=years.index(prev.get("birth_year")) if prev.get("birth_year") else 0)
        age = current_year - birth_year + 1
        gender = st.selectbox("성별", ["남성", "여성"], index=0 if prev.get("gender", "남성") == "남성" else 1)
    with col2:
        height = st.selectbox("키 (cm)", list(range(120, 200)), index=prev.get("height", 170)-120 if prev.get("height") else 50)
        weight = st.selectbox("몸무게 (kg)", list(range(30, 150)), index=prev.get("weight", 60)-30 if prev.get("weight") else 30)

    st.divider()
    st.markdown("### 🏃 생활 습관")
    daily_exercise = st.number_input("하루 평균 운동 시간 (분)", min_value=0, max_value=300, value=int(prev.get("daily_exercise", 30)))
    sleep_hours = st.number_input("하루 평균 수면 시간 (시간)", min_value=0, max_value=24, value=int(prev.get("sleep_hours", 7)))
    smoking = st.radio("흡연 여부", ["비흡연", "과거 흡연", "현재 흡연"], index=["비흡연", "과거 흡연", "현재 흡연"].index(prev.get("smoking", "비흡연")))
    alcohol = st.radio("음주 여부", ["비음주", "가끔", "자주"], index=["비음주", "가끔", "자주"].index(prev.get("alcohol", "비음주")))

    st.divider()
    st.markdown("### 🏥 진단 이력")
    diagnosis_years = st.number_input("당뇨 진단 이력 (년수)", min_value=0, max_value=100, value=int(prev.get("diagnosis_years", 0)))
    diabetes_type = st.selectbox("당뇨병 타입 (현재)", ["없음", "제1형", "제2형", "임신성"],
                                index=["없음", "제1형", "제2형", "임신성"].index(prev.get("diabetes_type", "없음")))
    complications = st.multiselect(
        "합병증 여부 (해당사항 모두 선택)",
        ["없음", "혈관", "신장", "신경", "급성"],
        default=prev.get("complications", ["없음"])
    )
    hemoglobin = st.number_input("당화혈색소 검사 (%)", min_value=0, max_value=20, value=int(prev.get("hemoglobin", 7)))

    st.divider()
    st.markdown("### ⚠️ 증상 및 자가 보고")
    recent_symptoms = st.text_area("최근 겪으신 증상이나 불편함을 작성해 주세요.", value=prev.get("recent_symptoms", ""))

    st.divider()
    st.markdown("### 🎯 목표 및 계획")
    target_weight = st.number_input("목표 체중 (kg)", min_value=30, max_value=200, value=int(prev.get("target_weight", weight)))
    target_glucose = st.number_input("목표 공복 혈당 (mg/dL)", min_value=50, max_value=300, value=int(prev.get("target_glucose", 100)))
    target_hba1c = st.number_input("목표 당화혈색소 (%)", min_value=3.0, max_value=15.0, step=0.1, value=float(prev.get("target_hba1c", 7)))

    submitted = st.form_submit_button("저장")

if submitted:
    user_data = {
        "name": name,
        "birth_year": birth_year,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "daily_exercise": daily_exercise,
        "sleep_hours": sleep_hours,
        "smoking": smoking,
        "alcohol": alcohol,
        "diagnosis_years": diagnosis_years,
        "diabetes_type": diabetes_type,
        "complications": complications,
        "hemoglobin": hemoglobin,
        "recent_symptoms": recent_symptoms,
        "target_weight": target_weight,
        "target_glucose": target_glucose,
        "target_hba1c": target_hba1c
    }

    all_users = [user_data]
    save_patient_info(username, all_users, overwrite=True)
    st.session_state["diabetes_report"] = user_data
    st.success(f"✅ {name}님의 리포트가 저장되었습니다!")

if all_users:
    if st.button("삭제"):
        all_users.clear()
        save_patient_info(username, all_users, overwrite=True)
        clear_glucose_data(username)
        clear_medications_data(username)
        st.success(f"🗑️ {prev['name']}님의 리포트 및 데이터가 삭제되었습니다.")
        st.rerun()
