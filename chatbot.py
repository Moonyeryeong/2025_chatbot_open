import streamlit as st
import json
import os
import datetime
from openai import OpenAI

# ----------- 로그인 확인 -----------
if not st.session_state.get("logged_in", False):
    st.warning("🔒 로그인 해주세요.")
    st.stop()
username = st.session_state["username"]

# --- OpenAI Key (secrets.toml) ---
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
api_key = OPENAI_API_KEY

# --- 파일에서 사용자 리포트 정보 로드 ---
def load_user_report(username):
    path = "data/patient_data.json"
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(username, {})
    except Exception:
        return {}

# --- 파일에서 혈당 정보 로드 ---
def load_glucose(username):
    path = "data/glucose.json"
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(username, [])
    except Exception:
        return []

# --- 파일에서 복약 정보 로드 ---
def load_medications(username):
    path = "data/medication.json"
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(username, [])
    except Exception:
        return []

# --- 파일에서 식단 정보 로드 ---
def load_diet(username):
    path = "data/diet.json"
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(username, {})
    except Exception:
        return {}

# --- 사용자 정보, 혈당, 복약, 식단을 system prompt로 변환 ---
def get_user_profile_text():
    report = st.session_state.get("diabetes_report", None)
    if not report or (isinstance(report, dict) and not report):
        report = load_user_report(username)

    if isinstance(report, list) and report:
        report_item = report[-1]
    else:
        report_item = report if isinstance(report, dict) else {}

    # 복약 정보
    med_list = load_medications(username)
    if med_list:
        meds_str = "; ".join([f"{m['복용 날짜']} {m['복용 시간']} - {m['약 이름']}" for m in med_list[-5:]])
    else:
        meds_str = "입력 기록 없음"

    # 혈당 정보
    glucose_list = load_glucose(username)
    if glucose_list:
        last_5 = glucose_list[-5:]
        avg_glucose = sum([float(g.get("glucose", 0)) for g in glucose_list]) / len(glucose_list)
        last_glucose_str = "; ".join([f"{g['date']} {g['time']} - {g['glucose']}mg/dL" for g in last_5])
        glucose_summary = f"최근 5회 혈당: {last_glucose_str}. 최근 평균 혈당: {avg_glucose:.1f} mg/dL"
    else:
        glucose_summary = "입력 기록 없음"

    # 식단 정보
    diet_list = load_diet(username)
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    today_meals = diet_list.get(today_str, {})
    if today_meals:
        all_items = [item for meal in today_meals.values() for item in meal]
        foods = [item['음식'] for item in all_items]
        total_carbs = sum(item['탄수화물'] for item in all_items)
        total_protein = sum(item['단백질'] for item in all_items)
        total_fat = sum(item['지방'] for item in all_items)
        diet_summary = f"오늘 먹은 음식: {', '.join(foods)}. 총 섭취량 - 탄수화물: {total_carbs}g, 단백질: {total_protein}g, 지방: {total_fat}g."
    else:
        diet_summary = "오늘 식단 입력 기록 없음."

    return (
        f"이 사용자의 건강 리포트 정보는 다음과 같습니다.\n"
        f"이름: {report_item.get('name', '미입력')}, "
        f"나이: {report_item.get('age', '미입력')}, "
        f"성별: {report_item.get('gender', '미입력')}, "
        f"키: {report_item.get('height', '미입력')}cm, "
        f"몸무게: {report_item.get('weight', '미입력')}kg, "
        f"운동 시간: {report_item.get('daily_exercise', '미입력')}분, "
        f"수면 시간: {report_item.get('sleep_hours', '미입력')}시간, "
        f"흡연 여부: {report_item.get('smoking', '미입력')}, "
        f"음주 여부: {report_item.get('alcohol', '미입력')}, "
        f"당뇨 기간: {report_item.get('diagnosis_years', '미입력')}년, "
        f"당뇨 유형: {report_item.get('diabetes_type', '미입력')}, "
        f"합병증: {report_item.get('complications', '미입력')}, "
        f"당화혈색소: {report_item.get('hemoglobin', '미입력')}, "
        f"최근 증상: {report_item.get('recent_symptoms', '미입력')}, "
        f"목표 체중: {report_item.get('target_weight', '미입력')}kg, "
        f"목표 공복 혈당: {report_item.get('target_glucose', '미입력')}mg/dL, "
        f"목표 당화혈색소: {report_item.get('target_hba1c', '미입력')}%,\n"
        f"혈압: {report_item.get('bp_sys', '미입력')} / {report_item.get('bp_dia', '미입력')} mmHg, "
        f"BMI: {report_item.get('bmi', '미입력')},\n"
        f"최근 복용약: {meds_str}\n"
        f"최근 혈당 데이터: {glucose_summary}\n"
        f"최근 식단 데이터: {diet_summary}\n"
        "아래 사항을 꼭 지켜주세요.\n"
        "1. 사용자가 최근 혈당, 약 복용, 식단 데이터가 반영된 답변을 선호하므로, 관련 데이터가 있으면 반드시 구체적으로 답변에 활용해 주세요.\n"
        "2. 사용자가 직접적으로 혈당이나 약물, 건강, 음식, 식단을 묻지 않더라도 최근 데이터 참고해 건강상태, 변화, 위험요소, 관리조언을 꼭 넣어 답변하세요.\n"
        "3. 필요시 데이터에 근거한 맞춤형 칭찬, 조언, 식단 추천도 함께 해주세요.\n"
    )

