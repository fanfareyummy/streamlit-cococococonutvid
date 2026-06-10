import streamlit as st
import pandas as pd
import json

# --- 1. 페이지 설정 및 메디컬 라이트 UI 테마 ---
st.set_page_config(
    page_title="스마트 의료 센터 - 바이러스 통합 관제",
    page_icon="🩺",
    layout="wide",
)

# 깨지는 외부 이미지 대신 순수 CSS 애니메이션으로 바이러스 효과 구현
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700&display=swap');

    .stApp { 
        background: linear-gradient(135deg, #F0F9FF 0%, #FFFFFF 100%);
        color: #1E293B;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 상단 의료 센터 헤더 */
    .hospital-header {
        background: white;
        border-bottom: 3px solid #0EA5E9;
        padding: 20px;
        margin-bottom: 25px;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .hospital-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0369A1;
    }
    .status-badge {
        background: #E0F2FE;
        border: 1px solid #0EA5E9;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.85rem;
        color: #0369A1;
        font-weight: 500;
    }

    /* 3D 화이트/블루 지구본 섹션 */
    .globe-section {
        background: linear-gradient(180deg, #FFFFFF 0%, #F0F9FF 100%);
        border: 1px solid #BAE6FD;
        border-radius: 24px;
        padding: 15px;
        box-shadow: 0 10px 30px rgba(14, 165, 233, 0.1);
    }

    /* [신설] 이미지 대체용 CSS 바이러스 배양기 현미경 효과 */
    .virus-microscope-box {
        background: radial-gradient(circle at center, #1E1B4B 0%, #030712 100%);
        height: 220px;
        border-radius: 20px;
        position: relative;
        overflow: hidden;
        border: 4px solid #E2E8F0;
        box-shadow: inset 0 0 30px rgba(239, 68, 68, 0.4);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .microscope-lens-grid {
        position: absolute;
        width: 100%;
        height: 100%;
        background-image: radial-gradient(rgba(0, 242, 255, 0.05) 2px, transparent 2px);
        background-size: 20px 20px;
    }
    .floating-virus-core {
        width: 40px;
        height: 40px;
        background: #EF4444;
        border-radius: 50%;
        box-shadow: 0 0 25px #EF4444, 0 0 50px #EF4444;
        animation: pulseAndFloat 4s ease-in-out infinite;
        position: relative;
    }
    .floating-virus-core::before, .floating-virus-core::after {
        content: '🦠';
        position: absolute;
        font-size: 24px;
        top: -10px; left: -10px;
    }

    @keyframes pulseAndFloat {
        0% { transform: scale(1) translate(0, 0); box-shadow: 0 0 20px #EF4444; }
        50% { transform: scale(1.2) translate(15px, -10px); box-shadow: 0 0 40px #FF0055; }
        100% { transform: scale(1) translate(0, 0); box-shadow: 0 0 20px #EF4444; }
    }

    /* 하단 가로형 스마트 제어 패널 */
    .control-panel {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid #BAE6FD;
        border-top: 4px solid #0EA5E9;
        border-radius: 20px;
        padding: 25px;
        margin-top: 30px;
        box-shadow: 0 -10px 30px rgba(14, 165, 233, 0.05);
    }

    div[data-baseweb="input"] { border-radius: 12px !important; border: 1px solid #CBD5E1 !important; }
    
    .medical-note {
        background: #F0FDF4;
        border-left: 5px solid #22C55E;
        padding: 15px;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #1E293B;
        line-height: 1.6;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 데이터 로드 ---
@st.cache_data
def load_data():
    file_name = "covid_risk_analysis_result.csv"
    try:
        data = pd.read_csv(file_name)
        return data[['위도', '경도', 'cluster']].dropna()
    except:
        return None

df = load_data()

if df is None:
    st.error("🔬 데이터 동기화 실패: 'covid_risk_analysis_result.csv' 파일이 필요합니다.")
    st.stop()

# --- 3. 헤더 섹션 ---
st.markdown("""
    <div class='hospital-header'>
        <div class='hospital-title'>🩺 스마트 의료 통합 관제 센터 <span>[V7.5 LIGHT]</span></div>
        <div class='status-badge'>● 로컬 그래픽 시스템 전면 구동됨</div>
    </div>
""", unsafe_allow_html=True)

# --- 4. 메인 콘텐츠 (좌측: 화사한 3D 지구본 / 우측: 실시간 바이러스 현미경 & 영상) ---
col_globe, col_micro = st.columns([2.1, 1.9])

with col_globe:
    st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0369A1; margin-bottom:10px;'>🌍 글로벌 병원균 확산 3D 시각화 매트릭스</p>", unsafe_allow_html=True)
    
    if 'lat_val' not in st.session_state: st.session_state.lat_val = 10.80
    if 'lon_val' not in st.session_state: st.session_state.lon_val = 106.60

    points_json = json.dumps(df.to_dict(orient="records"))
    
    hologram_globe_html = f"""
    <div class='globe-section'>
        <div id="medical-globe" style="width: 100%; height: 500px;"></div>
        
        <script src="https://unpkg.com/globe.gl"></script>
        <script>
            const rawData = {points_json};
            const gData = rawData.map(d => ({{
                lat: d['위도'], lng: d['경도'],
                size: d['cluster'] == 2 ? 0.7 : (d['cluster'] == 1 ? 0.45 : 0.25),
                color: d['cluster'] == 2 ? '#FF1E56' : (d['cluster'] == 1 ? '#FFAC1C' : '#00B4D8'),
                isTarget: false
            }}));

            // 사용자 입력 타겟 좌표 주입
            gData.push({{
                lat: {st.session_state.lat_val}, lng: {st.session_state.lon_val},
                size: 1.6, color: '#10B981', isTarget: true
            }});

            const globe = Globe()
                (document.getElementById('medical-globe'))
                .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-day.jpg')
                .backgroundColor('rgba(0,0,0,0)')
                .pointsData(gData)
                .pointRadius('size')
                .pointColor('color')
                .pointAltitude(d => d.isTarget ? 0.12 : 0.04)
                .pointLabel(d => d.isTarget ? `🎯 정밀 임상 추적 타겟` : `병원균 통계 지점`)
                .controlsMaxZoom(3);

            // 밝은 메디컬 아우라 광원(Atmosphere) 효과
            globe.atmosphereColor('#0EA5E9');
            globe.atmosphereRadiusScale(0.18);

            globe.pointOfView({{ lat: {st.session_state.lat_val}, lng: {st.session_state.lon_val}, alt: 1.9 }}, 1500);
            globe.controls().autoRotate = false;
        </script>
        <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.8rem; color: #64748B;">
            <div style="color: #10B981; font-weight: bold;">🎯 타겟 록온 지점: 위도 {st.session_state.lat_val}° / 경도 {st.session_state.lon_val}°</div>
            <div>
                <span style="color:#FF1E56;">●</span> 고위험 &nbsp;&nbsp;
                <span style="color:#FFAC1C;">●</span> 중위험 &nbsp;&nbsp;
                <span style="color:#00B4D8;">●</span> 안정구역
            </div>
        </div>
    </div>
    """
    st.components.v1.html(hologram_globe_html, height=580)

with col_micro:
    st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0369A1; margin-bottom:10px;'>🔬 실시간 현미경 세포 배양 시뮬레이터</p>", unsafe_allow_html=True)
    
    # [해결] 절대 안 깨지는 100% 로컬 CSS 코드로 렌더링된 현미경 박스 장착
    st.markdown("""
        <div class='virus-microscope-box'>
            <div class='microscope-lens-grid'></div>
            <div class='floating-virus-core'></div>
            <div style='position:absolute; bottom:10px; left:15px; color:#00F2FF; font-family:monospace; font-size:0.75rem;'>MAG: 45,000X <br>STATUS: ACTIVE</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""<div style='margin-top:20px;'></div>""", unsafe_allow_html=True)
    
    # 손씻기 6단계 유튜브 비디오 링크 (안전성 검증 완료)
    st.video("https://www.youtube.com/watch?v=aE0MEPeaks4")
    
    st.markdown(f"""
        <div class='medical-note'>
            <b style='font-size:1rem; color:#0369A1;'>📑 임상 관찰 요약</b><br>
            • 상단 배양 시뮬레이터 속 바이러스 변종은 생존력이 매우 강력합니다.<br>
            • <b>실험 결과:</b> 비누 없는 물 세척은 바이러스 외벽(Envelop)을 파괴하지 못해 감염력을 유지합니다.<br>
            • <b>해결책:</b> 30초 이상의 6단계 손씻기로 물리적/화학적 사멸을 유도하십시오.
        </div>
    """, unsafe_allow_html=True)

# --- 5. 하단 제어 패널 섹션 ---
st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
c_desc, c_input, c_result = st.columns([1, 1.4, 1.6])

with c_desc:
    # 이모지와 텍스트 조합으로 절대 안 깨지도록 로고 영역 변경
    st.markdown("""
        <div style='display: flex; gap: 15px; align-items: center;'>
            <div style='font-size: 2.5rem;'>🧬</div>
            <div>
                <div style='font-weight: 700; color: #0369A1;'>정밀 스캐너 가동</div>
                <div style='font-size: 0.8rem; color: #64748B;'>좌표 입력 시 구체가 추적합니다.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c_input:
    st.markdown("<span style='font-size: 0.8rem; font-weight: 700; color: #0EA5E9;'>TARGET COORDINATES</span>", unsafe_allow_html=True)
    i_lat, i_lon = st.columns(2)
    with i_lat:
        lat_in = st.number_input("위도", value=10.80, format="%.2f", label_visibility="collapsed", key="lat_input")
    with i_lon:
        lon_in = st.number_input("경도", value=106.60, format="%.2f", label_visibility="collapsed", key="lon_input")
    
    st.session_state.lat_val = lat_in
    st.session_state.lon_val = lon_in
    st.caption("🎯 위경도를 입력하고 Enter를 누르면 실시간 록온이 시작됩니다.")

with c_result:
    near_df = df[(df['위도'] >= lat_in-5) & (df['위도'] <= lat_in+5) & 
                 (df['경도'] >= lon_in-5) & (df['경도'] <= lon_in+5)]
    
    st.markdown("<span style='font-size: 0.8rem; font-weight: 700; color: #0EA5E9;'>DIAGNOSIS REPORT</span>", unsafe_allow_html=True)
    
    if not near_df.empty:
        main_c = int(near_df['cluster'].value_counts().idxmax())
        res_color = {0: '#0EA5E9', 1: '#F59E0B', 2: '#EF4444'}[main_c]
        res_text = {0: '안정(Normal) 🛡️', 1: '경계(Warning) ⚠️', 2: '위험(Infected) ☣️'}[main_c]
        
        st.markdown(f"""
            <div style='background:{res_color}15; color:{res_color}; border:2px solid {res_color}; padding:10px; border-radius:10px; text-align:center; font-weight:700; margin-bottom:10px;'>
                판독 등급: {res_text}
            </div>
        """, unsafe_allow_html=True)
        
        if main_c == 2:
            st.error("☣️ 긴급 지침: 해당 지역은 감염 농도가 매우 높습니다. 방역 프로토콜을 즉시 가동하십시오.")
        else:
            st.success("🔬 보고: 해당 구역은 현재 표준 위생 관리 범위 내에 있습니다.")
    else:
        st.markdown("<div style='background:#F1F5F9; color:#64748B; padding:10px; border-radius:10px; text-align:center; font-size:0.85rem;'>측정 범위 내 데이터 분석 불가능</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
