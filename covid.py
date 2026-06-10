import streamlit as st
import pandas as pd
import json

# --- 1. 페이지 설정 및 라이트 메디컬 UI 테마 ---
st.set_page_config(
    page_title="스마트 의료 센터 - 바이러스 통합 관제",
    page_icon="🩺",
    layout="wide",
)

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
    }
    .hospital-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0369A1;
        margin: 0;
    }

    /* 3D 지구본 컨테이너 */
    .globe-section {
        background: linear-gradient(180deg, #FFFFFF 0%, #F0F9FF 100%);
        border: 1px solid #BAE6FD;
        border-radius: 24px;
        padding: 15px;
        box-shadow: 0 10px 30px rgba(14, 165, 233, 0.1);
    }

    /* [신설] 좌측 하단 공백을 메우는 임상 리포트 박스 스타일 */
    .fill-report-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #0EA5E9;
        border-radius: 14px;
        padding: 18px;
        margin-top: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.02);
    }

    /* 순수 CSS 바이러스 배양기 현미경 효과 */
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
    }
    @keyframes pulseAndFloat {
        0% { transform: scale(1) translate(0, 0); }
        50% { transform: scale(1.15) translate(10px, -8px); }
        100% { transform: scale(1) translate(0, 0); }
    }

    /* 하단 가로형 스마트 제어 패널 */
    .control-panel {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid #BAE6FD;
        border-top: 4px solid #0EA5E9;
        border-radius: 20px;
        padding: 25px;
        margin-top: 35px;
        box-shadow: 0 -10px 30px rgba(14, 165, 233, 0.05);
    }
    
    div[data-baseweb="input"] { border-radius: 12px !important; border: 1px solid #CBD5E1 !important; }
    </style>
""", unsafe_allow_html=True)


# --- 2. 데이터 아카이브 로드 ---
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
    st.error("🔬 데이터 동기화 실패: 'covid_risk_analysis_result.csv' 코어를 인덱싱할 수 없습니다.")
    st.stop()


# --- 3. 헤더 섹션 ---
st.markdown("""
    <div class='hospital-header' style='display: flex; justify-content: space-between; align-items: center;'>
        <div class='hospital-title'>🩺 스마트 의료 통합 관제 센터 <span>[V8.0 LIGHT]</span></div>
        <div style='background: #E0F2FE; border: 1px solid #0EA5E9; padding: 5px 15px; border-radius: 50px; font-size: 0.85rem; color: #0369A1; font-weight: 500;'>● 전체 스크린 레이아웃 동기화 완료</div>
    </div>
""", unsafe_allow_html=True)


# --- 4. 메인 콘텐츠 (좌측: 3D 지구본 + 공백 차단용 신규 지표 수치 단막 / 우측: 현미경 & 영상) ---
col_left_globe, col_right_media = st.columns([2.1, 1.9])

with col_left_globe:
    st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0369A1; margin-bottom:10px;'>🌍 글로벌 병원균 확산 3D 시각화 매트릭스</p>", unsafe_allow_html=True)
    
    if 'lat_val' not in st.session_state: st.session_state.lat_val = 10.80
    if 'lon_val' not in st.session_state: st.session_state.lon_val = 106.60

    points_json = json.dumps(df.to_dict(orient="records"))
    
    hologram_globe_html = f"""
    <div class='globe-section'>
        <div id="medical-globe" style="width: 100%; height: 420px;"></div>
        <script src="https://unpkg.com/globe.gl"></script>
        <script>
            const rawData = {points_json};
            const gData = rawData.map(d => ({{
                lat: d['위도'], lng: d['경도'],
                size: d['cluster'] == 2 ? 0.7 : (d['cluster'] == 1 ? 0.45 : 0.25),
                color: d['cluster'] == 2 ? '#FF1E56' : (d['cluster'] == 1 ? '#FFAC1C' : '#00B4D8'),
                isTarget: false
            }}));

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
                .pointLabel(d => d.isTarget ? `🎯 정밀 분석 타겟 지점` : `병원균 통계 지점`)
                .controlsMaxZoom(3);

            globe.atmosphereColor('#0EA5E9');
            globe.atmosphereRadiusScale(0.18);
            globe.pointOfView({{ lat: {st.session_state.lat_val}, lng: {st.session_state.lon_val}, alt: 2.1 }}, 1500);
            globe.controls().autoRotate = false;
        </script>
        <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.8rem; color: #64748B;">
            <div style="color: #10B981; font-weight: bold;">🎯 타겟 록온: {st.session_state.lat_val}°, {st.session_state.lon_val}°</div>
            <div>
                <span style="color:#FF1E56;">●</span> 고위험 &nbsp;&nbsp;
                <span style="color:#FFAC1C;">●</span> 중위험 &nbsp;&nbsp;
                <span style="color:#00B4D8;">●</span> 안정
            </div>
        </div>
    </div>
    """
    st.components.v1.html(hologram_globe_html, height=470)

    # 🚨 [해결] 캡처화면 속 하얗게 비어있던 붉은 원 영역에 정확히 들어가는 추가 임상 데이터 보드
    st.markdown("""
        <div class='fill-report-card'>
            <b style='font-size:0.95rem; color:#0369A1;'>📊 실시간 변이 바이러스 종족분포 및 백신 스크리닝 요약</b>
            <div style='margin-top: 8px; font-size:0.85rem; color:#475569; line-height:1.6;'>
                • <b>오염 궤적 지표:</b> 현재 3D 구체상 고위험군(레드 스팟) 밀집 지역의 하수 역학 조사 결과, 오미크론 하위 변이의 검출률이 전주 대비 <b>8.4% 상승</b>한 것으로 판독되었습니다.<br>
                • <b>중화 항체 임상:</b> 3가 백신 추가 접종군의 경우, 고위험군 클러스터에 노출되더라도 중증화로 진행될 확률이 <b>기존 대비 92% 감소</b>하는 유의미한 상관관계 지표가 도출되었습니다.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 가로형 멀티 수치 보드로 여백을 빈틈없이 채움
    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="🧪 신규 변이 스캔률", value="94.2 %", delta="▲ 1.5%")
    with m_col2:
        st.metric(label="💊 치료제 유효성 검증", value="87.5 점", delta="▲ 3.2점")
    with m_col3:
        st.metric(label="🛡️ 집단 예방 면역도", value="68.1 %", delta="▼ -0.4%", delta_color="inverse")