# --- 챗봇 UI 및 system 프롬프트 ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": get_user_profile_text()},
        {"role": "assistant", "content": "안녕하세요! 당뇨병 및 건강관리에 대해 궁금한 점을 자유롭게 물어보세요 😊"}
    ]
else:
    st.session_state["messages"][0]["content"] = get_user_profile_text()

# --- 카카오톡 스타일 메시지 렌더러 ---
def kakao_message(content, is_user=False):
    if is_user:
        st.markdown(
            f"<div style='display:flex;justify-content:flex-end;margin:4px 0;'>"
            f"<div style='background:#FEE500;color:#222;border-radius:18px 18px 4px 18px;"
            f"padding:12px;max-width:65%;box-shadow:1px 2px 6px #ececec;'>{content}</div></div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='display:flex;justify-content:flex-start;margin:4px 0;'>"
            f"<div style='background:#fff;color:#222;border-radius:18px 18px 18px 4px;"
            f"padding:12px;max-width:65%;border:1px solid #F6F6F6;box-shadow:1px 2px 6px #ececec;'>"
            f"<span style='font-size:1.3em;margin-right:5px;'>💊</span>{content}</div></div>",
            unsafe_allow_html=True
        )

# --- 헤더 ---
st.markdown(
    "<h1 style='display:flex;align-items:center;gap:8px;'>"
    "<span>🤖</span><span>당뇨병 챗봇</span></h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<div style='margin-bottom:12px;color:#464646;'>"
    "<b>궁금한 점을 입력하고 Enter를 눌러 질문해 보세요!</b>"
    "</div>",
    unsafe_allow_html=True
)

# --- 기존 대화 렌더링 ---
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        kakao_message(msg["content"], is_user=(msg["role"] == "user"))

# --- 쿼리파라미터로 초기 메시지 채우기 ---
init_msgs = st.query_params.get("msg", None)
init_msg = init_msgs[0] if isinstance(init_msgs, list) and init_msgs else None

if init_msg:
    user_prompt = st.text_input(
        "궁금한 점을 입력하고 Enter를 눌러 보세요 😊",
        value=init_msg,
        key="prefill",
        label_visibility="collapsed"
    )
else:
    user_prompt = st.chat_input("궁금한 점을 입력해 주세요 :)")

# --- 사용자 입력 처리 & OpenAI 호출 ---
if user_prompt:
    st.session_state["messages"].append({"role": "user", "content": user_prompt})
    try:
        with st.spinner("챗봇이 답변을 작성 중입니다..."):
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state["messages"]
            )
            assistant_msg = resp.choices[0].message.content.strip()
    except Exception as e:
        assistant_msg = f"⚠️ 오류: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": assistant_msg})
    kakao_message(assistant_msg, is_user=False)

    # 한 번 질문 후에는 query params 초기화
    st.query_params.clear()
    st.rerun()