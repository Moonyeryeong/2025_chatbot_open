# import streamlit as st
# import datetime
# import calendar
# import pandas as pd
# from utils import load_medications, save_medications


# if not st.session_state.get("logged_in", False):
#     st.warning("🔒 로그인 해주세요.")
#     st.stop()

# username = st.session_state["username"]
# user_id = username
# today = datetime.date.today()

# st.markdown("""
#     <h2>📋 복용약 관리</h2>
#     <p style="color:#555; margin-bottom:18px;"> 
#     복용하고 있는 약을 기록하세요.<br>
#     기록 된 복용약은 달력으로 확인하고 챗봇에게 맞춤 상담이 가능해요.
#     </p>
#     """, unsafe_allow_html=True)
# st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# #약 데이터 로드
# med_list = load_medications(user_id)
# med_df = pd.DataFrame(med_list)
# if not med_df.empty:
#     med_df["date"] = pd.to_datetime(med_df["복용 날짜"]).dt.date

# #입력 폼
# st.markdown("#### ✏️ 복용약 입력 ")
# diabetes_meds = [
#     "메트포르민", "설포닐유레아", "글리네이드",
#     "DPP-4 억제제", "SGLT-2 억제제", "GLP-1 수용체 작용제", "인슐린", "기타"
# ]
# with st.form("med_input_form"):
#     selected_meds = st.multiselect("약 이름(중복 선택 가능)", diabetes_meds)
#     custom_meds = []
#     if "기타" in selected_meds:
#         other_input = st.text_input("기타 약 입력 (쉼표로 구분)")
#         if other_input:
#             custom_meds = [name.strip() for name in other_input.split(",") if name.strip()]
#     final_meds = [m for m in selected_meds if m != "기타"] + custom_meds

#     med_date = st.date_input("복용 날짜", value=today)
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

# #월·날짜별 복용약 기록
# if med_list:
#     st.markdown("#### 📋 복용약 기록")

#     df = pd.DataFrame(med_list)
#     df["복용 날짜"] = pd.to_datetime(df["복용 날짜"])
#     df["year_month"] = df["복용 날짜"].dt.strftime("%Y-%m")
#     df["year_month_str"] = df["복용 날짜"].dt.strftime("%Y년 %m월")
#     df["date_str"] = df["복용 날짜"].dt.strftime("%Y-%m-%d")

#     col_month, col_date = st.columns([1.3, 2])
#     with col_month:
#         month_options = df["year_month"].unique()
#         month_labels = df.drop_duplicates("year_month")[["year_month", "year_month_str"]].set_index("year_month")["year_month_str"].to_dict()
#         month_choice = st.selectbox(
#             "년 월",
#             options=month_options,
#             format_func=lambda m: month_labels[m],
#             index=len(month_options)-1 
#         )

#     #선택 월의 날짜들만 뽑기
#     month_df = df[df["year_month"] == month_choice]
#     date_options = month_df["date_str"].unique()
#     with col_date:
#         date_choice = st.selectbox(
#             "날짜",
#             options=date_options,
#             format_func=lambda d: f"{d}",
#             index=len(date_options)-1  
#         )

#     #선택 날짜의 복용약 기록(삭제 포함)
#     date_df = month_df[month_df["date_str"] == date_choice].sort_values("복용 시간")
#     if not date_df.empty:
#         st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
#         st.markdown(f"##### 📅 {date_choice} ")
#         col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
#         with col1: st.markdown("**약 이름**")
#         with col2: st.markdown("**복용 날짜**")
#         with col3: st.markdown("**복용 시간**")
#         with col4: st.markdown("**비고**")
#         with col5: st.markdown("**삭제**")
#         for idx, row in date_df.iterrows():
#             col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
#             with col1: st.write(row["약 이름"])
#             with col2: st.write(row["date_str"])
#             with col3: st.write(row["복용 시간"])
#             with col4: st.write(row["비고"])
#             if col5.button("삭제", key=f"del_{row['약 이름']}_{row['date_str']}_{row['복용 시간']}_{idx}"):
#                 # 실제 데이터에서 삭제
#                 for i, m in enumerate(med_list):
#                     if (m["약 이름"] == row["약 이름"] and
#                         m["복용 날짜"] == row["date_str"] and
#                         m["복용 시간"] == row["복용 시간"]):
#                         med_list.pop(i)
#                         break
#                 save_medications(user_id, med_list)
#                 st.success("삭제되었습니다.")
#                 st.rerun()
#     else:
#         st.info("해당 날짜의 복용약 기록이 없습니다.")
# else:
#     st.info("복용약 정보를 입력해 주세요.")

# st.markdown("---")


# #캘린더 시각화
# st.markdown("#### 🗓️ 복용약 캘린더")
# st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

# #연도/월 선택
# years = list(range(today.year - 10, today.year + 2))
# if "calendar_year" not in st.session_state:
#     st.session_state.calendar_year = today.year
# if "calendar_month" not in st.session_state:
#     st.session_state.calendar_month = today.month

