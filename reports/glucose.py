import streamlit as st
import datetime

st.set_page_config(page_title="혈당 관리", page_icon="🩸")
st.title("🩸 혈당 관리")
st.write("최근 혈당 수치를 기록하고, 변화를 모니터링하세요.")

sugar_data = st.session_state.get("sugar_data", [])

with st.form("sugar_input_form"):
    if sugar_data:
        last = sugar_data[-1]
        default_date = last["date"]
        default_time = last["time"]
        default_sugar = last["sugar"]
    else:
        default_date = datetime.date.today()
        default_time = datetime.time(9, 0)
        default_sugar = 100

    date = st.date_input("측정일자", value=default_date)
    time = st.time_input("측정시간", value=default_time)
    sugar = st.number_input("혈당(mg/dL)", min_value=30, max_value=600, value=int(default_sugar))
    submit = st.form_submit_button("저장")
    if submit:
        sugar_data.append({
            "date": date,
            "time": time,
            "sugar": sugar
        })
        st.session_state["sugar_data"] = sugar_data
        st.success("혈당 정보가 저장되었습니다.")

# ----- [여기부터 표처럼 출력] -----
if sugar_data:
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
    col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
    with col1: st.markdown("**날짜**")
    with col2: st.markdown("**시간**")
    with col3: st.markdown("**혈당**")
    with col4: st.markdown("**삭제**")
    # 표 데이터 행
    for i, entry in enumerate(sugar_data):
        col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
        with col1: st.write(str(entry["date"]))
        with col2: st.write(str(entry["time"]))
        with col3: st.write(f"{entry['sugar']} mg/dL")
        with col4:
            if st.button("삭제", key=f"delete_{i}"):
                sugar_data.pop(i)
                st.session_state["sugar_data"] = sugar_data
                st.rerun()
else:
    st.info("아직 혈당 기록이 없습니다. 데이터를 입력해 주세요.")
