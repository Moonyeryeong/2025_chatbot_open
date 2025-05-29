import streamlit as st
import datetime
import os
import json
import pandas as pd
import altair as alt

# 로그인 확인
if not st.session_state.get("logged_in", False):
    st.warning("🔒 로그인 해주세요.")
    st.stop()

username = st.session_state["username"]
user_id = username
today = datetime.date.today()

st.markdown("""
<h2>🩸 혈당 관리</h2>
<p style="color:#555; margin-bottom:18px;">
혈당을 측정하고 기록하세요.<br>
혈당 추적과 기록을 통해 변화를 확인하고 목표 혈당을 이루었는지 확인하세요.
</p>
""", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

#데이터 파일 로드
data_path = "data/glucose.json"
os.makedirs("data", exist_ok=True)
try:
    with open(data_path, "r", encoding="utf-8") as f:
        all_data = json.load(f)
except:
    all_data = {}

user_data = all_data.get(user_id, [])

st.markdown("#### ✏️ 혈당 입력 ")

#입력 폼
with st.form("glucose_form"):
    date = st.date_input("측정일자", value=today)
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
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        st.success("✅ 혈당 정보가 저장되었습니다.")
        st.rerun()

#월/날짜/년 선택 & 기록 
if user_data:
    st.markdown("---")
    st.markdown("#### 📋 혈당 기록")
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

    df = pd.DataFrame(user_data)
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df.sort_values(["date", "time"], inplace=True)

   #년도 선택
    df["year"] = df["date"].apply(lambda x: x.year)
    years = sorted(df["year"].unique())
    default_year_idx = years.index(today.year) if today.year in years else len(years)-1

    col_year, col_month, col_date = st.columns([1, 1.3, 2])

    with col_year:
        selected_year = st.selectbox(
            "년도", years,
            format_func=lambda y: f"{y}년",  
            index=default_year_idx,
            key="glucose_year"
        )

    #월 선택
    month_df = df[df["year"] == selected_year]
    months = sorted(month_df["date"].apply(lambda x: x.month).unique())
    default_month = today.month if today.month in months else months[-1]
    month_labels = {m: f"{m:02d}월" for m in months}
    with col_month:
        selected_month = st.selectbox(
            "월", months, format_func=lambda m: month_labels[m], index=months.index(default_month), key="glucose_month"
        )

    #날짜 선택 (선택한 년/월에 한함)
    date_df = month_df[month_df["date"].apply(lambda d: d.month == selected_month)]
    dates = sorted(date_df["date"].unique())
    # 기본값: 오늘 날짜 → 없으면 최신일
    if today in dates:
        default_date_idx = dates.index(today)
    else:
        default_date_idx = len(dates)-1 if dates else 0
    date_labels = {d: f"{d.strftime('%d일')}" for d in dates}
    with col_date:
        if dates:
            selected_date = st.selectbox(
                "날짜", dates, format_func=lambda d: date_labels[d], index=default_date_idx, key="glucose_date"
            )
        else:
            selected_date = None
            st.info("선택한 월에 혈당 기록이 없습니다.")

    #선택 날짜의 혈당 기록 표시 및 삭제
    if selected_date:
        daily_df = date_df[date_df["date"] == selected_date].sort_values("time")
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        st.markdown(f"##### 📅 {selected_date}")
        col_time, col_glucose, col_delete = st.columns([2, 2, 1])
        col_time.markdown("**측정 시각**")
        col_glucose.markdown("**혈당 (mg/dL)**")
        col_delete.markdown("**삭제**")
        for idx, row in daily_df.iterrows():
            col_time, col_glucose, col_delete = st.columns([2, 2, 1])
            col_time.write(str(row["time"]))
            col_glucose.write(str(row["glucose"]))
            if col_delete.button("삭제", key=f"delete_{row['date']}_{row['time']}"):
                # 삭제
                user_data = [
                    d for d in user_data
                    if not (d["date"] == row["date"].strftime("%Y-%m-%d") and d["time"] == row["time"])
                ]
                all_data[user_id] = user_data
                with open(data_path, "w", encoding="utf-8") as f:
                    json.dump(all_data, f, ensure_ascii=False, indent=2)
                st.success("삭제되었습니다.")
                st.rerun()
    else:
        st.info("해당 날짜의 기록이 없습니다.")

    st.markdown("---")

    #월별 혈당 변화 그래프
    month_label = f"{selected_year}년 {selected_month:02d}월"
    st.markdown(f"#### <span>📊 {month_label} 혈당 변화 그래프</span>", unsafe_allow_html=True)
    df_plot = date_df.copy()

    if not df_plot.empty:
        hover = alt.selection_single(fields=["datetime"], nearest=True, on="mouseover", empty="none", clear="mouseout")

        line = alt.Chart(df_plot).mark_line(
            color="#FF6F61",
            strokeWidth=2
        ).encode(
            x=alt.X("datetime:T", title="날짜/시간"),
            y=alt.Y("glucose:Q", title="혈당 (mg/dL)")
        )

        points = alt.Chart(df_plot).mark_circle(size=65, color="#FF6F61").encode(
            x="datetime:T",
            y="glucose:Q",
            tooltip=[
                alt.Tooltip("datetime:T", title="날짜/시간"),
                alt.Tooltip("glucose:Q", title="혈당")
            ]
        ).add_params(hover).transform_filter(hover)

        # 기준선 및 레이블
        low_line = alt.Chart(pd.DataFrame({"y": [126]})).mark_rule(color="#87CEEB", strokeDash=[4, 2]).encode(y="y:Q")
        high_line = alt.Chart(pd.DataFrame({"y": [200]})).mark_rule(color="#98FB98", strokeDash=[4, 2]).encode(y="y:Q")
        low_label = alt.Chart(pd.DataFrame({"y": [125]})).mark_text(align="left", dx=5, dy=-5, color="#87CEEB").encode(y="y:Q", text=alt.value("공복 기준 (126)"))
        high_label = alt.Chart(pd.DataFrame({"y": [200]})).mark_text(align="left", dx=5, dy=-5, color="#98FB98").encode(y="y:Q", text=alt.value("식후 2시간 기준 (200)"))
        chart = (line + points + low_line + high_line + low_label + high_label).properties(
            width=700,
            height=350
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("선택한 월에는 혈당 데이터가 없습니다.")

else:
    st.info("아직 혈당 기록이 없습니다. 데이터를 입력해 주세요.")

st.markdown("---")
#목표 혈당 안내
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