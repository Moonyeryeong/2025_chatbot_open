import streamlit as st

home = st.Page("home.py", title="홈", icon=":material/home:", default=True)

chatbot = st.Page("chatbot.py", title="챗봇", icon=":material/chat:")

#about
diet = st.Page("about/diet.py", title="식습관", icon=":material/restaurant:")
prevention = st.Page("about/prevention.py", title="예방", icon=":material/masks:")
symptoms = st.Page("about/symptoms.py", title="증상", icon=":material/sick:")
treatment = st.Page("about/treatment.py", title="치료", icon=":material/medical_services:")

#report
personal_info = st.Page("reports/personal_info.py", title="개인정보", icon=":material/account_circle:")
glucose = st.Page("reports/glucose.py", title="혈당관리", icon=":material/glucose:")
medication = st.Page("reports/medication.py", title="복용약", icon=":material/pill:")
final_report = st.Page("reports/final_report.py", title="리포트", icon=":material/description:")


pg = st.navigation(
    {
        "🏠 Home": [home],
        "🤖 Chatbot": [chatbot],
        "❓ About diabetes": [diet, prevention, symptoms, treatment],
        "📋 Reports": [personal_info, glucose, medication, final_report],
    }
)

pg.run()