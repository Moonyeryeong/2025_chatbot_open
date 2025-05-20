import streamlit as st

st.set_page_config(page_title="예방", page_icon="🛡")

st.markdown("<h2>🛡 당뇨 예방 가이드</h2>", unsafe_allow_html=True)
st.markdown("<p>지금 시작하는 건강 습관, 당뇨 예방의 첫걸음이에요.</p>", unsafe_allow_html=True)

def prevention_card(title, emoji, description, color):
    st.markdown(f"""
        <div style='background-color: {color}; padding: 15px 20px; border-radius: 12px; margin-bottom: 15px;'>
            <h4 style='margin-bottom:10px;'>{emoji} <strong>{title}</strong></h4>
            <p style='margin: 0;'>{description}</p>
        </div>
    """, unsafe_allow_html=True)

with st.expander("🥗 건강한 식단"):
    prevention_card(
        "균형 잡힌 식사",
        "🥗",
        "설탕과 단순 탄수화물을 줄이고, 채소와 단백질 중심의 식단을 유지해요. GI 수치가 낮은 식품을 선택하는 것이 좋아요.",
        "#e8f5e9"
    )

with st.expander("🏃 규칙적인 운동"):
    prevention_card(
        "주 3회 이상 활동",
        "🏃",
        "빠르게 걷기, 자전거, 수영 등의 유산소 운동을 주 3~5회 30분 이상 실천하면 인슐린 민감성이 향상돼요.",
        "#e3f2fd"
    )

with st.expander("⚖️ 체중 관리"):
    prevention_card(
        "건강한 체중 유지",
        "⚖️",
        "복부 비만은 당뇨 위험 요인이에요. 체지방률을 낮추고 적정 체중을 유지하면 예방 효과가 높아져요.",
        "#fce4ec"
    )

with st.expander("🧘 스트레스 줄이기"):
    prevention_card(
        "마음의 여유 갖기",
        "🧘",
        "스트레스는 호르몬 불균형을 유발하고 혈당을 올릴 수 있어요. 명상이나 휴식으로 마음을 다스리는 것도 중요해요.",
        "#f3e5f5"
    )
