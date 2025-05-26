# import streamlit as st
# import datetime
# from utils import load_patient_info, load_medications, save_medications
# import plotly.express as px
# import pandas as pd

# if not st.session_state.get("logged_in", False):
#     st.warning("🔒 로그인 해주세요.")
#     st.stop()

# username = st.session_state["username"]
# user_id = username

# st.title("💊 복용약 관리")

# # 복약 데이터 로딩
# med_list = load_medications(user_id)

# # 입력 폼
# st.markdown("### ✏️ 복용약 정보 입력")
# diabetes_meds = [
#     "메트포르민", "글리메피리드", "글리클라지드", "글리벤클라미드",
#     "DPP-4 억제제", "SGLT-2 억제제", "GLP-1 유사체", "인슐린", "기타"
# ]

# with st.form("med_input_form"):
#     selected_meds = st.multiselect("약 이름(중복 선택 가능)", diabetes_meds)
#     custom_meds = []
#     if "기타" in selected_meds:
#         other_input = st.text_input("기타 약 입력 (쉼표로 구분)")
#         if other_input:
#             custom_meds = [name.strip() for name in other_input.split(",") if name.strip()]
#     final_meds = [m for m in selected_meds if m != "기타"] + custom_meds

#     med_date = st.date_input("복용 날짜", value=datetime.date.today())
#     med_time = st.time_input("복용 시간", value=datetime.time(9, 0))
#     med_memo = st.text_input("비고")

#     if st.form_submit_button("추가") and final_meds:
#         for med in final_meds:
#             med_list.append({
#                 "약 이름": med,
#                 "복용 날짜": med_date.strftime("%Y-%m-%d"),
#                 "복용 시간": med_time.strftime("%H:%M"),
#                 "비고": med_memo
#             })
#         save_medications(user_id, med_list)
#         st.success("💾 약 정보가 저장되었습니다.")
#         st.rerun()
# st.markdown("---")

# # 복용중인 약 목록
# if med_list:
#     st.markdown("#### 📋 복용약 기록")
#     col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
#     with col1: st.markdown("**약 이름**")
#     with col2: st.markdown("**복용 날짜**")
#     with col3: st.markdown("**복용 시간**")
#     with col4: st.markdown("**비고**")
#     with col5: st.markdown("**삭제**")

#     for i, med in enumerate(med_list):
#         col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
#         with col1: st.write(med["약 이름"])
#         with col2: st.write(med["복용 날짜"])
#         with col3: st.write(med["복용 시간"])
#         with col4: st.write(med.get("비고", ""))
#         with col5:
#             if st.button("삭제", key=f"del_{i}"):
#                 med_list.pop(i)
#                 save_medications(user_id, med_list)
#                 st.rerun()
# else:
#     st.info("복용중인 약 정보를 입력해 주세요.")

# st.markdown("---")


import streamlit as st
import datetime
import calendar
import pandas as pd
from utils import load_medications, save_medications

if not st.session_state.get("logged_in", False):
    st.warning("🔒 로그인 해주세요.")
    st.stop()

username = st.session_state["username"]
user_id = username
today = datetime.date.today()

st.title("💊 복용약 관리")

# === 약 데이터 로드 ===
med_list = load_medications(user_id)

# === 입력 폼 ===
st.markdown("### ✏️ 복용약 정보 입력")
diabetes_meds = [
    "메트포르민", "글리메피리드", "글리클라지드", "글리벤클라미드",
    "DPP-4 억제제", "SGLT-2 억제제", "GLP-1 유사체", "인슐린", "기타"
]

with st.form("med_input_form"):
    selected_meds = st.multiselect("약 이름(중복 선택 가능)", diabetes_meds)
    custom_meds = []
    if "기타" in selected_meds:
        other_input = st.text_input("기타 약 입력 (쉼표로 구분)")
        if other_input:
            custom_meds = [name.strip() for name in other_input.split(",") if name.strip()]
    final_meds = [m for m in selected_meds if m != "기타"] + custom_meds

    med_date = st.date_input("복용 날짜", value=today)
    med_time = st.time_input("복용 시간", value=datetime.time(9, 0))
    med_memo = st.text_input("비고")

    if st.form_submit_button("추가") and final_meds:
        for med in final_meds:
            med_list.append({
                "약 이름": med,
                "복용 날짜": med_date.strftime("%Y-%m-%d"),
                "복용 시간": med_time.strftime("%H:%M"),
                "비고": med_memo
            })
        save_medications(user_id, med_list)
        st.success("💾 약 정보가 저장되었습니다.")
        st.rerun()

st.markdown("---")

# === 약 목록 표시 ===
if med_list:
    st.markdown("#### 📋 복용약 기록")
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    with col1: st.markdown("**약 이름**")
    with col2: st.markdown("**복용 날짜**")
    with col3: st.markdown("**복용 시간**")
    with col4: st.markdown("**비고**")
    with col5: st.markdown("**삭제**")

    for i, med in enumerate(med_list):
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        with col1: st.write(med["약 이름"])
        with col2: st.write(med["복용 날짜"])
        with col3: st.write(med["복용 시간"])
        with col4: st.write(med.get("비고", ""))
        with col5:
            if st.button("삭제", key=f"del_{i}"):
                med_list.pop(i)
                save_medications(user_id, med_list)
                st.rerun()
