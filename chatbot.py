import streamlit as st
from openai import OpenAI
import pandas as pd
import requests
import glob, os, re

# st.set_page_config(page_title="당뇨병 챗봇", page_icon="💬")
if not st.session_state.get("logged_in", False):
    st.warning("🔒 로그인 해주세요.")
    st.stop()


# === 1. secrets.toml에서 API Key 값 불러오기 ===
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
API_KEY = st.secrets["API_KEY"]
base_url = st.secrets["base_url"]

# === 2. api_info_list 및 엔드포인트 정의 ===
api_info_list = [
    # 8개 직접 호출형
    {"name": "폐암환자 당뇨병 병력 여부", "endpoint": "https://apis.data.go.kr/B551172/Lung08", "params": {"serviceKey": API_KEY, "type": "json"}},
    {"name": "대장암 환자 당뇨병 병력 여부", "endpoint": "https://apis.data.go.kr/B551172/Colon08", "params": {"serviceKey": API_KEY, "type": "json"}},
    {"name": "신장암 환자 당뇨병 병력 여부", "endpoint": "https://apis.data.go.kr/B551172/Kidney08", "params": {"serviceKey": API_KEY, "type": "json"}},
    {"name": "췌장암 환자 당뇨병 병력 여부", "endpoint": "https://apis.data.go.kr/B551172/Pancreatic08", "params": {"serviceKey": API_KEY, "type": "json"}},
    {"name": "위암 환자 당뇨병 병력 여부", "endpoint": "https://apis.data.go.kr/B551172/Gastric08", "params": {"serviceKey": API_KEY, "type": "json"}},
    {"name": "간암 환자 당뇨병 병력 여부", "endpoint": "https://apis.data.go.kr/B551172/Liver08", "params": {"serviceKey": API_KEY, "type": "json"}},
    {"name": "담도암 환자 당뇨병 병력 여부", "endpoint": "https://apis.data.go.kr/B551172/Cholan08", "params": {"serviceKey": API_KEY, "type": "json"}},
    {"name": "전립선암 환자 당뇨병 병력 여부", "endpoint": "https://apis.data.go.kr/B551172/Prostate08", "params": {"serviceKey": API_KEY, "type": "json"}},
    # Swagger 5개 path 추가
    {"name": "국민건강보험공단_당뇨병의료이용률_20181231", "endpoint": base_url + "/15064610/v1/uddi:cc3d9af4-8345-4821-8d0d-c3bf57b412a8", "params": {"serviceKey": API_KEY, "page": 1, "perPage": 10, "returnType": "JSON"}},
    {"name": "국민건강보험공단_당뇨병의료이용률_20201231", "endpoint": base_url + "/15064610/v1/uddi:02fd0457-42eb-4fdb-b85e-9922c12db10e", "params": {"serviceKey": API_KEY, "page": 1, "perPage": 10, "returnType": "JSON"}},
    {"name": "국민건강보험공단_당뇨병의료이용률_20230807", "endpoint": base_url + "/15064610/v1/uddi:c0174de2-33d0-4db9-a14d-c17aed2f845e", "params": {"serviceKey": API_KEY, "page": 1, "perPage": 10, "returnType": "JSON"}},
    {"name": "국민건강보험공단_당뇨병의료이용률_20221231", "endpoint": base_url + "/15064610/v1/uddi:765bd3dd-f432-49b2-840b-e10e1e19477f", "params": {"serviceKey": API_KEY, "page": 1, "perPage": 10, "returnType": "JSON"}},
    {"name": "국민건강보험공단_당뇨병의료이용률_20231231", "endpoint": base_url + "/15064610/v1/uddi:b9c96b9f-40d1-4c79-9474-fd0bfb675a39", "params": {"serviceKey": API_KEY, "page": 1, "perPage": 10, "returnType": "JSON"}},
]

