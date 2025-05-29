import streamlit as st

def guide_card(title, emoji, description):
    st.markdown(f"""
        <div style="
            background: #f6f7fa;
            border: 1.5px solid #e5e6e9;
            border-radius: 13px;
            margin-bottom: 16px;
            padding: 19px 23px 14px 22px;
            box-shadow: 0 2px 7px rgba(80, 85, 100, 0.07);
            display: flex;
            align-items: flex-start;
            height: 200px;
        ">
            <div style='font-size:1.35em; margin-right:10px; margin-top:3px;'>{emoji}</div>
            <div>
                <b style="font-size:1.13em; color:#232323;">{title}</b>
                <div style="font-size:1.03em; color:#444; margin-top:6px;">{description}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def treatment_card(title, emoji, description, color):
    st.markdown(f"""
        <div style='background-color: {color}; padding: 15px 20px; border-radius: 12px; margin-bottom: 15px;'>
            <h4 style='margin-bottom:10px;'>{emoji} <strong>{title}</strong></h4>
            <p style='margin: 0;'>{description}</p>
        </div>
    """, unsafe_allow_html=True)

# 상단 제목 및 설명
st.markdown("""
<h2>🏥 당뇨 치료 가이드</h2>
<p style="color:#555; margin-bottom:18px;">
정기적인 관리와 치료는 당뇨 합병증 예방과 건강한 삶의 핵심입니다.<br>
대표 치료제와 혈당 관리 원칙을 확인해보세요.
</p>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
st.markdown("#### 🧪 당뇨 치료제")
st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

def symptoms_card(title, emoji, description, note="", height=150):
    return f"""
        <div style='
            background: #f6f7fa;
            border: 1.5px solid #e4e4ec;
            border-radius: 12px;
            padding: 16px 20px;
            height: {height}px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            margin-bottom: 20px;
        '>
            <div>
                <div style="font-size:1.05rem; font-weight:600; color:#333; display:flex; align-items:center; margin-bottom:6px;">
                    <span style="font-size:1.3rem; margin-right:8px;">{emoji}</span>{title}
                </div>
                <div style="font-size:0.95rem; color:#444; line-height:1.45;">{description}</div>
            </div>
            <div style="font-size:0.87rem; color:#4a4a4a; font-weight:500; margin-top:10px;">
                {note}  
        </div>
    """



#카드 출력
rows = [
    ("메트포르민", "💊", "1차 치료제로 많이 사용되며, 인슐린 저항성을 개선하고 간에서 포도당 생성을 억제하는 효과가 있습니다."),
    ("설포닐유레아", "💊", "췌장에서 인슐린 분비를 촉진하여 혈당을 낮춥니다."),
    ("DPP-4 억제제", "💊", "인슐린 분비를 촉진하고 글루카곤 분비를 억제하여 혈당을 조절하는 약물입니다."),
    ("SGLT-2 억제제", "💊", "신장에서 포도당 흡수를 억제하여 혈당을 낮추는 약물로, 최근에는 만성콩팥병과 심혈관 질환에 대한 보호 효과도 입증되고 있습니다."),
    ("GLP-1 수용체 작용제제", "💉", "인슐린 분비를 촉진하고 식욕을 억제하는 효과가 있어, 당뇨병 치료와 함께 비만 치료에도 활용 됩니다."),
    ("인슐린", "💉", "제1형 당뇨병 환자에게 필수적이며, 제2형 당뇨병 환자에서도 혈당 조절이 어려운 경우 사용됩니다."),
]


for i in range(0, len(rows), 2):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(symptoms_card(*rows[i]), unsafe_allow_html=True)
    with col2:
        st.markdown(symptoms_card(*rows[i+1]), unsafe_allow_html=True)


st.markdown("---")

# 혈당 모니터링
st.markdown("#### 📉 혈당 모니터링")
st.markdown(f"""
<div style="
    background: #f6f7fa;
    border: 1.5px solid #e5e6e9;
    border-radius: 13px;
    padding: 18px 24px;
    margin-bottom: 20px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
">
    <div style="display: flex; align-items: center; font-weight: bold; font-size: 1.1rem; margin-bottom: 6px; color:#232323;">
        <span style="font-size: 1.4rem; margin-right: 10px;">✅</span> 정기적으로 혈당을 기록해요!
    </div>
    <div style="color: #444; font-size: 0.96rem; flex: 1;">
        💡 자가 혈당 측정기로 <b>공복·식후 혈당</b>을 확인, <b>이상 수치가 계속된다면</b> 전문의 상담이 필요합니다.<br>
        <span style='color:#767676; font-size:0.98em;'>
        ✔ 공복 혈당: 70~99 mg/dL<br>
        ✔ 식후 2시간 혈당: 90~140 mg/dL<br>
        ✔ 당화혈색소(HbA1c): 4.0~5.6%<br>
        ✔ 혈압(수축/이완): 90~119 / 60~79 mmHg
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("---")
# 생활습관 개선
st.markdown("### 🏃 생활습관 개선")
st.markdown(f"""
<div style="
    background: #f6f7fa;
    border: 1.5px solid #e5e6e9;
    border-radius: 13px;
    padding: 18px 24px;
    margin-bottom: 20px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
">
    <div style="display: flex; align-items: center; font-weight: bold; font-size: 1.1rem; margin-bottom: 6px; color:#232323;">
        <span style="font-size: 1.4rem; margin-right: 10px;">🔄</span> 건강한 일상 습관을 만들어 봐요!
    </div>
    <div style="color: #444; font-size: 0.96rem; flex: 1;">
        <b>💡 운동, 체중 감량, 금연, 스트레스</b> 등의 관리는 중요합니다.<br>
        <span style='color:#767676; font-size:0.98em; margin-bottom: 3px;'>
        ✔ 운동: 하루에 30분 이상 유산소+근력 운동<br>
        ✔ 식사: 혈당지수(GI) 낮은 식품 위주 섭취, 규칙적 식사<br>
        ✔ 체중: 전체 체중의 5~10%만 감량해도 혈당 개선<br>
        ✔ 수면·스트레스 관리도 꼭 필요
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# 하단 안내 문구
st.markdown("""
<div style="color:#767676; font-size:0.97em; margin-top:14px;">
✔️ <b>복용 중인 약은 반드시 전문의와 상의하여 변경/조절해야 하며, 생활습관 개선도 함께 병행하세요.</b>
</div>
""", unsafe_allow_html=True)