# c1, c2 = st.columns(2)
# with c1:
#     year = st.selectbox("년", years, index=years.index(st.session_state.calendar_year))
# with c2:
#     month = st.selectbox("월", list(range(1, 13)), index=st.session_state.calendar_month - 1)

# st.session_state.calendar_year = year
# st.session_state.calendar_month = month

# col_left, col_spacer, col_right = st.columns([1, 5, 1])
# with col_left:
#     if st.button("←", use_container_width=True):
#         if st.session_state.calendar_month == 1:
#             st.session_state.calendar_month = 12
#             st.session_state.calendar_year -= 1
#         else:
#             st.session_state.calendar_month -= 1
# with col_right:
#     if st.button("→", use_container_width=True):
#         if st.session_state.calendar_month == 12:
#             st.session_state.calendar_month = 1
#             st.session_state.calendar_year += 1
#         else:
#             st.session_state.calendar_month += 1

# if med_list:
#     med_names = sorted(set(m["약 이름"] for m in med_list))
#     selected_name = st.selectbox("🔍 약 필터링", ["전체 보기"] + med_names)
#     filtered_meds = med_list if selected_name == "전체 보기" else [m for m in med_list if m["약 이름"] == selected_name]

#     def style_medication(name, time):
#         med_colors = {
#             "메트포르민": "#FA8072", 
#             "설포닐유레아": "#9CAF88",
#             "글리네이드": "#A2B9BC", 
#             "DPP-4 억제제": "#FFD966", 
#             "SGLT-2 억제제": "#D8CAB8",  
#             "GLP-1 수용체 작용제": "#C3B1E1", 
#             "인슐린": "#3C4F76", 
#             "기타": "#C0C0C0", 
#         }
#         color = next((c for k, c in med_colors.items() if k in name), "#FA8072")  # fallback: salmon
#         hour = int(time[:2]) if time[:2].isdigit() else 9
#         icon = "🌞" if hour < 12 else "🌙"
#         return f"<span style='color:{color};'>{icon} {name} ({time})</span>"

#     def generate_calendar(year, month, meds):
#         cal = calendar.Calendar(firstweekday=6)
#         month_days = cal.monthdatescalendar(year, month)
#         med_df = pd.DataFrame(meds)
#         med_df["date"] = pd.to_datetime(med_df["복용 날짜"]).dt.date
#         grid = []

#         for week in month_days:
#             row = []
#             for day in week:
#                 meds_today = med_df[med_df["date"] == day]
#                 meds_text = "<br>".join(
#                     style_medication(row["약 이름"], row["복용 시간"])
#                     for _, row in meds_today.iterrows()
#                 )
#                 base_style = "padding: 10px; border-radius: 12px; height: 100%; width: 100%; display: block;"
#                 if day == today:
#                     cell_style = base_style + " background-color:#e0e0e0; color:#000;"
#                 elif day.weekday() == 6:
#                     cell_style = base_style + " color:#e74c3c;"
#                 elif day.weekday() == 5:
#                     cell_style = base_style + " color:#3498db;"
#                 else:
#                     cell_style = base_style

#                 if day.month == month:
#                     cell = f"<div style='{cell_style}'><b>{day.day}</b><br>{meds_text}</div>"
#                 else:
#                     cell = ""
#                 row.append(cell)
#             grid.append(row)
#         return grid

#     def render_html_calendar(grid):
#         days = ["일", "월", "화", "수", "목", "금", "토"]
#         html = """
#         <style>
#         table { border-collapse: separate; border-spacing: 8px; width: 100%; font-size: 0.95rem; }
#         th { background-color: #f0f4f8; color: #333; font-weight: bold; padding: 10px; border-radius: 6px; }
#         td {
#             vertical-align: top; padding: 0px; border: 1px solid #e0e0e0; border-radius: 12px;
#             min-width: 100px; height: 110px; background-color: #fafafa;
#             box-shadow: 1px 1px 3px rgba(0,0,0,0.05); word-break: break-word;
#         }
#         @media screen and (max-width: 768px) {
#             table, th, td { font-size: 12px; }
#             td { min-width: 60px; height: 80px; }
#         }
#         </style>
#         """
#         html += "<table><tr>" + "".join(f"<th>{d}</th>" for d in days) + "</tr>"
#         for week in grid:
#             html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in week) + "</tr>"
#         html += "</table>"
#         st.markdown(html, unsafe_allow_html=True)

#     cal_grid = generate_calendar(st.session_state.calendar_year, st.session_state.calendar_month, filtered_meds)
#     render_html_calendar(cal_grid)
# else:
#     st.info("복용 약 정보가 있어야 캘린더를 표시할 수 있습니다.")





import streamlit as st
import datetime
import calendar
import pandas as pd
from utils import load_medications, save_medications

# 로그인 확인
if not st.session_state.get("logged_in", False):
    st.warning("🔒 로그인 해주세요.")
    st.stop()

