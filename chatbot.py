import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="당뇨병 챗봇", page_icon="💬")

api_key = st.secrets["OPENAI_API_KEY"]

# 1. 유저 정보, 혈당, 복약 세션에서 모두 가져와 system 프롬프트로 생성
profile = st.session_state.get("diabetes_report", {})
med_list = st.session_state.get("med_list", [])
sugar_data = st.session_state.get("sugar_data", [])

# 복용약 요약(마지막 n개, 혹은 전체/최근만 선택)
if med_list:
    med_summary = "; ".join([f"{m['약 이름']}({m['복용 시간']})" for m in med_list[-3:]])
else:
    med_summary = "정보 없음"

# 혈당 요약(최신 값)
if sugar_data:
    latest_sugar = sugar_data[-1]["sugar"]
    sugar_info = f"{latest_sugar} mg/dL (최근 기록)"
else:
    sugar_info = "정보 없음"

# 개인정보 상세 (입력값 없으면 기본값 대체)
user_profile = f"""
당신은 당뇨병 환자 맞춤 건강 상담 챗봇입니다.
아래는 사용자 정보입니다:
- 이름: {profile.get('name', '미입력')}
- 나이: {profile.get('age', '미입력')}
- 성별: {profile.get('gender', '미입력')}
- 키: {profile.get('height', '미입력')}
- 몸무게: {profile.get('weight', '미입력')}
- 공복 혈당: {profile.get('fasting_glucose', '미입력')}
- 당화혈색소: {profile.get('hba1c', '미입력')}
- 혈압(수축기/이완기): {profile.get('bp_sys', '미입력')} / {profile.get('bp_dia', '미입력')}
- 당뇨약/인슐린 투여: {profile.get('on_medication', '미입력')}
- 진단받은 당뇨 유형: {profile.get('diabetes_type', '미입력')}
- 복용 중인 약: {med_summary}
- 최근 혈당 측정: {sugar_info}

이 정보를 항상 참고해서, 맞춤형 답변을 해주세요.
(특히 약 복용, 혈당 관리, 생활습관, 식단, 운동, 위험 신호 등에 대해 상황에 맞는 상담을 해주어야 합니다.)
"""

# 2. 메시지 세션 관리(이전 대화 내역 기억)
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "안녕하세요! 당뇨병 관리와 관련된 궁금한 점을 자유롭게 물어보세요 😊"}
    ]

# 3. 카카오톡 스타일 말풍선 함수
def kakao_message(content, is_user=False):
    if is_user:
        st.markdown(
            f"""
            <div style='display:flex;justify-content:flex-end;margin-bottom:4px;'>
                <div style="
                    background:#FEE500;
                    color:#222;
                    border-radius:18px 18px 4px 18px;
                    padding:12px 15px;
                    max-width:65%;
                    box-shadow:1px 2px 6px #ececec;">
                    {content}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            f"""
            <div style='display:flex;justify-content:flex-start;margin-bottom:4px;'>
                <div style="
                    background:#fff;
                    color:#222;
                    border-radius:18px 18px 18px 4px;
                    padding:12px 15px;
                    max-width:65%;
                    border:1.2px solid #F6F6F6;
                    box-shadow:1px 2px 6px #ececec;">
                    <span style="font-size:1.3em;vertical-align:-4px;margin-right:5px;">💬</span>{content}
                </div>
            </div>
            """, unsafe_allow_html=True)

# 4. UI: 제목, FAQ, 메시지 출력 등
st.markdown("""
<h1 style='display:flex; align-items:center; gap:9px; font-size:2.2em;'>
    <span>🤖</span>
    <span>당뇨병 챗봇</span>
</h1>
""", unsafe_allow_html=True)
st.markdown(
    """
    <div style="font-size:1.08em; margin-bottom:12px; color:#464646">
        <b>궁금한 점을 아래에 입력하거나 예시 버튼을 눌러 질문해보세요!</b>
    </div>
    """, unsafe_allow_html=True
)
faq_cols = st.columns(3)
faq_list = [
    "혈당이 높을 때 대처법은?", "당뇨에 좋은 식단 추천", "약 복용법이 궁금해요"
]
faq_inputs = [
    "혈당이 높을 때 어떻게 대처해야 하나요?",
    "당뇨병 환자에게 추천하는 식단이 있나요?",
    "메트포르민 복용법 알려주세요."
]
for i, label in enumerate(faq_list):
    if faq_cols[i].button(label):
        st.session_state["prompt"] = faq_inputs[i]
        st.rerun()

for msg in st.session_state["messages"]:
    kakao_message(msg["content"], is_user=(msg["role"] == "user"))

assistant_count = sum([m["role"] == "assistant" for m in st.session_state["messages"]])
if assistant_count > 1:
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown("#### 💬 더 궁금한 점 있으신가요?")
    st.markdown("<span style='color:#555;'>아래 예시를 눌러 추가로 질문해보세요!</span>", unsafe_allow_html=True)
    rec_cols = st.columns(3)
    rec_qs = [
        ("혈당이 낮을 때 대처법은?", "혈당이 낮을 때 어떻게 대처해야 하나요?"),
        ("당뇨 환자가 피해야 하는 음식은?", "당뇨 환자가 피해야 하는 음식이 있나요?"),
        ("운동은 뭘 하면 좋을까요?", "당뇨병 환자에게 좋은 운동을 추천해 주세요.")
    ]
    for i, (btn_label, btn_prompt) in enumerate(rec_qs):
        if rec_cols[i].button(btn_label, key=f"recq_{i}"):
            st.session_state["prompt"] = btn_prompt
            st.rerun()

user_prompt = st.chat_input("궁금한 점을 입력해 주세요 :)")
if "prompt" in st.session_state:
    user_prompt = st.session_state.pop("prompt")

if user_prompt:
    # always include user_profile(system) first, then messages so far
    messages = [{"role": "system", "content": user_profile}] + st.session_state["messages"]
    messages.append({"role": "user", "content": user_prompt})
    kakao_message(user_prompt, is_user=True)
    with st.spinner("챗봇이 답변을 작성 중입니다..."):
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        msg = response.choices[0].message.content.strip()
    st.session_state["messages"].append({"role": "user", "content": user_prompt})
    st.session_state["messages"].append({"role": "assistant", "content": msg})
    kakao_message(msg, is_user=False)
    st.rerun()
