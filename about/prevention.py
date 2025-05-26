import streamlit as st

def prevention_card(title, emoji, description, badge=None, border=False):
    st.markdown(f"""
    <div style='
        background: #f6f7fa;
        border-radius: 13px;
        {"border:1.5px solid #ececec;" if border else "box-shadow: 0 2px 8px #f2f2f2;"}
        width: 100%;
        min-height: 120px;
        padding: 16px 21px 12px 21px;
        margin-bottom: 13px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    '>
        <div style="font-size:1.21rem; display:flex; align-items:center; margin-bottom:6px;">
            {emoji}
            <b style='font-size:1.06rem; margin-left:10px; color:#232323;'>{title}</b>
            {badge if badge else ""}
        </div>
        <div style='color:#222; font-size:0.99rem; flex:1; margin-top:3px;'>
            {description}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<h2 style="display:flex;align-items:center; color:#232323;">
    <span style="font-size:2.2rem;">🛡</span> 
    <span style="margin-left:0.5rem">당뇨 예방 가이드</span>
</h2>
<p style="color:#555; font-size:1.07rem; margin-bottom:10px;">
작은 습관부터 예방! 건강 습관을 함께 시작해요.
</p>
""", unsafe_allow_html=True)

st.markdown("#### 💪 예방 4대 생활수칙")

col1, col2 = st.columns(2, gap="small")
with col1:
    prevention_card(
        "1. 균형 잡힌 식사", "🥗",
        "설탕, 단순 탄수화물을 줄이고<br><b>GI 낮은 식품, 채소·단백질 섭취</b>가 핵심!",
        badge="<span style='background:#232323;color:white;font-size:0.85rem;padding:2.5px 8px;border-radius:7px;margin-left:10px;'>핵심</span>",
        border=True
    )
    prevention_card(
        "2. 건강한 체중 유지", "👟",
        "복부비만 주의! 체지방률 낮추고, 적정 체중 유지.",
        badge="<span style='background:#232323;color:white;font-size:0.83rem;padding:2.5px 8px;border-radius:7px;margin-left:10px;'>중요</span>",
        border=True
    )
with col2:
    prevention_card(
        "3. 주 3회 이상 운동", "🏃",
        "빠르게 걷기·수영 등 유산소, 근력운동 병행.<br>30분 이상, 땀이 나야 효과!",
        badge="<span style='background:#232323;color:white;font-size:0.85rem;padding:2.5px 8px;border-radius:7px;margin-left:10px;'>추천</span>",
        border=True
    )
    prevention_card(
        "4. 마음의 여유 갖기", "🧘",
        "스트레스는 혈당에도 영향! 명상, 산책 등으로 마음을 안정시키세요.",
        badge="<span style='background:#232323;color:white;font-size:0.85rem;padding:2.5px 8px;border-radius:7px;margin-left:10px;'>실천</span>",
        border=True
    )

st.markdown("""
<div style="background:#fcfcfc; border-radius:7px; padding:12px 19px; margin: 15px 0 3px 0; color:#a83232; border:1.2px solid #eee; font-size:1.02rem;">
※ 혈압·혈당·체중은 주기적으로 체크! 가족력 있으면 더 꼼꼼히 관리하세요.
</div>
<div style="color:#338000; font-size:1.01rem; margin-top:8px;">
🌱 습관을 오늘 시작하면 내일의 건강이 달라집니다!
</div>
""", unsafe_allow_html=True)