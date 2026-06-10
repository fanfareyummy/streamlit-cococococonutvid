import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- 1. 임상/의료 연구실 컨셉 테마 설정 ---
st.set_page_config(
    page_title="EPIDEMIC BIO-MONITORING SYSTEM",
    page_icon="🩺",
    layout="wide",
)

# 대학병원/질병관리청 대시보드 스타일의 딥 다크 메디컬 Teal & Slate UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Noto+Sans+KR:wght@300;500;700&display=swap');

    .stApp { 
        background-color: #0B111E; 
        color: #E2E8F0;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 상단 메디컬 센터 타이틀 바 */
    .medical-header {
        border-bottom: 3px solid #0D9488;
        padding-bottom: 12px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .medical-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: #0EA5E9;
        letter-spacing: -1px;
    }
    .medical-title span {
        color: #0D9488;
    }
    .live-indicator {
        background-color: rgba(13, 148, 136, 0.1);
        border: 1px solid #0D9488;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        color: #2DD4BF;
        font-family: 'JetBrains Mono', monospace;
    }

    /* 메인 임상 맵 프레임 */
    .map-container {
        background: #141B2D;
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 12px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }

    /* 하단 가로형 고정 임상 분석 제어판 (절대 깨지지 않는 구조) */
    .clinical-panel {
        background: #141B2D;
        border-top: 4px solid #38BDF8;
        border-radius: 12px;
        padding: 22px;
        margin-top: 25px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }

    /* 의학 정보 컴포넌트 */
    div[data-baseweb="input"] { background-color: #0B111E !important; border: 1px solid #334155 !important; color: #fff !important; }
    .clinical-badge {
        padding: 10px;
        border-radius: 8px;
        font-weight: 700;
        text-align: center;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }
    
    .med-instruction {
        background: rgba(14, 165, 233, 0.05);
        border-left: 4px solid #0EA5E9;
        padding: 12px;
        border-radius: 0 8px 8px 0;
        font-size: 0.85rem;
        line-height: 1.5;
        color: #94A3B8;
    }
    </style>
""", unsafe_allow_html=True)


# --- 2. 역학 조사 데이터 로드 ---
@st.cache_data
def load_epidemic_data():
    file_name = "covid_risk_analysis_result.csv"
    try:
        try: return pd.read_csv(file_name, encoding="utf-8")
        except: return pd.read_csv(file_name, encoding="cp949")
    except: return None

df = load_epidemic_data()

if df is None:
    st.error("🔬 임상 분석 에러: 원격지 'covid_risk_analysis_result.csv' 코어 데이터를 로드하지 못했습니다.")
    st.stop()


# --- 3. 임상 위험도 및 메디컬 컬러 매핑 ---
# 0: 안전(Teal), 1: 주의(Orange), 2: 고위험(Crimson)
med_colors = {0: '#0D9488', 1: '#EA580C', 2: '#DC2626'}
med_status = {
    0: '🟢 LEVEL I: NORMAL AREA (안정 수준)', 
    1: '🟠 LEVEL II: WATCH AREA (추적·경계 관찰 필요)', 
    2: '🔴 LEVEL III: BIO-HAZARD AREA (감염 고위험 요격 구역)'
}


# --- 4. 메인 대시보드 상단 바 ---
st.markdown("""
    <div class='medical-header'>
        <div class='medical-title'>🩺 CDC-BIOMETRIC INDEXING SYSTEM <span>[EPIDEMIC-4.0]</span></div>
        <div class='live-indicator'>● HOSP-NET LINKED (EMERGENCY_MODE)</div>
    </div>
""", unsafe_allow_html=True)


# --- 5. 2분할 메인 레이아웃 (좌측: 글로벌 역학 지도 / 우측: 의학 참고 비디오 및 가이드) ---
col_left_map, col_right_media = st.columns([2.2, 1.8])

with col_left_map:
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#0EA5E9; margin-bottom:5px;'>🌐 GLOBAL GEOGRAPHIC PATHOGEN TRACKING MAP</p>", unsafe_allow_html=True)
    st.markdown("<div class='map-container'>", unsafe_allow_html=True)
    
    # 임상 느낌을 주는 깔끔한 CartoDB Dark Matter 맵 적용
    m = folium.Map(location=[25, 15], zoom_start=1.8, tiles="CartoDB dark_matter")
    
    for i in range(len(df)):
        cluster = int(df.iloc[i]['cluster'])
        folium.CircleMarker(
            location=[df.iloc[i]['위도'], df.iloc[i]['경도']],
            radius=4,
            color=med_colors[cluster],
            fill=True,
            fill_color=med_colors[cluster],
            fill_opacity=0.4,
            weight=1,
            popup=f"BIO-STATUS LEVEL: {cluster}"
        ).add_to(m)
        
    st_folium(m, width=780, height=450, key="epidemic_clinical_map")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right_media:
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#0D9488; margin-bottom:5px;'>📹 CLINICAL REFERENCE VIDEO: 감염 예방의 기적</p>", unsafe_allow_html=True)
    
    # 요청하신 KBS 뉴스 올바른 손씻기 방법 영상 임베드 및 동기화
    st.video("https://www.youtube.com/watch?v=_fhiA1-Qd34")
    
    # 영상 내용 기반의 초정밀 의학 아카이브 노트 
    st.markdown("""
        <div class='med-instruction'>
            <b style='color:#FFF; font-size:0.9rem;'>🔬 임상 의학 가이드: 30초의 기적 (KBS 분석 제공)</b><br>
            • <b>감염병 70% 차단:</b> 수시로 비누 거품을 내어 <b>30초 이상</b> 손을 세척할 시 콜레라, 대장균, 식중독, 황색포도상구균 등의 주요 병원균을 차단할 수 있습니다.<br>
            • <b>맹점 구역(Blind Spot):</b> 일반 세척 시 <b>손톱 주변, 손끝, 손바닥 가장자리</b>에 형광물질(세균 모사)이 그대로 잔류함이 검증되었습니다.<br>
            • <b>올바른 6단계 수칙:</b> 1) 손바닥 비비기 2) 손가락 교차 3) 엄지손가락 회전 문지르기 4) 손끝을 손바닥에 문질러 손톱 밑까지 완벽하게 소독하십시오.<br>
            • <b>얼굴 접촉 차단:</b> 인간은 시간당 평균 36회 이상 손으로 얼굴(눈, 코, 입)을 무의식적으로 접촉하므로 점막 감염의 핵심 통로가 됩니다.
        </div>
    """, unsafe_allow_html=True)


# --- 6. 하단 3분할 가로형 의학 콘솔 패널 (절대 깨지지 않는 구조) ---
st.markdown("<div class='clinical-panel'>", unsafe_allow_html=True)
col_sim_title, col_coords, col_prediction = st.columns([1.1, 1.4, 1.5])

# [6-1] 임상 모니터 센터 상태창
with col_sim_title:
    st.markdown("""
        <div style='border-left: 3px solid #38BDF8; padding-left: 12px;'>
            <span style='color: #64748B; font-size: 0.75rem; font-weight: bold; font-family: "JetBrains Mono";'>SECTION A: RADAR MATRIX</span>
            <div style='font-size: 0.9rem; font-weight: bold; margin-top: 5px; color: #E2E8F0;'>역학 검사 좌표 지정</div>
            <div style='font-size: 0.75rem; color: #475569; margin-top: 3px;'>위경도 기준 반경 500km 내 생체 매트릭스를 추적합니다.</div>
        </div>
    """, unsafe_allow_html=True)

# [6-2] 위도 및 경도 좌표 스캐너 인풋
with col_coords:
    st.markdown("<span style='color: #38BDF8; font-size: 0.75rem; font-weight: bold; font-family: \"JetBrains Mono\";'>PATIENT COORDINATES SCANNER</span>", unsafe_allow_html=True)
    c_lat, c_lon = st.columns(2)
    with c_lat:
        lat = st.number_input("LATITUDE", value=10.82, format="%.2f", label_visibility="collapsed")
    with c_lon:
        lon = st.number_input("LONGITUDE", value=106.63, format="%.2f", label_visibility="collapsed")
    st.caption("🚨 지정 좌표 반경의 원격 병원균 클러스터 인덱스를 반환합니다.")

# [6-3] 미생물 오염도 및 위험 구역 임상 예측 결과창
with col_prediction:
    # 필터링 기법으로 반경 내 클러스터 요격
    near_df = df[(df['위도'] >= lat-5) & (df['위도'] <= lat+5) & 
                 (df['경도'] >= lon-5) & (df['경도'] <= lon+5)]
    
    st.markdown("<span style='color: #2DD4BF; font-size: 0.75rem; font-weight: bold; font-family: \"JetBrains Mono\";'>EPIDEMIC FORECAST REPORT</span>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
    
    if not near_df.empty:
        main_cluster = int(near_df['cluster'].value_counts().idxmax())
        target_color = med_colors[main_cluster]
        target_text = med_status[main_cluster]
        
        # 임상 등급 결과 카드 표출
        st.markdown(f"""
            <div class='clinical-badge' style='background-color: {target_color}18; color: {target_color}; border: 1px solid {target_color}88;'>
                {target_text}
            </div>
        """, unsafe_allow_html=True)
        
        # 임상 수치에 따른 처방전 메시지 분기 활성화
        if main_cluster == 2:
            st.error("☣️ 비상 지침: 고감염성 구역입니다. N95 마스크를 상시 착용하고 즉시 6단계 손 위생 수칙을 가동하십시오.")
        elif main_cluster == 1:
            st.warning("⚠️ 모니터링 요망: 산발적 병원균 이동 경로입니다. 개인 방역 및 얼굴 터치 금지 수칙을 강화하십시오.")
        else:
            st.success("🔬 청정 판정: 대조군 대비 무해한 수준의 안정선입니다. 표준 위생 관리를 유지하십시오.")
            
    else:
        st.markdown("<div class='clinical-badge' style='background-color: #1E293B; color: #64748B; border: 1px solid #334155;'>🧪 STERILE / NO REPLICON FOUND</div>", unsafe_allow_html=True)
        st.markdown("<div style='color: #64748B; font-size: 0.75rem; margin-top: 8px; text-align: center;'>해당 구역은 샘플 누락 구역이거나 멸균 상태(Sterile) 코드가 유지되고 있습니다.</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