# === 3. 파일 데이터 통합 (csv/xlsx) ===
data_folder = "데이터"
data_files = glob.glob(os.path.join(data_folder, "*.csv")) + glob.glob(os.path.join(data_folder, "*.xlsx"))
df_list = []
for file in data_files:
    if file.endswith(".csv"):
        df = pd.read_csv(file)
    elif file.endswith(".xlsx"):
        df = pd.read_excel(file)
    else:
        continue
    df["__sourcefile__"] = os.path.basename(file)
    df_list.append(df)
all_data = pd.concat(df_list, ignore_index=True) if df_list else None

# === 4. 공공API 자동 매핑/검색 함수 ===
def api_autosearch(user_prompt):
    # (1) 암종명별 API 매핑
    disease_api_map = {
        "폐암": "폐암환자 당뇨병 병력 여부",
        "대장암": "대장암 환자 당뇨병 병력 여부",
        "신장암": "신장암 환자 당뇨병 병력 여부",
        "췌장암": "췌장암 환자 당뇨병 병력 여부",
        "위암": "위암 환자 당뇨병 병력 여부",
        "간암": "간암 환자 당뇨병 병력 여부",
        "담도암": "담도암 환자 당뇨병 병력 여부",
        "전립선암": "전립선암 환자 당뇨병 병력 여부"
    }
    for k, v in disease_api_map.items():
        if k in user_prompt:
            target = [api for api in api_info_list if api["name"] == v]
            if not target:
                return f"❌ 해당 암종({k})에 대한 API가 없습니다."
            try:
                resp = requests.get(target[0]["endpoint"], params=target[0]["params"], timeout=10)
                data = resp.json()
                return f"({k}) 데이터 예시: {str(data)[:400]}..."  # 일부만 표시
            except Exception as e:
                return f"API 오류({k}): {e}"

    # (2) 연도 및 시도 기반 의료이용률 (ex. "2023년 서울특별시")
    year_match = re.search(r"(\d{4})년", user_prompt)
    city_list = ["서울특별시", "부산광역시", "경기도", "대구광역시", "인천광역시", "광주광역시"]
    city_match = None
    for city in city_list:
        if city in user_prompt:
            city_match = city
            break
    if year_match and city_match:
        year = year_match.group(1)
        api_targets = [api for api in api_info_list if api["name"].endswith(year + "1231") or api["name"].endswith(year)]
        if not api_targets:
            return f"❌ {year}년도 해당 데이터 API가 없습니다."
        for api in api_targets:
            try:
                resp = requests.get(api["endpoint"], params=api["params"], timeout=10)
                data = resp.json()
                if "data" in data:
                    for row in data["data"]:
                        if city_match in row.get("시도", ""):
                            return f"{year}년 {city_match}의 당뇨병 의료이용률: {row.get('지표값(퍼센트)', 'N/A')}%"
                elif "response" in data and "body" in data["response"]:
                    return f"{year}년 {city_match} 데이터(참고): {data['response']['body']}"
            except Exception as e:
                return f"API 오류({city_match}): {e}"

    # (3) 기타(직접 검색이 불가할 때)
    return None

# === 5. 파일 데이터 검색 함수 ===
def file_data_search(user_prompt):
    if all_data is not None:
        for idx, row in all_data.iterrows():
            row_text = " ".join(map(str, row.values))
            if any(keyword in user_prompt for keyword in [str(row[col]) for col in all_data.columns]):
                return f"CSV/엑셀 데이터 예시: {row.to_dict()}"
    return None

# === 6. 챗봇 UI/메시지 ===
api_key = OPENAI_API_KEY

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "당뇨병 데이터/통계/약물/의료이용 등 모든 정보를 참고해 답변해 주세요."},
        {"role": "assistant", "content": "안녕하세요! 당뇨병 관리와 관련된 궁금한 점을 자유롭게 물어보세요 😊"}
    ]

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

    # 1순위: 공공API에서 답변
    api_msg = api_autosearch(user_prompt)
    if api_msg:
        msg = api_msg
    else:
        # 2순위: 파일 데이터에서 답변
        file_msg = file_data_search(user_prompt)
        if file_msg:
            msg = file_msg
        else:
            # 3순위: OpenAI로 답변
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
