import streamlit as st

st.markdown("""
<h2>🤧 당뇨 주요 증상</h2>
<p style="color:#555; margin-bottom:16px;">
당뇨에서 주의해야 할 증상들을 확인해보세요.<br>
특정 증상이 지속되거나 갑자기 심해지면 <b>전문의 상담</b>을 권장합니다.
</p>
""", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
#카드
def symptoms_card(title, emoji, description, note="", height=210):
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
        </div>
    """



#카드 출력
rows = [
    ("잦은 소변", "🚽",
     "혈당이 높으면 신장이 과도한 포도당을 소변으로 배출하여 소변량과 횟수가 증가합니다.",
     "밤에 화장실을 자주 간다면 혈당 체크가 필요합니다. 특히 수면 질 저하로 이어질 수 있으므로 주의가 필요합니다."),

    ("심한 갈증", "💧",
     "소변으로 수분이 많이 빠져나가 탈수가 발생하면, 물을 자주 마시게 되고 갈증이 계속됩니다.",
     "물을 충분히 마셔도 해소되지 않으면 혈당 이상 신호일 수 있습니다. 이 증상이 반복된다면 병원 진료를 받아보세요."),

    ("만성 피로감", "😴",
     "세포가 포도당을 제대로 활용하지 못해 에너지가 부족, 평소보다 쉽게 피로해집니다.",
     "충분히 쉬어도 피곤하다면 혈당을 체크해보세요. 일상생활에 지장이 생길 만큼 피로가 누적된다면 당뇨 의심이 필요합니다."),

    ("원인 모를 체중 감소", "📉",
     "인슐린이 부족하거나 제대로 작동하지 않으면, 지방·근육을 에너지로 써서 살이 빠질 수 있습니다.",
     "식사를 제대로 하는데도 체중이 줄면 주의가 필요합니다. 기저질환이나 당뇨 외 다른 원인도 함께 고려해야 합니다."),

    ("흐린 시야/시력 저하", "👁️",
     "혈당 변화로 안구 내 수분 균형이 깨져 일시적 시력 저하, 시야 흐림이 생길 수 있습니다.",
     "합병증 위험이 있으니 정기검진이 중요합니다. 초기에는 증상이 미약할 수 있어 조기 발견이 핵심입니다."),

    ("상처 회복 지연", "🩹",
     "혈관·면역기능 저하로 작은 상처도 잘 낫지 않고, 감염이 반복되는 경우가 많아집니다.",
     "상처가 오래가거나 반복 감염 시, 혈당 관리가 필요합니다. 특히 발 부위 상처는 세심하게 살펴야 합니다."),

    ("손발 저림·감각 저하", "🦶",
     "만성 고혈당으로 신경이 손상될 경우, 손발이 저리거나 감각이 무뎌질 수 있습니다.",
     "당뇨병성 신경병증의 전조일 수 있습니다. 통증 없이 진행되는 경우도 있어 정기적인 체크가 중요합니다."),

    ("불안·우울 등 심리적 변화", "🧠",
     "혈당 조절이 어렵거나 만성 스트레스가 쌓이면 불안감, 우울, 짜증이 늘 수 있습니다.",
     "심리 건강도 당뇨 관리에서 매우 중요합니다. 필요 시 심리상담이나 전문가 도움을 받아보는 것이 좋습니다.")
]


for i in range(0, len(rows), 2):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(symptoms_card(*rows[i]), unsafe_allow_html=True)
    with col2:
        st.markdown(symptoms_card(*rows[i+1]), unsafe_allow_html=True)



#추가 안내 및 주의문 
st.markdown("""
<div style="
    background: #f6f7f9; 
    border-radius: 10px; 
    padding: 13px 22px; 
    margin-top:20px;
    margin-bottom:4px;
    color:#292929; 
    font-size:1.03em;
    border: 1.2px solid #ececec;">
    <b>❗ 아래와 같은 증상이 동반되면 즉시 의료진과 상담하세요.</b>
    <ul style="margin: 0.7em 0 0.5em 0.9em; padding:0; color:#555;">
        <li>극심한 갈증, 구토, 복통, 과호흡, 의식 저하</li>
        <li>소변에서 특이한 냄새가 남 (케톤산증 가능)</li>
        <li>고열, 감염, 갑작스러운 체중 감소, 실신</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="color:#767676; font-size:14px; margin-top:10px;">
<b>💡 혈당·체중·혈압 등은 주기적으로 체크하고, 가족력이 있거나 위 증상이 반복된다면 반드시 전문가 상담을 받으세요.</b>
</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
#사용자 Q&A
st.markdown("#### <span style='color:#232323;'>❓ 자주 묻는 Q&A</span>", unsafe_allow_html=True)
qna_list = [
    {
        "q": "증상이 없어도 당뇨일 수 있나요?",
        "a": "초기 당뇨는 <b>별다른 증상</b>이 없을 수 있습니다. 가족력이 있거나, 건강검진에서 혈당/당화혈색소가 높게 나왔다면 증상이 없어도 전문의 진료가 필요합니다."
    },
    {
        "q": "피로감, 식욕 저하가 있는데 꼭 당뇨 때문인가요?",
        "a": "피로, 식욕 변화는 <b>다양한 원인</b>이 있을 수 있습니다. 당뇨가 의심된다면 본인의 혈당 수치를 확인하고, 동반 증상이 있다면 기본 검진을 받으세요."
    },
    {
        "q": "당뇨로 인해 우울하거나 불안감이 심해집니다. 어떻게 해야 하나요?",
        "a": "심리적 어려움도 당뇨 관리의 한 부분입니다. 혼자 고민하지 말고 <b>가족·지인, 의료진, 상담센터</b>와 소통해보세요. 필요하면 심리 상담을 병행해도 좋습니다."
    },
    {
        "q": "당뇨 합병증은 어떻게 예방할 수 있나요?",
        "a": "혈당, 혈압, 콜레스테롤을 목표 범위 내로 관리하고, 금연·운동·균형 잡힌 식사 등 <b>건강 습관</b>을 실천하면 합병증 위험을 크게 낮출 수 있습니다."
    },
    {
        "q": "혈당의 정상 수치는 어느 정도인가요?",
        "a": "공복 혈당: **70~99 mg/dL**  \n- 식후 2시간 혈당: **140 mg/dL 미만**  \n- 당화혈색소: **5.7% 미만**"
    },
    {
        "q": "증상이 나아졌으면 약 복용을 멈춰도 되나요?",
        "a": "임의로 약 복용을 중단하면 혈당이 급격히 오를 수 있습니다. 증상이 좋아져도 반드시 <b>의료진</b>의 지시에 따라 약을 조절하세요."
    }
]

for item in qna_list:
    with st.expander(f"{item['q']}"):
        st.markdown(f"- <span style='color:#232323; font-size:1.02em;'>{item['a']}</span>", unsafe_allow_html=True)

