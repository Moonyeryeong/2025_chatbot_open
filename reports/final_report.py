import streamlit as st

st.set_page_config(page_title="건강 리포트", page_icon="📊")

st.markdown("<h2 style='text-align: center;'>📊 건강 리포트</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>입력한 정보를 바탕으로 당신에게 맞는 건강 관리 전략을 제안합니다.</p>", unsafe_allow_html=True)

if "diabetes_report" not in st.session_state:
    st.warning("⚠️ 먼저 '보고서 입력' 페이지에서 정보를 입력해주세요.")
else:
    data = st.session_state["diabetes_report"]

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

    # BMI 계산 및 해석
    st.markdown("#### 📐 체질량지수 (BMI) 분석")
    height_m = data['height'] / 100
    bmi = data['weight'] / (height_m ** 2)
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
    st.markdown("💬 더 궁금한 점이 있다면 **[챗봇 탭]**을 통해 질문해보세요!")
