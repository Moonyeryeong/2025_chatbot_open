import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
from openai import OpenAI
import requests

# 로그인 확인
if not st.session_state.get("logged_in", False):
    st.warning("🔒 로그인 해주세요.")
    st.stop()

# 경로 및 권장값
DATA_PATH = "data/diet.json"
RECOMMENDED_CARBS = 250  # g
RECOMMENDED_SUGAR = 50   # g
RECOMMENDED_PROTEIN = 60 # g
RECOMMENDED_FAT = 70     # g

# ✅ 초기 상태 설정
for key in ["carbs_value", "protein_value", "fat_value"]:
    if key not in st.session_state:
        st.session_state[key] = 0

import pandas as pd

# ✅ 엑셀에서 영양소 데이터 불러오기 함수
def fetch_nutrition_from_csv(food):
    csv_path = "data/20250408_음식DB.csv"
    try:
        df = pd.read_csv(csv_path)

        # 1️⃣ food in CSV → ex: '치즈김밥' in '김밥_치즈'
        result = df[df["식품명"].str.contains(food, case=False, na=False)]

        # 2️⃣ CSV in food → ex: '김밥_치즈' in '치즈김밥'
        if result.empty:
            result = df[df["식품명"].apply(lambda x: food in x or x in food)]

        if not result.empty:
            row = result.iloc[0]
            return {
                "탄수화물": int(row["탄수화물(g)"]),
                "단백질": int(row["단백질(g)"]),
                "지방": int(row["지방(g)"])
            }
        else:
            st.warning(f"⚠️ CSV에 '{food}' 데이터가 없습니다.")
            return None
    except Exception as e:
        st.warning(f"⚠️ csv 파일 불러오기 실패: {e}")
        return None



def ask_gpt_nutrition_info(food):
    # 먼저 CSV에서 시도
    csv_result = fetch_nutrition_from_csv(food)
    if csv_result:
        return csv_result

    # 실패하면 GPT로 fallback
    system_prompt = (
        "당신은 영양 성분 전문가입니다. "
        "사용자가 요청한 음식의 100g당 평균 탄수화물(g), 단백질(g), 지방(g)을 한국 식품 성분 기준으로 정확히 제공합니다. "
        "출력은 반드시 아래 JSON 형식만 사용하고, 다른 설명이나 말은 절대 하지 마세요. "
        "{\"탄수화물\": 숫자, \"단백질\": 숫자, \"지방\": 숫자}"
    )
    
    user_prompt = (
        f"{food} 음식의 100g당 평균 탄수화물, 단백질, 지방 값을 알려주세요."
    )

    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        st.error(f"⚠️ GPT 영양 정보를 불러오는 데 실패했습니다: {e}")
        return None


# 데이터 입출력 함수
def load_diet_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_diet_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 사용자 불러오기
username = st.session_state.get("username", "guest")
diet_data = load_diet_data()
user_data = diet_data.get(username, {})

#입력 영역
st.markdown("""
    <h2>🍽️ 식단 관리 </h2>
    <p style="color:#555; margin-bottom:18px;"> 
    날짜와 시간을 선택하고 음식을 입력하세요.<br>
    먹은 음식의 영양소를 기록해 하루에 섭취한 영양소를 확인하세요.
    </p>
    """, unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)


st.markdown("#### ✏️ 식단 입력 ")
# === 자동 영양소 입력 폼 ===
with st.form("nutrition_form"):
    food_for_nutrition = st.text_input("먹은 음식", key="nutrition_food")
    nutrition_submit = st.form_submit_button("🔍 영양소 자동 입력")
    if nutrition_submit:
        nutrition = ask_gpt_nutrition_info(food_for_nutrition)
        if nutrition:
            st.session_state['carbs_value'] = nutrition.get('탄수화물', 0)
            st.session_state['protein_value'] = nutrition.get('단백질', 0)
            st.session_state['fat_value'] = nutrition.get('지방', 0)
            st.session_state['record_food'] = food_for_nutrition
            st.success("✅ 영양소 정보가 자동 입력되었습니다!")
        else:
            st.warning("⚠️ 영양소 정보를 가져오지 못했습니다.")

# === 식단 기록 폼 ===
with st.form("diet_form"):
    input_date = st.date_input("날짜", datetime.today()).strftime("%Y-%m-%d")
    meal_time = st.selectbox("시간", ["아침", "점심", "저녁", "간식"])
    food = st.text_input("먹은 음식 (기록용)", key="record_food")
    
    carbs = st.number_input("탄수화물 (g)", value=float(st.session_state.get('carbs_value', 0.0)), min_value=0.0, step=1.0)
    protein = st.number_input("단백질 (g)", value=float(st.session_state.get('protein_value', 0.0)), min_value=0.0, step=1.0)
    fat = st.number_input("지방 (g)", value=float(st.session_state.get('fat_value', 0.0)), min_value=0.0, step=1.0)
    
    submitted = st.form_submit_button("💾 기록 저장")
    if submitted:
        record = {"음식": food, "탄수화물": carbs, "단백질": protein, "지방": fat}
        user_data.setdefault(input_date, {}).setdefault(meal_time, []).append(record)
        diet_data[username] = user_data
        save_diet_data(diet_data)
        st.success("✅ 식단이 저장되었습니다!")


