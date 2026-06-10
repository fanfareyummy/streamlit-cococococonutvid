import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# --- 1. 임상 연구소 3D 레이아웃 설정 ---
st.set_page_config(
    page_title="3D GLOBAL PATHOGEN RADAR",
    page_icon="🌍",
    layout="wide",
)

# 사이버 메디컬 퓨처리즘 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Noto+Sans+KR:wght@300;500;700&display=swap');

    .stApp { 
        background-color: #020617; 
        color: #F8FAFC;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 3D 관제 센터 상단 바 */
    .globe-header {
        border-bottom: 1px solid #334155;
        padding: 15px 0;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .globe-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #22D3EE;
        text-shadow: 0 0 15px rgba(34, 211, 238, 0.5);
    }
    .globe-title span { color: #94A3B8; font-size: 0.8rem; font-weight: 400; margin-left: 10px; }

    /* 3D 지구본 프레임 */
    .globe-container {
        background: radial-gradient(circle at center, #0F172A 0%, #020617 100%);
        border: 1px solid #1E293B;
        border-radius: 24px;
        padding: 10px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.5);
    }

    /* 하단 가로형 고정 임상 분석 제어판 */
    .control-deck {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(15px);
        border: 1px solid #334155;
        border-top: 2px solid #22D3EE;
        border-radius: 16px;
        padding: 20px;
        margin-top: 20px;
    }

    /* 의학 정보 컴포넌트 */
    div[data-baseweb="input"] { background-color: #020617 !important; border: 1px solid #334155 !important; }
    
    .med-briefing {
        background: rgba(34, 211, 238, 0.05);
        border-left: 3px solid #22D3EE;
        padding: 15px;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #94A3B8;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 역학 데이터 로드 및 전처리 ---
@st.cache_data
def load_data():
    file_name = "covid_risk_analysis_result.csv"
    try:
        data = pd.read_csv(file_name)
        # Pydeck 시각화를 위한 컬러 매핑 (RGBA)
        # 0: Teal(안전), 1: Orange(주의), 2: Pink/Red(위험)
        def get_color(cluster):
            if cluster == 0: return [34, 211, 238, 160]  # Cyan
            if cluster == 1: return [245, 158, 11, 180]  # Amber
            return [236, 72, 153, 200]                   # Pink

        data['color'] = data['cluster'].apply(get_color)
        return data
    except: return None

df = load_data()

if df is None:
    st.error("🚀 SYSTEM ERROR: 'covid_risk_analysis_result.csv' 코어 링크가 손실되었습니다.")
    st.stop()

# --- 3. 3D 지구본 뷰 설정 ---
# 레이어 설정 (Scatterplot을 3D 포인트로 활용)
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position=["경도", "위도"],
    get_fill_color="color",
    get_radius=80000,  # 3D 지구본 위에서의 포인트 크기
    pickable=True,
    opacity=0.8,
    stroked=False,
    filled=True,
)

# 3D 지구본 뷰 상태 (GlobeView)
view_state = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=0.5,
    min_zoom=0,
    max_zoom=3,
    pitch=0,
    bearing=0
)

# --- 4. 메인 대시보드 상단 ---
st.markdown("""
    <div class='globe-header'>
        <div class='globe-title'>🌐 GLOBAL BIO-RADAR <span>v5.0 [3D MATRIX MODE]</span></div>
        <div style='color:#64748B; font-size:0.75rem; font-family:Orbitron;'>SAT-LINK: STABLE</div>
    </div>
""", unsafe_allow_html=True)

# --- 5. 중앙 2분할 레이아웃 ---
col_map, col_info = st.columns([2.2, 1.8])

with col_map:
    st.markdown("<p style='font-size:0.75rem; font-weight:700; color:#22D3EE; margin-bottom:10px;'>3D GLOBAL PATHOGEN DISTRIBUTION</p>", unsafe_allow_html=True)
    st.markdown("<div class='globe-container'>", unsafe_allow_html=True)
    
    # Pydeck을 이용한 3D 지구본 렌더링
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        views=[pdk.View(type="_GlobeView", controller=True)], # 이 부분이 3D 지구본 핵심
        map_style=None, # 배경 지도 없이 우주 공간처럼 연출
        tooltip={"text": "Infection Cluster: {cluster}\nCoords: {위도}, {경도}"}
    ))
    st.markdown("</div>", unsafe_allow_html=True)

