import streamlit as st

def prevention_card(title, emoji, description, min_height=150):
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

st.markdown("""
<h2 style="display:flex;align-items:center; color:#232323;">
    <span style="font-size:2.2rem;">🛡️</span> 
    <span style="margin-left:0.5rem">당뇨 예방 가이드</span>
</h2>
<p style="color:#555; argin-bottom:10px;">
당뇨를 예방할 수 있는 건강한 습관을 확인해보세요.
</p>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
# st.markdown("#### 🚶🏻‍♂️ 예방 생활습관")

col1, col2 = st.columns(2, gap="small")
with col1:
    prevention_card(
        "균형 잡힌 식사", "🥗",
        "탄수화물, 단백질, 지방, 비타민, 미네랄 등 다양한 영양소를 골고루 섭취하는 것이 중요합니다."
    )
    prevention_card(
        "규칙적인 운동", "👟",
        "주 3회 이상, 30분 이상 유산소 운동과 근력 운동을 병행하는 것이 좋습니다."
    )
with col2:
    prevention_card(
        "생활습관 개선", "🧘🏻",
        "흡연과 음주는 줄이는 것이 좋습니다. 충분한 수면과 스트레스 관리도 중요합니다."
    )
    prevention_card(
        "정기적인 검진", "🧑🏻‍⚕️",
        "정기적인 검진을 통해 건강 상태를 확인하고, 필요한 경우 전문의와 상담하여 건강 관리를 하는 것이 좋습니다."
    )

st.markdown("""
<div style="background: #f6f7fa; border-radius:7px; padding:12px 19px; margin: 15px 0 3px 0; color:salmon; border:1.2px solid #eee; font-size:1.02rem;">
❗ 혈압·혈당·체중은 주기적으로 체크해 주는 것이 좋아요. 가족력 있다면 더 꼼꼼히 관리하세요.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# 자주 묻는 질문

st.markdown("#### <span style='color:#232323;'>❓ 자주 묻는 Q&A</span>", unsafe_allow_html=True)

with st.expander("운동은 꼭 헬스장에서 해야 하나요?", expanded=False):
    st.markdown("""
    - 꼭 그렇지 않습니다! <b>걷기, 스트레칭, 계단 오르기</b> 등도 충분한 효과가 있습니다.
     """, unsafe_allow_html=True)

with st.expander("식단을 지키기 힘든 날은 어떻게 하나요?", expanded=False):
    st.markdown("""
    - 완벽함이 아니라 <b>꾸준함</b>이 중요합니다! 때때로 지키긴 힘든 날은 운동으로 보완해 보세요.
    """, unsafe_allow_html=True)

with st.expander("스트레스를 줄이는 것이 중요한가요?", expanded=False):
    st.markdown("""
    - 스트레스를 받으면 코르티솔, 아드레날린 같은 호르몬이 올라가서 간에서 포도당을 더 방출하여 <b>인슐린 저항성</b>이 높아집니다.
    - 스트레스는 고혈압, 심혈관실환 같은 합병증 위험까지 키울 수 있으니 관리하는 것이 좋습니다.
        """, unsafe_allow_html=True)

with st.expander("주기적 검진이 왜 중요한가요?", expanded=False):
    st.markdown("""
    - 합병증 대부분은 초기 증상이 없습니다. 
    - 조기에 발견하면 약물, 식습관, 운동으로 진행을 막을 수 있습니다.
    - 당뇨는 혈당 관리뿐 아니라, 눈·신장·심장 건강까지 <b>전체적인 정기 검진</b>을 하는 것이 좋습니다.
        """, unsafe_allow_html=True)
