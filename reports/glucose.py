import streamlit as st
import datetime
import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
from utils import load_patient_info

if not st.session_state.get("logged_in", False):
    st.warning("🔒 로그인 해주세요.")
    st.stop()

username = st.session_state["username"]
user_id = username  # 유저 ID로 로그인 ID 사용

st.title("🩸 혈당 관리")

# 파일 경로
path = "data/glucose.json"
os.makedirs("data", exist_ok=True)

# 데이터 불러오기
try:
    with open(path, "r", encoding="utf-8") as f:
        all_data = json.load(f)
except:
    all_data = {}

user_data = all_data.get(user_id, [])

# 입력 폼
with st.form("glucose_form"):
    date = st.date_input("측정일자", value=datetime.date.today())
    time = st.time_input("측정시간", value=datetime.time(9, 0))
    glucose = st.number_input("혈당(mg/dL)", min_value=0, max_value=500, value=100)
    submit = st.form_submit_button("저장")

    if submit:
        new_entry = {
            "date": str(date),
            "time": time.strftime("%H:%M"),
            "glucose": glucose
        }
        user_data = [d for d in user_data if not (d["date"] == new_entry["date"] and d["time"] == new_entry["time"])]
        user_data.append(new_entry)
        user_data.sort(key=lambda x: x["date"] + x["time"])
        all_data[user_id] = user_data
        with open(path, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        st.success("✅ 혈당 정보가 저장되었습니다.")
        st.rerun()

# 시각화 및 삭제

if user_data:
    st.markdown("""
        <style>
        .sugar-table th, .sugar-table td {
            padding: 8px 16px;
            text-align: center;
            font-size: 1.05em;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 표 헤더
    st.markdown("---")
    st.markdown("#### 📋 혈당 기록")
    col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
    with col1: st.markdown("**날짜**")
    with col2: st.markdown("**시간**")
    with col3: st.markdown("**혈당**")
    with col4: st.markdown("**삭제**")

    # 표 데이터 행
    for i, entry in enumerate(user_data):
        col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
        with col1: st.write(str(entry["date"]))
        with col2: st.write(str(entry["time"]))
        with col3: st.write(f"{entry['glucose']} mg/dL")
        with col4:
            if st.button("삭제", key=f"delete_{i}"):
                user_data.pop(i)
                all_data[user_id] = user_data
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(all_data, f, ensure_ascii=False, indent=2)
                st.rerun()

    # Altair 시각화 준비
    df = pd.DataFrame(user_data)
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])
    df.sort_values("datetime", inplace=True)

    st.markdown("---")
    st.markdown("#### 📊 혈당 변화 그래프")

    # 기본 라인 차트
    line = alt.Chart(df).mark_line(
        color="#FF6F61",
        strokeWidth=2
    ).encode(
        x=alt.X("datetime:T", title="날짜/시간"),
        y=alt.Y("glucose:Q", title="혈당 (mg/dL)")
    )

    # 마우스 hover 마커용 selector
    hover = alt.selection_single(
        fields=["datetime"],
        nearest=True,
        on="mouseover",
        empty="none",
        clear="mouseout"
    )

    # Hover 시 마커 표시 
    points = alt.Chart(df).mark_circle(size=65, color="#FF6F61").encode(
        x="datetime:T",
        y="glucose:Q",
        tooltip=[
            alt.Tooltip("datetime:T", title="날짜/시간"),
            alt.Tooltip("glucose:Q", title="혈당")
        ]
    ).add_selection(hover).transform_filter(hover)

    # 기준선
    low_line = alt.Chart(pd.DataFrame({"y": [126]})).mark_rule(
        color="#87CEEB", strokeDash=[4, 2]
    ).encode(y="y:Q")

    high_line = alt.Chart(pd.DataFrame({"y": [200]})).mark_rule(
        color="#98FB98", strokeDash=[4, 2]
    ).encode(y="y:Q")

    # 기준선 라벨
    low_label = alt.Chart(pd.DataFrame({"y": [125]})).mark_text(
        align="left", dx=5, dy=-5, color="#87CEEB"
    ).encode(
        y="y:Q",
        text=alt.value("공복 기준 (126)")
    )

    high_label = alt.Chart(pd.DataFrame({"y": [200]})).mark_text(
        align="left", dx=5, dy=-5, color="#98FB98"
    ).encode(
        y="y:Q",
        text=alt.value("식후 2시간 기준 (200)")
    )

    # 최종 차트 조합
    chart = (line + points + low_line + high_line + low_label + high_label).properties(
        width=700,
        height=350
    ).interactive()

    # 출력
    st.altair_chart(chart, use_container_width=True)

else:
    st.info("아직 혈당 기록이 없습니다. 데이터를 입력해 주세요.")
st.markdown("---")

#목표혈당 안내
st.markdown("#### 🎯목표 혈당")
st.markdown("목표 혈당에 달성했는지 확인하세요!")
st.markdown("""
<table style="width:100%; border-collapse: collapse;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="text-align:center; padding:8px; border:1px solid #ddd;">구분</th>
      <th style="text-align:center; padding:8px; border:1px solid #ddd;">정상수치</th>
      <th style="text-align:center; padding:8px; border:1px solid #ddd;">조절목표</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:center; padding:8px; border:1px solid #ddd;">공복혈당</td>
      <td style="text-align:center; padding:8px; border:1px solid #ddd;">70~100 mg/dL</td>
      <td style="text-align:center; padding:8px; border:1px solid #ddd;">80~130 mg/dL</td>
    </tr>
    <tr>
      <td style="text-align:center; padding:8px; border:1px solid #ddd;">식후 2시간 혈당</td>
      <td style="text-align:center; padding:8px; border:1px solid #ddd;">90~140 mg/dL</td>
      <td style="text-align:center; padding:8px; border:1px solid #ddd;">&lt;180 mg/dL</td>
    </tr>
    <tr>
      <td style="text-align:center; padding:8px; border:1px solid #ddd;">당화혈색소</td>
      <td style="text-align:center; padding:8px; border:1px solid #ddd;">5.7% 미만</td>
      <td style="text-align:center; padding:8px; border:1px solid #ddd;">6.5% 미만</td>
    </tr>
  </tbody>
</table>
""", unsafe_allow_html=True)