with col_info:
    st.markdown("<p style='font-size:0.75rem; font-weight:700; color:#22D3EE; margin-bottom:10px;'>📹 MEDICAL PROOF: 손씻기 6단계 시뮬레이션</p>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=aE0MEPeaks4")
    
    st.markdown("""
        <div class='med-briefing'>
            <b style='color:#E2E8F0;'>🔬 질병관리청 검증 역학 리포트</b><br>
            • <b>3D 글로벌 패턴:</b> 현재 지구본에 표시된 노드들은 전 세계 확진자 밀집도를 실시간 클러스터링한 결과입니다.<br>
            • <b>영상 핵심 요약:</b> 비누를 사용하지 않은 '가짜 손씻기' 비율이 무려 60%에 달하며, 이는 3D 데이터 상의 고위험군(Pink) 확산의 주원인이 됩니다.<br>
            • <b>방어 기전:</b> 6단계 손씻기 완수 시 바이러스 사멸률은 비약적으로 상승하며, 특히 엄지손가락과 손톱 밑의 사각지대를 요격하는 것이 핵심입니다.
        </div>
    """, unsafe_allow_html=True)

# --- 6. 하단 가로형 제어 데크 (절대 깨지지 않음) ---
st.markdown("<div class='control-deck'>", unsafe_allow_html=True)
c_title, c_input, c_report = st.columns([1, 1.5, 1.5])

with c_title:
    st.markdown("""
        <div style='border-left: 3px solid #22D3EE; padding-left: 15px;'>
            <div style='font-family:Orbitron; font-size:0.8rem; color:#22D3EE;'>COORD SCANNER</div>
            <div style='font-size:0.9rem; font-weight:700; margin-top:5px;'>지정 좌표 요격</div>
            <div style='font-size:0.7rem; color:#64748B; margin-top:3px;'>분석할 지점의 위경도를 입력하세요.</div>
        </div>
    """, unsafe_allow_html=True)

with c_input:
    i_lat, i_lon = st.columns(2)
    with i_lat:
        lat = st.number_input("LAT", value=10.82, format="%.2f", label_visibility="collapsed")
    with i_lon:
        lon = st.number_input("LON", value=106.63, format="%.2f", label_visibility="collapsed")
    st.caption("🎯 지구본 상의 특정 위치를 정밀 스캔합니다.")

with c_report:
    near_df = df[(df['위도'] >= lat-5) & (df['위도'] <= lat+5) & 
                 (df['경도'] >= lon-5) & (df['경도'] <= lon+5)]
    
    if not near_df.empty:
        main_c = int(near_df['cluster'].value_counts().idxmax())
        colors_hex = {0: '#22D3EE', 1: '#F59E0B', 2: '#EC4899'}
        status_kr = {0: '안전(SECURE)', 1: '주의(WATCH)', 2: '위험(OUTBREAK)'}
        
        st.markdown(f"""
            <div style='background:{colors_hex[main_c]}22; color:{colors_hex[main_c]}; border:1px solid {colors_hex[main_c]}; padding:10px; border-radius:8px; text-align:center; font-weight:700;'>
                BIO-STATUS: {status_kr[main_c]}
            </div>
        """, unsafe_allow_html=True)
        
        if main_c == 2:
            st.error("🚨 경고: 고농도 바이러스 구역. 즉시 개인 위생 6단계를 강화하십시오.")
        else:
            st.info("✓ 안정: 해당 좌표 주변은 현재 표준 방역 범위 내에 있습니다.")
    else:
        st.markdown("<div style='background:#1E293B; color:#475569; padding:10px; border-radius:8px; text-align:center;'>데이터 공백 지역</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
