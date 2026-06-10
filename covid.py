import streamlit as st
import pandas as pd
import json

# --- 1. 페이지 설정 및 메디컬 라이트 UI 테마 ---
st.set_page_config(
    page_title="스마트 의료 센터 - 바이러스 통합 관제",
    page_icon="🩺",
    layout="wide",
)

# 화사하고 깨끗한 의료용 대시보드 스타일 CSS
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
        display: flex;
        align-items: center;
        gap: 10px;
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

    /* 3D 홀로그램 지구본 섹션 */
    .globe-section {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }

    /* 바이러스 분석 카드 */
    .virus-info-card {
        background: #F8FAFC;
        border-radius: 20px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        margin-top: 20px;
    }

    /* 하단 가로형 스마트 제어 패널 (Glassmorphism 적용) */
    .control-panel {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid #BAE6FD;
        border-top: 4px solid #0EA5E9;
        border-radius: 20px;
        padding: 25px;
        margin-top: 30px;
        box-shadow: 0 -10px 30px rgba(14, 165, 233, 0.05);
    }

    /* 입력 필드 스타일 */
    div[data-baseweb="input"] { border-radius: 12px !important; border: 1px solid #CBD5E1 !important; }
    
    .medical-note {
        background: #F0FDF4;
        border-left: 5px solid #22C55E;
        padding: 15px;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #1E293B;
        line-height: 1.6;
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
    st.error("🔬 데이터 동기화 실패: 아카이브 파일을 확인하십시오.")
    st.stop()

# --- 3. 헤더 섹션 ---
st.markdown("""
    <div class='hospital-header'>
        <div class='hospital-title'>🩺 스마트 의료 통합 관제 센터 <span>[V6.5 PRO]</span></div>
        <div class='status-badge'>● 실시간 보건 네트워크 활성화됨</div>
    </div>
""", unsafe_allow_html=True)

# --- 4. 메인 콘텐츠 (좌측: 3D 지구본 / 우측: 바이러스 현미경 & 영상) ---
col_globe, col_micro = st.columns([2.1, 1.9])

with col_globe:
    st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0369A1; margin-bottom:10px;'>🌍 글로벌 병원균 확산 3D 시각화 매트릭스</p>", unsafe_allow_html=True)
    
    # 하단 제어판에서 입력된 좌표를 미리 받기 위해 순서를 조정하거나 기본값 설정
    # (Streamlit은 상단부터 실행하므로 나중에 정의될 변수를 위해 기본값을 설정함)
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
                color: d['cluster'] == 2 ? '#EF4444' : (d['cluster'] == 1 ? '#F59E0B' : '#0EA5E9'),
                isTarget: false
            }}));

            // 사용자 입력 타겟 좌표 추가
            gData.push({{
                lat: {st.session_state.lat_val}, lng: {st.session_state.lon_val},
                size: 1.5, color: '#22C55E', isTarget: true
            }});

            const globe = Globe()
                (document.getElementById('medical-globe'))
                .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
                .backgroundColor('rgba(0,0,0,0)')
                .pointsData(gData)
                .pointRadius('size')
                .pointColor('color')
                .pointAltitude(d => d.isTarget ? 0.1 : 0.03)
                .pointLabel(d => d.isTarget ? `🎯 정밀 분석 타겟` : `관찰 데이터`)
                .controlsMaxZoom(3);

            globe.pointOfView({{ lat: {st.session_state.lat_val}, lng: {st.session_state.lon_val}, alt: 2.0 }}, 1500);
            globe.controls().autoRotate = false;
        </script>
        <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.8rem; color: #64748B;">
            <div style="color: #22C55E; font-weight: bold;">🎯 타겟 록온: {st.session_state.lat_val}°, {st.session_state.lon_val}°</div>
            <div>
                <span style="color:#EF4444;">●</span> 위중증 &nbsp;&nbsp;
                <span style="color:#F59E0B;">●</span> 경계 &nbsp;&nbsp;
                <span style="color:#0EA5E9;">●</span> 안정
            </div>
        </div>
    </div>
    """
    st.components.v1.html(hologram_globe_html, height=580)

with col_micro:
    st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0369A1; margin-bottom:10px;'>🔬 바이러스 미생물 분석 리포트</p>", unsafe_allow_html=True)
    
    # 검색된 바이러스 GIF 이미지 삽입
    st.image("http://googleusercontent.com/image_collection/image_retrieval/11640972239884877934", caption="현미경으로 관찰된 코로나 바이러스 구조 (실시간 렌더링)", use_container_width=True)
    
    st.markdown("""<div style='margin-top:20px;'></div>""", unsafe_allow_html=True)
    
    # 손씻기 6단계 영상
    st.video("https://www.youtube.com/watch?v=aE0MEPeaks4")
    
    st.markdown(f"""
        <div class='medical-note'>
            <b style='font-size:1rem; color:#0369A1;'>📑 임상 관찰 요약</b><br>
            • 현재 분석 중인 바이러스 변종은 점막을 통한 침투력이 매우 강력합니다.<br>
            • <b>실험 결과:</b> 비누 없는 물 세척은 바이러스 외벽(Envelop)을 파괴하지 못해 감염력을 유지합니다.<br>
            • <b>해결책:</b> 30초 이상의 6단계 손씻기로 물리적/화학적 사멸을 유도하십시오.
        </div>
    """, unsafe_allow_html=True)

# --- 5. 하단 제어 패널 섹션 ---
st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
c_desc, c_input, c_result = st.columns([1, 1.4, 1.6])

with c_desc:
    # 의료 센터 로고 스타일 이미지 삽입
    st.image("http://googleusercontent.com/image_collection/image_retrieval/9673394217972218586", width=80)
    st.markdown("""
        <div style='margin-top: 10px;'>
            <div style='font-weight: 700; color: #0369A1;'>정밀 스캐너 가동</div>
            <div style='font-size: 0.8rem; color: #64748B;'>타겟 지점의 위경도를 입력하면 지구본이 자동 추적합니다.</div>
        </div>
    """, unsafe_allow_html=True)

with c_input:
    st.markdown("<span style='font-size: 0.8rem; font-weight: 700; color: #0EA5E9;'>TARGET COORDINATES</span>", unsafe_allow_html=True)
    i_lat, i_lon = st.columns(2)
    with i_lat:
        lat_in = st.number_input("위도", value=10.80, format="%.2f", label_visibility="collapsed", key="lat_input")
    with i_lon:
        lon_in = st.number_input("경도", value=106.60, format="%.2f", label_visibility="collapsed", key="lon_input")
    
    # 입력값을 세션 상태에 저장하여 지도와 동기화
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