st.markdown("---")
# ================== 기록 조회 ==================
if user_data:
    st.markdown("#### 📋 식단 기록")
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

    records = []
    for date, meals in user_data.items():
        for time, items in meals.items():
            for item in items:
                records.append({
                    "날짜": date,
                    "식사시간": time,
                    "음식": item["음식"],
                    "탄수화물": item["탄수화물"],
                    "단백질": item["단백질"],
                    "지방": item["지방"]
                })

    df = pd.DataFrame(records)
    df["날짜"] = pd.to_datetime(df["날짜"])

    today = datetime.today().date()

    # === 년도 선택 ===
    years = sorted(df["날짜"].dt.year.unique())
    default_year_idx = years.index(today.year) if today.year in years else len(years)-1
    col_year, col_month, col_date = st.columns([1, 1.3, 2])

    with col_year:
        selected_year = st.selectbox(
            "년도", years,
            format_func=lambda y: f"{y}년",
            index=default_year_idx,
            key="diet_year"
        )

    # === 월 선택 ===
    month_df = df[df["날짜"].dt.year == selected_year]
    months = sorted(month_df["날짜"].dt.month.unique())
    default_month = today.month if today.month in months else months[-1]
    month_labels = {m: f"{m:02d}월" for m in months}
    with col_month:
        selected_month = st.selectbox(
            "월", months, format_func=lambda m: month_labels[m],
            index=months.index(default_month),
            key="diet_month"
        )

    # === 날짜 선택 ===
    date_df = month_df[month_df["날짜"].dt.month == selected_month]
    dates = sorted(date_df["날짜"].dt.date.unique())
    if today in dates:
        default_date_idx = dates.index(today)
    else:
        default_date_idx = len(dates)-1 if dates else 0
    date_labels = {d: f"{d.strftime('%d일')}" for d in dates}
    with col_date:
        if dates:
            selected_date = st.selectbox(
                "날짜", dates, format_func=lambda d: date_labels[d],
                index=default_date_idx, key="diet_date"
            )
        else:
            selected_date = None
            st.info("선택한 월에 식단 기록이 없습니다.")

    # === 선택 날짜의 식단 표시 및 삭제 ===
    if selected_date:
        daily_df = date_df[date_df["날짜"].dt.date == selected_date]
        if not daily_df.empty:
            st.markdown("", unsafe_allow_html=True)
            st.markdown(f"##### 📅{selected_date}")
            col_time, col_food, col_macro, col_delete = st.columns([1.5, 3, 3, 1])
            col_time.markdown("**식사시간**")
            col_food.markdown("**음식**")
            col_macro.markdown("**영양소 (탄/단/지)**")
            col_delete.markdown("**삭제**")
            for idx, row in daily_df.iterrows():
                col_time, col_food, col_macro, col_delete = st.columns([1.5, 3, 3, 1])
                col_time.write(row["식사시간"])
                col_food.write(row["음식"])
                col_macro.write(f"{row['탄수화물']}g / {row['단백질']}g / {row['지방']}g")
                if col_delete.button("삭제", key=f"delete_{row['날짜']}_{row['식사시간']}_{row['음식']}_{idx}"):
                    # 삭제 로직
                    date_str = row["날짜"].strftime("%Y-%m-%d")
                    meals = user_data[date_str][row["식사시간"]]
                    meals = [item for item in meals if not (
                        item["음식"] == row["음식"] and
                        item["탄수화물"] == row["탄수화물"] and
                        item["단백질"] == row["단백질"] and
                        item["지방"] == row["지방"]
                    )]
                    if meals:
                        user_data[date_str][row["식사시간"]] = meals
                    else:
                        del user_data[date_str][row["식사시간"]]
                    if not user_data[date_str]:
                        del user_data[date_str]
                    diet_data[username] = user_data
                    save_diet_data(diet_data)
                    st.success("삭제되었습니다.")
                    st.rerun()
        else:
            st.info("해당 날짜의 식단 기록이 없습니다.")
else:
    st.info("식단 기록이 없습니다.")

st.markdown("---")
# ================== 차트 및 권장량 경고 ==================
if user_data:
    st.markdown("#### 📊 날짜별 섭취량 차트")

    chart_data = []
    for date, meals in user_data.items():
        total_c, total_p, total_f = 0, 0, 0
        for items in meals.values():
            for item in items:
                total_c += item["탄수화물"]
                total_p += item["단백질"]
                total_f += item["지방"]
        chart_data.append({"날짜": date, "탄수화물": total_c, "단백질": total_p, "지방": total_f})

    if chart_data:
        df = pd.DataFrame(chart_data).sort_values("날짜")
        st.line_chart(df.set_index("날짜"))

        for idx, row in df.iterrows():
            warnings = []
            if row["탄수화물"] > RECOMMENDED_CARBS:
                warnings.append(f"🔴 `{idx}`의 탄수화물 섭취량 **{row['탄수화물']}g**이 권장량 **{RECOMMENDED_CARBS}g**을 초과했습니다.")
            if row["단백질"] > RECOMMENDED_PROTEIN:
                warnings.append(f"🟠 `{idx}`의 단백질 섭취량 **{row['단백질']}g**이 권장량 **{RECOMMENDED_PROTEIN}g**을 초과했습니다.")
            if row["지방"] > RECOMMENDED_FAT:
                warnings.append(f"🟡 `{idx}`의 지방 섭취량 **{row['지방']}g**이 권장량 **{RECOMMENDED_FAT}g**을 초과했습니다.")
            for w in warnings:
                st.warning(w)
