import streamlit as st
from utils import load_patient_info, load_medications

if not st.session_state.get("logged_in", False):
    st.warning("🔒 로그인 해주세요.")
    st.stop()

username = st.session_state["username"]
data_list = load_patient_info(username)


if not data_list:
    st.warning("⚠️ 먼저 [개인정보] 탭에서 정보를 입력해 주세요.")
    st.stop()

data = data_list[0]
user_id = username

st.markdown("<h2>📊 건강 리포트</h2>", unsafe_allow_html=True)
st.success(f"🔍 현재 로그인된 사용자: {data['name']}")

st.markdown(f"#### 👤 {data['name']}님의 건강 요약")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**나이:** {data['age']}세")
    st.write(f"**성별:** {data['gender']}")
    st.write(f"**키 / 몸무게:** {data['height']} cm / {data['weight']} kg")
with col2:
    st.write(f"**공복 혈당:** {data['fasting_glucose']} mg/dL")
    st.write(f"**당화혈색소(HbA1c):** {data['hba1c']}%")
    st.write(f"**혈압:** {data['bp_sys']} / {data['bp_dia']} mmHg")

st.divider()

# BMI 계산 및 분석
st.markdown("#### 📐 체질량지수 (BMI) 분석")
height_m = data["height"] / 100
bmi = data["weight"] / (height_m ** 2)

if bmi < 18.5:
    bmi_category = "저체중"
    risk_msg = "당뇨병 위험은 낮지만, 영양 상태를 점검할 필요가 있습니다."
elif bmi < 23:
    bmi_category = "정상 체중"
    risk_msg = "당뇨병 위험이 낮은 건강한 체중입니다. 잘 유지하세요!"
elif bmi < 25:
    bmi_category = "과체중"
    risk_msg = "당뇨병 위험이 다소 증가할 수 있습니다. 체중 관리에 주의하세요."
elif bmi < 30:
    bmi_category = "비만 1단계"
    risk_msg = "당뇨병 위험이 높습니다. 식이조절과 운동이 필요합니다."
else:
    bmi_category = "고도비만"
    risk_msg = "당뇨병 위험이 매우 높습니다. 적극적인 체중 감량이 권장됩니다."

st.write(f"**BMI:** `{bmi:.1f}`")
st.write(f"**판정:** `{bmi_category}`")
st.info(risk_msg)

st.divider()

# 복용중인 약 출력
st.markdown("#### 💊 복용중인 약 목록")
med_list = load_medications(user_id)

if med_list:
    for med in med_list:
        st.write(f"- {med['복용 날짜']} {med['복용 시간']} - **{med['약 이름']}** | {med.get('비고', '')}")
else:
    st.info("해당 사용자에 대한 복용 약 정보가 없습니다.")

st.divider()
st.markdown("💬 더 궁금한 점이 있다면 [챗봇]을 통해 질문해보세요!")