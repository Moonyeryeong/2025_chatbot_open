import streamlit as st
import pandas as pd
import glob, os, json, re
from openai import OpenAI

# ----------- 로그인 확인 -----------
if not st.session_state.get("logged_in", False):
    st.warning("🔒 로그인 해주세요.")
    st.stop()
username = st.session_state["username"]

# --- OpenAI Key (secrets.toml) ---
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# --- 데이터 폴더 내 모든 csv/xlsx 자동 통합 (공공데이터용) ---
data_folder = "데이터"
data_files = glob.glob(os.path.join(data_folder, "*.csv")) + glob.glob(os.path.join(data_folder, "*.xlsx"))
df_list = []
for file in data_files:
    if file.endswith(".csv"):
        df = pd.read_csv(file, dtype=str)
    elif file.endswith(".xlsx"):
        df = pd.read_excel(file, dtype=str)
    else:
        continue
    df["__sourcefile__"] = os.path.basename(file)
    df_list.append(df)
all_data = pd.concat(df_list, ignore_index=True) if df_list else None

# --- 리포트(개인정보) 파일에서 사용자별 정보 불러오기 ---
def load_user_report(username):
    path = "data/patient_data.json"
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(username, {})
    except Exception as e:
        return {}

# --- 사용자 정보(리포트) → system 프롬프트용 텍스트로 변환 ---
def get_user_profile_text():
    # 1. 세션에 최신 리포트가 있으면 우선 사용, 없으면 파일에서 불러오기
    report = st.session_state.get("diabetes_report", None)
    if not report or (isinstance(report, dict) and not report):  # 세션에 없으면 파일에서 불러옴
        report = load_user_report(username)
    # 만약 리스트라면(히스토리 저장) 최신(마지막)만 사용
    if isinstance(report, list):
        report_item = report[-1] if report else {}
    else:
        report_item = report

    # 최신 복용약 리스트: 리포트에서 사용하는 함수와 동일하게 불러오기!
    from utils import load_medications  # utils.py에 있다고 가정
    med_list = load_medications(username)  # username에 맞는 약 데이터 가져오기

    # 약 목록 텍스트 포맷 (예: 날짜, 시간, 약 이름)
    if med_list:
        meds_str = "; ".join([
            f"{med['복용 날짜']} {med['복용 시간']} - {med['약 이름']}"
            for med in med_list
        ])
    else:
        meds_str = "미입력"

    # system 프롬프트용 텍스트
    return (
        f"이 사용자의 건강 리포트 정보는 다음과 같습니다.\n"
        f"이름: {report_item.get('name', '미입력')}, "
        f"나이: {report_item.get('age', '미입력')}, "
        f"성별: {report_item.get('gender', '미입력')}, "
        f"키: {report_item.get('height', '미입력')}cm, "
        f"몸무게: {report_item.get('weight', '미입력')}kg, "
        f"공복 혈당: {report_item.get('fasting_glucose', '미입력')}mg/dL, "
        f"당화혈색소: {report_item.get('hba1c', '미입력')}, "
        f"혈압: {report_item.get('bp_sys', '미입력')} / {report_item.get('bp_dia', '미입력')} mmHg, "
        f"BMI: {report_item.get('bmi', '미입력')}, "
        f"복용약: {meds_str}\n"
        "답변 시 이 정보를 최대한 활용해 맞춤 설명을 해주세요."
    )

# --- 파일 데이터 자동검색 (CSV/XLSX) ---
def file_data_search(user_prompt, max_results=3):
    if all_data is None:
        return None
    years = re.findall(r"\d{4}", user_prompt)
    locations = ["서울", "특별시", "부산", "광역시", "경기도", "인천", "대구", "광주", "대전", "울산", "세종"]
    location_found = [loc for loc in locations if loc in user_prompt]
    disease_words = ["당뇨", "의료이용률", "유병률", "환자수", "분율", "비율"]
    disease_found = [d for d in disease_words if d in user_prompt]
    keywords = years + location_found + disease_found + user_prompt.split()

    def row_score(row):
        row_text = " ".join([str(x) for x in row.values])
        score = sum([k in row_text for k in keywords])
        return score

    scored_rows = [(row_score(row), row) for idx, row in all_data.iterrows()]
    filtered = [r for s, r in sorted(scored_rows, key=lambda x: -x[0]) if s > 0][:max_results]
    if filtered:
        outs = []
        for r in filtered:
            src = r["__sourcefile__"]
            show = pd.DataFrame(r).T.drop(columns=["__sourcefile__"], errors="ignore")
            outs.append(f"<b>파일:</b> {src}\n\n" + show.to_html(index=False, escape=False))
        return "<br><br>".join(outs)
    return None

# --- 챗봇 UI 및 system 프롬프트 ---
api_key = OPENAI_API_KEY

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "아래 사용자 리포트 및 데이터 파일 기반으로 답변하세요.\n" + get_user_profile_text()},
        {"role": "assistant", "content": "안녕하세요! 당뇨병 및 건강관리에 대해 궁금한 점을 자유롭게 물어보세요 😊"}
    ]
else:
    # system 메시지 최신화 (리포트가 바뀌면 항상 최신 정보 사용)
    st.session_state["messages"][0]["content"] = "아래 사용자 리포트 및 데이터 파일 기반으로 답변하세요.\n" + get_user_profile_text()

def kakao_message(content, is_user=False):
    if is_user:
        st.markdown(
            f"<div style='display:flex;justify-content:flex-end;margin-bottom:4px;'><div style='background:#FEE500;color:#222;border-radius:18px 18px 4px 18px;padding:12px 15px;max-width:65%;box-shadow:1px 2px 6px #ececec;'>{content}</div></div>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='display:flex;justify-content:flex-start;margin-bottom:4px;'><div style='background:#fff;color:#222;border-radius:18px 18px 18px 4px;padding:12px 15px;max-width:65%;border:1.2px solid #F6F6F6;box-shadow:1px 2px 6px #ececec;'><span style='font-size:1.3em;vertical-align:-4px;margin-right:5px;'>💊</span>{content}</div></div>",
            unsafe_allow_html=True)

st.markdown("<h1 style='display:flex; align-items:center; gap:9px; font-size:2.2em;'><span>🤖</span><span>당뇨병 챗봇</span></h1>", unsafe_allow_html=True)
st.markdown(
    "<div style='font-size:1.08em; margin-bottom:12px; color:#464646'><b>궁금한 점을 입력하고 Enter를 눌러 질문해 보세요!</b></div>",
    unsafe_allow_html=True
)

for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        kakao_message(msg["content"], is_user=(msg["role"] == "user"))

user_prompt = st.chat_input("궁금한 점을 입력해 주세요 :)")
if user_prompt:
    st.session_state["messages"].append({"role": "user", "content": user_prompt})

    # 1순위: 파일 데이터 검색
    file_msg = file_data_search(user_prompt)
    if file_msg:
        msg = file_msg
    else:
        # 2순위: OpenAI로 답변 (리포트 자동 반영)
        try:
            with st.spinner("챗봇이 답변을 작성 중입니다..."):
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state["messages"]
                )
                msg = response.choices[0].message.content.strip()
        except Exception as e:
            msg = f"⚠️ 오류: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": msg})
    kakao_message(msg, is_user=False)
    st.rerun()