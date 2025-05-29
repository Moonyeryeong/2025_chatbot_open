import streamlit as st
import json
import os
import hashlib

st.set_page_config(page_title="당뇨병 통합관리", page_icon="🩺")

USERS_FILE = "data/users.json"

# ---------------- 사용자 정보 파일 로드 및 저장 ----------------
def load_users():
    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- 세션 상태 초기화 ----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "mode" not in st.session_state:
    st.session_state["mode"] = "home"  # 처음에는 home 페이지 보여주기

# ---------------- 사이드바 (항상 동일하게 표시) ----------------
with st.sidebar:
    if st.session_state["logged_in"]:
        st.markdown(f"""<p style='color: black; font-size: 18px;'>👤 {st.session_state['username']}님 환영합니다!</p>""",unsafe_allow_html=True)
        if st.button("로그아웃"):
            st.session_state.clear()
            st.session_state["mode"] = "home"
            st.rerun()
    else:
        st.markdown(
        """
        <h2 style= color: black; font-size: 18px;'>🔐 Sign Up </h2>""", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("로그인", use_container_width=True):
                st.session_state["mode"] = "login"
                st.rerun()

        with col2:
            if st.button("회원가입", use_container_width=True):
                st.session_state["mode"] = "signup"
                st.rerun()



# ---------------- 로그인 화면 ----------------
def show_login():
    st.title("🔐 로그인")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        users = load_users()
        if username in users and users[username] == hash_password(password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["mode"] = "home"  # 로그인 성공 시 다시 home으로
            st.success("✅ 로그인 성공!")
            st.rerun()
        else:
            st.error("❌ 아이디 또는 비밀번호가 잘못되었습니다. 회원가입을 안하셨다면 회원가입을 해주세요.")

    if st.button("← 홈으로"):
        st.session_state["mode"] = "home"
        st.rerun()

# ---------------- 회원가입 화면 ----------------
def show_signup():
    st.title("📝 회원가입")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    confirm = st.text_input("비밀번호 확인", type="password")

    if st.button("가입하기"):
        if not username or not password:
            st.warning("모든 항목을 입력하세요.")
            return
        if password != confirm:
            st.error("비밀번호가 일치하지 않습니다.")
            return

        users = load_users()
        if username in users:
            st.error("이미 존재하는 아이디입니다.")
        else:
            users[username] = hash_password(password)
            save_users(users)
            st.success("회원가입 완료! 로그인 해주세요.")
            st.session_state["mode"] = "login"
            st.rerun()

    if st.button("← 홈으로"):
        st.session_state["mode"] = "home"
        st.rerun()

# ---------------- 본문 표시 ----------------
if st.session_state["mode"] == "login":
    show_login()
    st.stop()
elif st.session_state["mode"] == "signup":
    show_signup()
    st.stop()

# ---------------- 기본 페이지 네비게이션 ----------------
home = st.Page("home.py", title="홈", icon=":material/home:", default=True)
chatbot = st.Page("chatbot.py", title="챗봇", icon=":material/chat:")

diet = st.Page("about/diet.py", title="식단", icon=":material/restaurant:")
prevention = st.Page("about/prevention.py", title="예방", icon=":material/masks:")
symptoms = st.Page("about/symptoms.py", title="증상", icon=":material/sick:")
treatment = st.Page("about/treatment.py", title="치료", icon=":material/medical_services:")
gi = st.Page("about/gi.py", title="GI지수", icon=":material/rice_bowl:")


personal_info = st.Page("reports/personal_info.py", title="개인정보", icon=":material/account_circle:")
glucose = st.Page("reports/glucose.py", title="혈당관리", icon=":material/glucose:")
medication = st.Page("reports/medication.py", title="복용약", icon=":material/pill:")
final_report = st.Page("reports/final_report.py", title="리포트", icon=":material/description:")
personal_diet = st.Page("reports/personal_diet.py", title="식단관리", icon=":material/egg_alt:")


pg = st.navigation(
    {
        "🏠 Home": [home],
        "🤖 Chatbot": [chatbot],
        "❓ About diabetes": [diet, prevention, symptoms, treatment, gi],
        "📋 Reports": [personal_info, glucose, personal_diet, medication, final_report],
    }
)

pg.run()
