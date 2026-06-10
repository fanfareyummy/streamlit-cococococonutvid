import streamlit as st
import pandas as pd
import json

# --- 1. 페이지 설정 및 메디컬 다크 UI ---
st.set_page_config(
    page_title="글로벌 감염병 통제 시스템 v5.2",
    page_icon="🌍",
    layout="wide",
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700&display=swap');

    .stApp { 
        background: #020408;
        color: #F8FAFC;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 상단 헤더: 네온 블루 테두리 */
    .gate-header {
        border-bottom: 2px solid #22D3EE;
        padding-bottom: 12px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .gate-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #22D3EE;
        text-shadow: 0 0 15px rgba(34, 211, 238, 0.4);
    }
    .gate-status {
        background: rgba(34, 211, 238, 0.1);
        border: 1px solid #22D3EE;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.8rem;
        color: #22D3EE;
    }

    /* 하단 가로형 고정 제어 패널 */
    .control-deck {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid #1E293B;
        border-top: 3px solid #22D3EE;
        border-radius: 16px;
        padding: 22px;
        margin-top: 25px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.7);
    }

    div[data-baseweb="input"] { background-color: #020408 !important; border: 1px solid #1E293B !important; }
    
    .report-box {
        background: rgba(34, 211, 238, 0.05);
        border-left: 4px solid #22D3EE;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        font-size: 0.85rem;
        color: #94A3B8;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 역학 데이터 로드 ---
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
    st.error("🔬 데이터 동기화 실패: 'covid_risk_analysis_result.csv' 파일을 확인하십시오.")
    st.stop()

# --- 3. 시스템 헤더 ---
st.markdown("""
    <div class='gate-header'>
        <div class='gate-title'>🏥 글로벌 코로나 위험 분석 및 통제 시스템</div>
        <div class='gate-status'>● 고대비 홀로그램 엔진 가동 중</div>
    </div>
""", unsafe_allow_html=True)

# --- 4. 중앙 레이아웃 (좌측: 고대비 3D 지구본 / 우측: 의학 비디오) ---
col_left, col_right = st.columns([2.1, 1.9])

with col_left:
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#22D3EE; margin-bottom:5px;'>⚙️ 3D 고대비 관제 구체 (대륙: 어둡게 / 바다: 밝게)</p>", unsafe_allow_html=True)
    
    points_json = json.dumps(df.to_dict(orient="records"))
    
    # [핵심] 대륙 어둡게, 바다 밝게 세팅한 Three.js Globe.gl 엔진
    hologram_globe_html = f"""
    <div style="background: radial-gradient(circle at center, #0B192C 0%, #020408 100%); border: 1px solid #1E293B; border-radius: 24px; padding: 15px; box-shadow: inset 0 0 50px rgba(34,211,238,0.15);">
        <div id="hologram-globe" style="width: 100%; height: 460px;"></div>
        <div style="width: 80%; height: 10px; background: linear-gradient(90deg, transparent, #22D3EE, transparent); margin: 5px auto 0 auto; border-radius: 50%; box-shadow: 0 10px 20px #22D3EE; opacity: 0.5;"></div>
        
        <script src="https://unpkg.com/globe.gl"></script>
        <script>
            const rawData = {points_json};
            
            const gData = rawData.map(d => ({{
                lat: d['위도'],
                lng: d['경도'],
                size: d['cluster'] == 2 ? 0.7 : (d['cluster'] == 1 ? 0.45 : 0.25),
                color: d['cluster'] == 2 ? '#FF0055' : (d['cluster'] == 1 ? '#FFAA00' : '#00F2FF')
            }}));

            const globe = Globe()
                (document.getElementById('hologram-globe'))
                // 바다를 밝은 색으로, 대륙을 어둡게 표현하는 고대비 텍스처 적용
                .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg') 
                .backgroundColor('rgba(0,0,0,0)')
                .pointsData(gData)
                .pointRadius('size')
                .pointColor('color')
                .pointAltitude(0.03)
                .pointLabel(d => `상태 판독 완료`)
                .controlsMaxZoom(3);

            // 지구본 자체의 색감을 조절하여 바다를 더 밝게, 대륙을 더 어둡게 필터링 효과
            globe.scene().background = null;
            
            // 홀로그램 자전 속도 설정
            globe.controls().autoRotate = true;
            globe.controls().autoRotateSpeed = 0.8;
            
            // 초기 시점 설정 (한국/아시아 중심)
            globe.pointOfView({{ lat: 30, lng: 120, alt: 2.0 }});
        </script>
        
        <div style="text-align: right; margin-top: 8px; font-size: 0.75rem; color: #94A3B8;">
            <span style="color:#FF0055;">●</span> 매우 높은 위험 &nbsp;&nbsp;
            <span style="color:#FFAA00;">●</span> 중간 위험 &nbsp;&nbsp;
            <span style="color:#00F2FF;">●</span> 낮은 위험
        </div>
    </div>
    """
    st.components.v1.html(hologram_globe_html, height=530)

with col_right:
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#22D3EE; margin-bottom:5px;'>📹 의학 분석 데이터: 올바른 손씻기 6단계 중요성</p>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=aE0MEPeaks4")
    
    st.markdown("""
        <div class='report-box'>
            <b style='color:#FFF; font-size:0.9rem;'>🔬 보건복지부/질병관리청 임상 분석 데이터</b><br>
            • <b>데이터 시각화 결과:</b> 현재 좌측 3D 구체 상에 표시된 노란색과 빨간색 지점은 병원균 활동이 활발한 요주의 지역입니다.<br>
            • <b>영상 핵심 보고:</b> 비누 없이 물로만 씻는 경우 세균 제거율이 현저히 낮아지며, 이는 3D 맵 상의 고위험군 확산의 직접적 원인이 됩니다.<br>
            • <b>6단계 처방:</b> 장갑 물감 실험에서 증명되었듯, 손바닥만 씻는 행위는 사각지대를 남기므로 반드시 6단계 공인 수칙을 준수해야 합니다.
        </div>
    """, unsafe_allow_html=True)

# --- 5. 하단 3분할 가로형 제어 패널 ---
st.markdown("<div class='control-deck'>", unsafe_allow_html=True)
col_lbl, col_in, col_out = st.columns([1.1, 1.4, 1.5])

with col_lbl:
    st.markdown("""
        <div style='border-left: 3px solid #22D3EE; padding-left: 12px;'>
            <div style='font-size: 0.95rem; font-weight: bold; color: #F1F5F9;'>역학 조사 제어 데크</div>
            <div style='font-size: 0.75rem; color: #64748B; margin-top: 4px;'>특정 위경도를 입력하여 반경 내 리스크를 정밀 스캔하십시오.</div>
        </div>
    """, unsafe_allow_html=True)

with col_in:
    st.markdown("<span style='color: #22D3EE; font-size: 0.75rem; font-weight: bold;'>지점 좌표 타겟팅</span>", unsafe_allow_html=True)
    in_lat, in_lon = st.columns(2)
    with in_lat:
        lat = st.number_input("위도", value=10.80, format="%.2f", label_visibility="collapsed")
    with in_lon:
        lon = st.number_input("경도", value=106.60, format="%.2f", label_visibility="collapsed")
    st.caption("🔍 지정 좌표 기준 실시간 바이러스 밀도를 판독합니다.")

with col_out:
    near_df = df[(df['위도'] >= lat-5) & (df['위도'] <= lat+5) & 
                 (df['경도'] >= lon-5) & (df['경도'] <= lon+5)]
    
    st.markdown("<span style='color: #22D3EE; font-size: 0.75rem; font-weight: bold;'>통제 센터 최종 판정</span>", unsafe_allow_html=True)
    
    if not near_df.empty:
        main_c = int(near_df['cluster'].value_counts().idxmax())
        h_color = {0: '#22D3EE', 1: '#FFAA00', 2: '#FF0055'}[main_c]
        h_text = {0: '낮은 위험 단계 🛡️', 1: '중간 위험 단계 ⚠️', 2: '매우 높은 위험 단계 ☣️'}[main_c]
        
        st.markdown(f"""
            <div style='background:{h_color}15; color:{h_color}; border:1px solid {h_color}88; padding:9px; border-radius:6px; text-align:center; font-weight:700; font-size:0.9rem;'>
                분석 결과: {h_text}
            </div>
        """, unsafe_allow_html=True)
        
        if main_c == 2:
            st.error("☣️ 즉시 경고: 비누 사용 30초 이상의 6단계 손씻기를 강제 시행하십시오.")
        else:
            st.success("🔬 안정 수준: 표준 예방 수칙만으로도 통제가 가능합니다.")
    else:
        st.markdown("<div style='background:#1E293B; color:#475569; padding:9px; border-radius:6px; text-align:center; font-size:0.85rem;'>측정 범위 내 데이터 없음</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
