import streamlit as st

# 이전 입력값이 있으면 불러오기 (없으면 빈 값)
prev = st.session_state.get("diabetes_report", {})

st.set_page_config(page_title="건강 리포트 입력", page_icon="📝")

st.markdown("<h2 style='text-align: center;'>📝 당뇨병 맞춤 건강 리포트</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>당신의 건강 상태를 기반으로 맞춤형 리포트를 생성해드립니다.</p>", unsafe_allow_html=True)

with st.form("user_info", clear_on_submit=False):
    st.markdown("### 👤 기본 정보")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("이름", value=prev.get("name", ""))
        age = st.selectbox("나이", options=list(range(20, 121)), index=prev.get("age", 20) - 20 if prev.get("age") else 0)
        gender = st.selectbox("성별", ["남성", "여성"], index=0 if prev.get("gender", "남성") == "남성" else 1)
    with col2:
        height = st.selectbox("키 (cm)", options=list(range(120, 251)), index=prev.get("height", 170)-120 if prev.get("height") else 0)
        weight = st.selectbox("몸무게 (kg)", options=list(range(30, 201)), index=prev.get("weight", 60)-30 if prev.get("weight") else 0)

    st.divider()
    st.markdown("### 🩸 건강 정보")

    col3, col4 = st.columns(2)
    with col3:
        fasting_glucose = st.number_input("공복 혈당 수치 (mg/dL)", min_value=50, max_value=300, value=int(prev.get("fasting_glucose", 100)))
        hba1c = st.number_input("당화혈색소 (%)", min_value=3.0, max_value=15.0, step=0.1, value=float(prev.get("hba1c", 5.6)))
    with col4:
        bp_systolic = st.number_input("혈압 (수축기 mmHg)", min_value=80, max_value=200, value=int(prev.get("bp_sys", 120)))
        bp_diastolic = st.number_input("혈압 (이완기 mmHg)", min_value=50, max_value=130, value=int(prev.get("bp_dia", 80)))

    st.divider()
    st.markdown("### 💊 복약 및 진단 이력")
    on_medication = st.radio("당뇨약 또는 인슐린 투여 중인가요?", ["예", "아니오"], index=0 if prev.get("on_medication", "아니오") == "예" else 1)
    diabetes_type = st.selectbox("진단받은 당뇨 유형이 있다면 선택해주세요", ["없음", "제1형", "제2형", "임신성"],
                                 index=["없음", "제1형", "제2형", "임신성"].index(prev.get("diabetes_type", "없음")))

    submitted = st.form_submit_button("✅ 리포트 제출")

if submitted:
    st.success("🎉 리포트 정보가 저장되었습니다!")
    st.session_state["diabetes_report"] = {
        "name": name,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "fasting_glucose": fasting_glucose,
        "hba1c": hba1c,
        "bp_sys": bp_systolic,
        "bp_dia": bp_diastolic,
        "on_medication": on_medication,
        "diabetes_type": diabetes_type
    }
