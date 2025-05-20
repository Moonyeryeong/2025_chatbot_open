import streamlit as st
import datetime

st.set_page_config(page_title="복용중인 약", page_icon="💊")
st.title("💊 복용중인 약")

# 이전 값 불러오기 (없으면 빈 리스트)
med_list = st.session_state.get("med_list", [])

diabetes_meds = [
    "메트포르민", "글리메피리드", "글리클라지드", "글리벤클라미드", 
    "DPP-4 억제제", "SGLT-2 억제제", "GLP-1 유사체", "인슐린", "기타"
]

with st.form("med_input_form"):
    # 최근에 추가된 값 불러와서 기본값으로 세팅
    if med_list:
        last = med_list[-1]
        default_meds = [last["약 이름"]] if last["약 이름"] in diabetes_meds else []
        default_custom = last["약 이름"] if last["약 이름"] not in diabetes_meds else ""
        default_date = datetime.datetime.strptime(last["복용 날짜"], "%Y-%m-%d").date()
        default_time = datetime.datetime.strptime(last["복용 시간"], "%H:%M").time()
        default_memo = last["비고"]
    else:
        default_meds, default_custom, default_date, default_time, default_memo = [], "", datetime.date.today(), datetime.time(9, 0), ""

    selected_meds = st.multiselect("약 이름(중복 선택 가능)", diabetes_meds, default=default_meds)
    custom_meds = []
    if "기타" in selected_meds:
        st.info("아래 입력란에 기타 약 이름을 입력해 주세요. 여러 개면 쉼표(,)로 구분")
        other_input = st.text_input("기타 약 이름 입력", value=default_custom)
        if other_input:
            custom_meds = [name.strip() for name in other_input.split(",") if name.strip()]
    final_meds = [med for med in selected_meds if med != "기타"] + custom_meds

    med_date = st.date_input("복용 날짜", value=default_date)
    med_time = st.time_input("복용 시간", value=default_time, step=300)
    med_memo = st.text_input("비고(필요시)", value=default_memo)
    submit = st.form_submit_button("추가")
    if submit and final_meds:
        for med in final_meds:
            med_list.append({
                "약 이름": med,
                "복용 날짜": med_date.strftime("%Y-%m-%d"),
                "복용 시간": med_time.strftime("%H:%M"),
                "비고": med_memo
            })
        st.session_state["med_list"] = med_list
        st.success("약 정보가 추가되었습니다.")

# 표 형식 + 행별 삭제 버튼
if med_list:
    st.markdown("#### 복용 중인 약 목록")
    col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
    with col1: st.markdown("**약 이름**")
    with col2: st.markdown("**복용 시간**")
    with col3: st.markdown("**비고**")
    with col4: st.markdown("**삭제**")
    for i, med in enumerate(med_list):
        col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
        with col1: st.write(med["약 이름"])
        with col2: st.write(med["복용 시간"])
        with col3: st.write(med["비고"])
        with col4:
            if st.button("삭제", key=f"del_{i}"):
                med_list.pop(i)
                st.session_state["med_list"] = med_list
                st.rerun()
else:
    st.info("복용 중인 약 정보를 등록해 주세요.")
