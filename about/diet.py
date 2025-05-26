import streamlit as st

st.markdown("""
<h2 style="display:flex;align-items:center;">
    <span style="font-size:2.2rem;">🍱</span> 
    <span style="margin-left:0.5rem">당뇨 식단 가이드</span>
</h2>
<p style="color:#555;">건강한 혈당 관리를 위한 식단 요소와 실제 식사 팁을 확인해보세요.</p>
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

st.markdown("#### <span style='color:#232323;'>🌾 식단의 핵심 원칙</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="small")
with col1:
    diet_card(
        "탄수화물 섭취량 조절", "🍚",
        "백미, 밀가루 대신 잡곡, 고구마, 현미 등 복합 탄수화물로 교체.<br>"
        "<span style='color:#e65100;font-weight:bold;'>※ 과도한 섭취는 혈당 급상승 위험!</span>"
    )
    diet_card(
        "나트륨 섭취 줄이기", "🧂",
        "가공식품/짠 반찬 피하고 싱겁게.<br>싱겁게 먹는 습관이 고혈압 예방에도 좋아요."
    )
with col2:
    diet_card(
        "식이섬유 섭취 증가", "🥬",
        "채소, 해조류, 통곡물 중심으로 식사.<br>포만감+소화속도↓→혈당 안정!"
    )
    diet_card(
        "규칙적인 식사 시간", "⏰",
        "하루 3끼 일정 시간, 과식 NO!<br>소량씩 나눠먹는 것도 좋아요."
    )

# 실전 식단 예시
with st.expander("🍽️ 하루 식단 샘플", expanded=False):
    st.markdown("""
    <ul>
        <li><b>아침:</b> 현미잡곡밥 + 달걀찜 + 시금치나물</li>
        <li><b>점심:</b> 닭가슴살 샐러드 + 고구마 + 두부부침</li>
        <li><b>저녁:</b> 생선구이 + 나물반찬 + 브로콜리</li>
    </ul>
    <div style="background:#f8f8f9;padding:8px 15px;border-radius:8px;color:#805800;margin-top:6px;font-size:0.99rem;">
    <b>TIP</b>: 과일은 한 번에 1개 미만! <br>식사 중간엔 무가당 요거트, 견과류 소량 추천
    </div>
    """, unsafe_allow_html=True)

# 자주 묻는 질문(FAQ) 섹션
with st.expander("❓ 자주 묻는 Q&A", expanded=False):
    st.markdown("""
- <b>Q. 밥 대신 빵이나 면은 괜찮나요?</b><br>
  → 정제된 빵·면은 혈당을 더 올릴 수 있으니 <b>통밀빵/메밀국수</b> 등으로 제한하세요.<br><br>
- <b>Q. 과일은 마음껏 먹어도 되나요?</b><br>
  → <span style="color:#e65100;font-weight:bold;">과일도 당분!</span> 하루 1~2조각, 소량만 섭취!
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.info("✨ 모든 음식은 '적당히, 다양하게, 꾸준히!'가 기본 원칙입니다.", icon="💡")