else:
    st.info("복용중인 약 정보를 입력해 주세요.")

st.markdown("---")

# === 🗓️ 캘린더 시각화 ===
st.markdown("#### 🗓️ 약 복용 일정 캘린더")

# 연도/월 선택
years = list(range(today.year - 10, today.year + 2))
if "calendar_year" not in st.session_state:
    st.session_state.calendar_year = today.year
if "calendar_month" not in st.session_state:
    st.session_state.calendar_month = today.month

c1, c2 = st.columns(2)
with c1:
    year = st.selectbox("년도 선택", years, index=years.index(st.session_state.calendar_year))
with c2:
    month = st.selectbox("월 선택", list(range(1, 13)), index=st.session_state.calendar_month - 1)

st.session_state.calendar_year = year
st.session_state.calendar_month = month

col_left, col_spacer, col_right = st.columns([1, 5, 1])
with col_left:
    if st.button("←", use_container_width=True):
        if st.session_state.calendar_month == 1:
            st.session_state.calendar_month = 12
            st.session_state.calendar_year -= 1
        else:
            st.session_state.calendar_month -= 1
with col_right:
    if st.button("→", use_container_width=True):
        if st.session_state.calendar_month == 12:
            st.session_state.calendar_month = 1
            st.session_state.calendar_year += 1
        else:
            st.session_state.calendar_month += 1

if med_list:
    med_names = sorted(set(m["약 이름"] for m in med_list))
    selected_name = st.selectbox("🔍 특정 약 이름으로 필터링", ["전체 보기"] + med_names)
    filtered_meds = med_list if selected_name == "전체 보기" else [m for m in med_list if m["약 이름"] == selected_name]

    def style_medication(name, time):
        med_colors = {
            "메트포르민": "#2980b9", "글리메피리드": "#27ae60", "글리클라지드": "#8e44ad",
            "글리벤클라미드": "#f39c12", "DPP-4 억제제": "#d35400", "SGLT-2 억제제": "#16a085",
            "GLP-1 유사체": "#34495e", "인슐린": "#e74c3c", "기타": "#7f8c8d"
        }
        color = next((c for k, c in med_colors.items() if k in name), "#2b7de9")
        hour = int(time[:2]) if time[:2].isdigit() else 9
        icon = "🌞" if hour < 12 else "🌙"
        return f"<span style='color: {color}; font-weight: bold;'>{icon} {name} ({time})</span>"

    def generate_calendar(year, month, meds):
        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdatescalendar(year, month)
        med_df = pd.DataFrame(meds)
        med_df["date"] = pd.to_datetime(med_df["복용 날짜"]).dt.date
        grid = []

        for week in month_days:
            row = []
            for day in week:
                meds_today = med_df[med_df["date"] == day]
                meds_text = "<br>".join(
                    style_medication(row["약 이름"], row["복용 시간"])
                    for _, row in meds_today.iterrows()
                )
                base_style = "padding: 10px; border-radius: 12px; height: 100%; width: 100%; display: block;"
                if day == today:
                    cell_style = base_style + " background-color:#e0e0e0; color:#000;"
                elif day.weekday() == 6:
                    cell_style = base_style + " color:#e74c3c;"
                elif day.weekday() == 5:
                    cell_style = base_style + " color:#3498db;"
                else:
                    cell_style = base_style

                if day.month == month:
                    cell = f"<div style='{cell_style}'><b>{day.day}</b><br>{meds_text}</div>"
                else:
                    cell = ""
                row.append(cell)
            grid.append(row)
        return grid

    def render_html_calendar(grid):
        days = ["일", "월", "화", "수", "목", "금", "토"]
        html = """
        <style>
        table { border-collapse: separate; border-spacing: 8px; width: 100%; font-size: 0.95rem; }
        th { background-color: #f0f4f8; color: #333; font-weight: bold; padding: 10px; border-radius: 6px; }
        td {
            vertical-align: top; padding: 0px; border: 1px solid #e0e0e0; border-radius: 12px;
            min-width: 100px; height: 110px; background-color: #fafafa;
            box-shadow: 1px 1px 3px rgba(0,0,0,0.05); word-break: break-word;
        }
        @media screen and (max-width: 768px) {
            table, th, td { font-size: 12px; }
            td { min-width: 60px; height: 80px; }
        }
        </style>
        """
        html += "<table><tr>" + "".join(f"<th>{d}</th>" for d in days) + "</tr>"
        for week in grid:
            html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in week) + "</tr>"
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)

    cal_grid = generate_calendar(st.session_state.calendar_year, st.session_state.calendar_month, filtered_meds)
    render_html_calendar(cal_grid)
else:
    st.info("복용 약 정보가 있어야 캘린더를 표시할 수 있습니다.")

