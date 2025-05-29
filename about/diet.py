import streamlit as st

st.markdown("""
<h2 style="display:flex;align-items:center;">
    <span style="font-size:2.2rem;">🍱</span> 
    <span style="margin-left:0.5rem">당뇨 식단 가이드</span>
</h2>
<p style="color:#555;">건강한 혈당 관리를 위한 식단의 핵심 원칙을 확인해보세요.</p>
""", unsafe_allow_html=True)

def diet_card(title, emoji, description, min_height=150):
    st.markdown(f"""
        <div style='
            background: #f6f7fa;
            border:1.5px solid #ececec;
            border-radius: 13px;
            padding: 16px 21px 13px 21px;
            margin-bottom: 13px;
            min-height: {min_height}px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        '>
            <div style="font-size:1.21rem; display:flex; align-items:center; margin-bottom:6px;">
                {emoji}
                <b style='font-size:1.06rem; margin-left:10px; color:#232323;'>{title}</b>
            </div>
            <div style='color:#222; font-size:0.99rem; flex:1; margin-top:3px;'>{description}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
# st.markdown("#### <span style='color:#232323;'>🌾 식단의 핵심 원칙</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="small")
with col1:
    diet_card(
        "나트륨 섭취 줄이기", "🧂",
        "과다한 나트륨의 섭취는 혈압을 상승시킬 수 있으므로 저염식으로 먹는 습관을 갖는 것이 좋습니다.<br>"
    )
    diet_card(
        "당류 섭취 주의하기", "🍯",
        "당류는 농축된 에너지원으로 소화 흡수가 빨라 급격한 혈당 상승을 유발할 수 있습니다."
    )
with col2:
    diet_card(
        "식이섬유 충분히 섭취하기", "🥬",
        "식이섬유는 완만한 혈당의 상승과 혈중지방의 농도를 조절하므로 혈당 조절 및 심 뇌혈관계 질환의 예방에 도움이 됩니다."
    )
    diet_card(
        "규칙적인 시간에 식사하기", "⏰",
        "적절한 에너지섭취와 규칙적인 식사는 혈당 조절에 도움이 됩니다."
    )

st.markdown("---")
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# 자주 묻는 질문(FAQ) 섹션
st.markdown("#### <span style='color:#232323;'>❓ 자주 묻는 Q&A</span>", unsafe_allow_html=True)

with st.expander("밥 대신 빵이나 면은 괜찮나요?", expanded=False):
    st.markdown("""
- 정제된 빵·면(흰빵, 흰국수 등)은 혈당을 더 올릴 수 있어요.<br>
- <b>통곡물빵, 메밀국수, 곤약면</b> 등을 제한적으로 드세요.
    """, unsafe_allow_html=True)

with st.expander("과일은 마음껏 먹어도 되나요?", expanded=False):
    st.markdown("""
- <span style="font-weight:bold;">과일도 당분!</span> 과일은 천연당이 들어 있어서 과다 섭취 시 혈당을 급격히 올릴 수 있습니다.<br>
- <b>딸기, 사과, 키위, 블루베리</b> 등 혈당 지수가 낮은 과일을 추천해요.
    """, unsafe_allow_html=True)

with st.expander("저염식이 무엇인가요?", expanded=False):
    st.markdown("""
    - 저염식은 <b>나트륨</b> 섭취를 줄인 식단을 말합니다.
    - 하루 소금 5g 이하, 나트륨 2000mg 이하로 제한하는 것이 좋습니다.
    - 가공식품과 즉석식품은 줄이고 싱겁게 드시는게 좋습니다. 국물, 찌개, 라면 등은 자주 먹지 않는 것이 좋아요.
    """, unsafe_allow_html=True)

with st.expander("외식이나 배달음식을 자주 먹어도 되나요?", expanded=False):
    st.markdown("""
- 먹어도 되지만 <b>선택</b>과 <b>조절</b>이 중요합니다!<br>
- 단백질, 채소 위주의 메뉴를 고르시는게 좋습니다.<br>
- <b>양념, 소스, 튀김</b> 등은 양을 줄이고, 싱겁게 드시는 것도 도움이 됩니다.
    """, unsafe_allow_html=True)

with st.expander("식사 중에 주의해야 할 점이 있나요?", expanded=False):
    st.markdown("""
- <b>천천히 꼭꼭 씹어</b> 먹는 습관은 혈당 급상승 예방에 좋습니다.<br>
- 식사 전후로 가벼운 산책도 혈당 관리에 도움이 돼요.<br>
- 음료수나 주스는 피하고 물이나 차 위주로 드시는 것이 좋습니다.
    """, unsafe_allow_html=True)