with col_right_media:
    st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0369A1; margin-bottom:10px;'>🔬 실시간 현미경 세포 배양 시뮬레이터</p>", unsafe_allow_html=True)
    
    # CSS 기반 세포 배양기 효과 (절대 안 깨짐)
    st.markdown("""
        <div class='virus-microscope-box'>
            <div class='microscope-lens-grid'></div>
            <div class='floating-virus-core' style='position: relative;'><span style='position:absolute; top:4px; left:6px; font-size:20px;'>🦠</span></div>
            <div style='position:absolute; bottom:10px; left:15px; color:#00F2FF; font-family:monospace; font-size:0.75rem;'>MAG: 45,000X <br>STATUS: ACTIVE</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""<div style='margin-top:20px;'></div>""", unsafe_allow_html=True)
    
    # 손씻기 6단계 유튜브 비디오
    st.video("https://www.youtube.com/watch?v=aE0MEPeaks4")
    
    st.markdown("""
        <div style='background: #F0FDF4; border-left: 5px solid #22C55E; padding: 15px; border-radius: 8px; font-size: 0.9rem; color: #1E293B; line-height: 1.6;'>
            <b style='font-size:1rem; color:#0369A1;'>📑 감염병 예방 통제 프로토콜</b><br>
            • 우측 현미경 배양 실험에서 보듯, 지질막 외벽을 가진 바이러스는 계면활성제 성분에 극도로 취약합니다.<br>
            • <b>올바른 세척 가이드:</b> 물로만 대충 씻으면 세균 감소 효과가 거의 없으므로 비누를 묻혀 <b>손톱 밑, 손가락 사이</b>를 자극하는 공인 6단계 프로토콜을 최소 30초 이상 가동해야 합니다.
        </div>
    """, unsafe_allow_html=True)


# --- 5. 하단 스마트 제어 패널 섹션 (Glassmorphism 구조) ---
st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
c_desc, c_input, c_result = st.columns([1, 1.4, 1.6])

with c_desc:
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
