import streamlit as st
import json
import pandas as pd
import altair as alt
from utils import load_patient_info, load_medications

if not st.session_state.get("logged_in", False):
    st.warning("🔒 로그인 해주세요.")
    st.stop()

username = st.session_state["username"]
data_list = load_patient_info(username)
med_list = load_medications(username)

# 혈당 데이터 불러오기
try:
    with open("data/glucose.json", "r", encoding="utf-8") as f:
        all_glucose_data = json.load(f)
    glucose_data = all_glucose_data.get(username, [])
except:
    glucose_data = []

if not data_list:
    st.warning("⚠️ [개인정보] 탭에서 먼저 정보를 입력해 주세요.")
    st.stop()

data = data_list[0]

st.markdown("<h2>📊 건강 리포트</h2>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# 개인 정보
st.markdown("#### 👤 기본 정보")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**나이:** {data['age']}세")
    st.write(f"**성별:** {data['gender']}")
    st.write(f"**키 / 몸무게:** {data['height']} cm / {data['weight']} kg")
    st.write(f"**흡연 여부:** {data['smoking']}")
    st.write(f"**음주 여부:** {data['alcohol']}")
with col2:
    st.write(f"**하루 평균 운동:** {data['daily_exercise']} 분")
    st.write(f"**하루 평균 수면:** {data['sleep_hours']} 시간")
    st.write(f"**목표 체중:** {data['target_weight']} kg")
    st.write(f"**목표 공복 혈당:** {data['target_glucose']} mg/dL")
    st.write(f"**목표 당화혈색소:** {data['target_hba1c']}%")

st.divider()

# 최근 검사 및 혈당
st.markdown("#### 🏥 진단 이력")
st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

st.write(f"**당뇨병 진단받은 지:** {data.get('diagnosis_years', '미입력')} 년째")
st.write(f"**현재 당뇨병 타입:** {data.get('diabetes_type', '미입력')}")
comp_list = ", ".join(data.get("complications", ["미입력"]))
st.write(f"**합병증 여부:** {comp_list}")
st.write(f"**최근 당화혈색소:** {data['hemoglobin']} %")
st.write(f"**최근 보고된 증상:** {data['recent_symptoms'] or '없음'}")

st.divider()

# BMI
st.markdown("#### 📐 체질량지수 (BMI)")
st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

height_m = data["height"] / 100
bmi = data["weight"] / (height_m ** 2)
if bmi < 18.5:
    bmi_category = "저체중"
elif bmi < 23:
    bmi_category = "정상 체중"
elif bmi < 25:
    bmi_category = "과체중"
elif bmi < 30:
    bmi_category = "비만 1단계"
else:
    bmi_category = "고도비만"
st.write(f"**BMI:** `{bmi:.1f}`")
st.write(f"**판정:** `{bmi_category}`")

st.divider()

st.info("🤖 더 궁금한 점이 있다면 챗봇에게 질문하세요!")