import streamlit as st

st.set_page_config(page_title="식단", page_icon="🍱")

st.markdown("<h2>🍱 당뇨 식단 가이드</h2>", unsafe_allow_html=True)
st.markdown("<p>건강한 혈당 관리를 위한 식단 요소들을 확인해보세요.</p>", unsafe_allow_html=True)

# 공통 카드 스타일 함수
def diet_card(title, emoji, description, color):
    st.markdown(f"""
        <div style='background-color: {color}; padding: 15px 20px; border-radius: 12px; margin-bottom: 15px;'>
            <h4 style='margin-bottom:10px;'>{emoji} <strong>{title}</strong></h4>
            <p style='margin: 0;'>{description}</p>
        </div>
    """, unsafe_allow_html=True)

# 상세 식단 항목
with st.expander("🍚 탄수화물 조절"):
    diet_card(
        "탄수화물 섭취량 조절",
        "🍚",
        "백미, 밀가루보다는 잡곡이나 고구마, 현미 등 복합 탄수화물을 선택해 혈당 상승을 완만하게 유지하세요.",
        "#fff3e0"
    )

with st.expander("🥬 섬유소 섭취"):
    diet_card(
        "식이섬유 섭취 증가",
        "🥬",
        "채소, 해조류, 통곡물 등은 소화 속도를 늦추고 포만감을 주어 혈당 조절에 도움을 줍니다.",
        "#e0f2f1"
    )

with st.expander("🧂 저염식 권장"):
    diet_card(
        "나트륨 섭취 줄이기",
        "🧂",
        "가공식품이나 짠 반찬은 피하고, 싱겁게 먹는 습관을 길러야 고혈압 합병증도 예방할 수 있어요.",
        "#f3e5f5"
    )

with st.expander("⏰ 정해진 시간에 식사"):
    diet_card(
        "규칙적인 식사 시간",
        "⏰",
        "하루 3끼를 일정한 시간에 먹으며, 과식을 피하고 소량씩 나눠 먹는 것도 좋아요.",
        "#e8f5e9"
    )