username = st.session_state["username"]
user_id = username
today = datetime.date.today()

st.markdown("""
     <h2>📋 복용약 관리</h2>
     <p style="color:#555; margin-bottom:18px;"> 
     복용하고 있는 약을 기록하세요.<br>
     기록 된 복용약은 달력으로 확인하고 챗봇에게 맞춤 상담이 가능해요.
     </p>
     """, unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# === 약 데이터 로드 ===
med_list = load_medications(user_id)

# ======= 복용약 정보 입력 =======
st.markdown("#### ✏️ 복용약 입력 ")
diabetes_meds = [
    "메트포르민", "설포닐유레아", "글리네이드",
    "DPP-4 억제제", "SGLT-2 억제제", "GLP-1 수용체 작용제", "인슐린", "기타"
]
selected_meds = st.multiselect("약 이름(중복 선택 가능)", diabetes_meds)

# 기타 입력란은 항상 표시하되, 기타 선택 시에만 값 사용
other_input = st.text_input("기타 약 입력 (쉼표로 구분)")
custom_meds = []
if other_input and "기타" in selected_meds:
    custom_meds = [name.strip() for name in other_input.split(",") if name.strip()]

# 최종 약 목록
final_meds = [m for m in selected_meds if m != "기타"] + custom_meds

# 복용 날짜, 시간, 메모 입력
med_date = st.date_input("복용 날짜", value=today)
med_time = st.time_input("복용 시간", value=datetime.time(9, 0))
med_memo = st.text_input("비고")

# 저장 버튼
if st.button("추가"):
    if final_meds:
        for med in final_meds:
            med_list.append({
                "약 이름": med,
                "복용 날짜": med_date.strftime("%Y-%m-%d"),
                "복용 시간": med_time.strftime("%H:%M"),
                "비고": med_memo
            })
        save_medications(user_id, med_list)
        st.success("💾 약 정보가 저장되었습니다.")
        # st.experimental_rerun()  # Streamlit rerun removed, state change will trigger update
    else:
        st.warning("저장할 약을 선택하거나 입력해주세요.")

st.markdown("---")

# === 월·날짜별 복용약 기록 ===
if med_list:
    st.markdown("#### 📋 복용약 기록")
    df = pd.DataFrame(med_list)
    df["복용 날짜"] = pd.to_datetime(df["복용 날짜"])
    df["year_month"] = df["복용 날짜"].dt.strftime("%Y-%m")
    df["year_month_str"] = df["복용 날짜"].dt.strftime("%Y년 %m월")
    df["date_str"] = df["복용 날짜"].dt.strftime("%Y-%m-%d")

    # 월/날짜 선택 UI
    col_month, col_date = st.columns([1.3, 2])
    with col_month:
        months = df["year_month"].unique()
        labels = df.drop_duplicates("year_month")[["year_month","year_month_str"]]
        labels = labels.set_index("year_month")["year_month_str"].to_dict()
        month_choice = st.selectbox("월별 보기", options=months,
                                    format_func=lambda m: labels[m],
                                    index=len(months)-1)
    with col_date:
        days = df[df["year_month"]==month_choice]["date_str"].unique()
        date_choice = st.selectbox("날짜 선택", options=days,
                                    format_func=lambda d: f"{d} 복용약 기록",
                                    index=len(days)-1)

    # 선택된 날짜 기록
    display_df = df[df["date_str"]==date_choice].sort_values("복용 시간")
    if not display_df.empty:
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        st.markdown(f"##### 🗓️ {date_choice}")
        cols = st.columns([2,2,2,2,1])
        for i, header in enumerate(["약 이름","복용 날짜","복용 시간","비고","삭제"]):
            cols[i].markdown(f"**{header}**")
        for idx, row in display_df.iterrows():
            c1,c2,c3,c4,c5 = st.columns([2,2,2,2,1])
            c1.write(row["약 이름"])
            c2.write(row["date_str"])
            c3.write(row["복용 시간"])
            c4.write(row["비고"])
            if c5.button("삭제", key=f"del_{idx}"):
                med_list.pop(idx)
                save_medications(user_id, med_list)
                st.success("삭제되었습니다.")
                st.rerun()
    else:
        st.info("해당 날짜의 복용약 기록이 없습니다.")
else:
    st.info("복용약 정보를 입력해 주세요.")
st.markdown("---")
# === 🗓️ 캘린더 시각화 ===
st.markdown("#### 🗓️ 복용약 캘린더")
st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

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
             "메트포르민": "#FA8072", 
             "설포닐유레아": "#9CAF88",
             "글리네이드": "#A2B9BC", 
             "DPP-4 억제제": "#FFD966", 
             "SGLT-2 억제제": "#D8CAB8",  
             "GLP-1 수용체 작용제": "#C3B1E1", 
             "인슐린": "#3C4F76", 
             "기타": "#C0C0C0", 
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