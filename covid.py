import streamlit as st
import pandas as pd
import json

# --- 1. 임상 관제 센터 레이아웃 및 3D 홀로그램 스타일링 ---
st.set_page_config(
    page_title="글로벌 감염병 통제 시스템",
    page_icon="🔮",
    layout="wide",
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700&display=swap');

    .stApp { 
        background: #020617;
        color: #F8FAFC;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 상단 보건 통제 센터 헤더 */
    .gate-header {
        border-bottom: 2px solid #06B6D4;
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
        text-shadow: 0 0 15px rgba(6, 182, 212, 0.6);
    }
    .gate-status {
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid #06B6D4;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.8rem;
        color: #38BDF8;
    }

    /* 가로형 하단 제어 통제판 (절대 깨지지 않는 유연한 박스) */
    .control-center-deck {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid #1E293B;
        border-top: 3px solid #06B6D4;
        border-radius: 16px;
        padding: 22px;
        margin-top: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }

    div[data-baseweb="input"] { background-color: #020617 !important; border: 1px solid #334155 !important; }
    
    .clinical-brief {
        background: rgba(6, 182, 212, 0.03);
        border-left: 4px solid #06B6D4;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        font-size: 0.85rem;
        color: #94A3B8;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)


# --- 2. 임상 아카이브 데이터 로드 ---
@st.cache_data
def load_data():
    file_name = "covid_risk_analysis_result.csv"
    try:
        data = pd.read_csv(file_name)
        # 웹 프레임과 호환을 위해 필수 칼럼만 정제
        return data[['위도', '경도', 'cluster']].dropna()
    except:
        return None

df = load_data()

if df is None:
    st.error("🔬 데이터 통신 실패: 'covid_risk_analysis_result.csv' 파일을 읽을 수 없습니다.")
    st.stop()


# --- 3. 시스템 헤더 배치 ---
st.markdown("""
    <div class='gate-header'>
        <div class='gate-title'>🏥 글로벌 코로나 위험 분석 및 통제 시스템</div>
        <div class='gate-status'>● 3D 홀로그램 코어 네트워크 연결됨</div>
    </div>
""", unsafe_allow_html=True)


# --- 4. 중앙 2분할 레이아웃 (좌측: 진짜 3D 구체 홀로그램 / 우측: 의학 비디오) ---
col_left_globe, col_right_info = st.columns([2.1, 1.9])

with col_left_globe:
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#22D3EE; margin-bottom:5px;'>⚙️ 실시간 웹 가속 기반 3D 디지털 홀로그램 구체</p>", unsafe_allow_html=True)
    
    # 파이썬 데이터셋을 자바스크립트용 JSON 데이터로 바인딩
    points_json = json.dumps(df.to_dict(orient="records"))
    
    # [핵심] Three.js 기반 3D 글로벌 구체 엔진 주입 (종이 지도 탈피)
    hologram_globe_html = f"""
    <div style="background: radial-gradient(circle at center, #0B192C 0%, #020617 100%); border: 1px solid #1E293B; border-radius: 24px; padding: 15px; box-shadow: 0 0 30px rgba(6,182,212,0.15); text-align: center;">
        <div id="globe-3d-canvas" style="width: 100%; height: 460px;"></div>
        <div style="width: 70%; height: 8px; background: linear-gradient(90deg, transparent, #06B6D4, transparent); margin: 5px auto 0 auto; border-radius: 50%; box-shadow: 0 10px 25px #06B6D4; opacity: 0.6;"></div>
        
        <script src="https://unpkg.com/globe.gl"></script>
        <script>
            const rawData = {points_json};
            
            // 데이터 매핑 가공
            const gData = rawData.map(d => ({{
                lat: d['위도'],
                lng: d['경도'],
                size: d['cluster'] == 2 ? 0.6 : (d['cluster'] == 1 ? 0.4 : 0.2),
                color: d['cluster'] == 2 ? '#F43F5E' : (d['cluster'] == 1 ? '#FB923C' : '#22D3EE')
            }}));

            // 3D 구체(Globe) 컨텍스트 생성 및 초기화
            const globe = Globe()
                (document.getElementById('globe-3d-canvas'))
                .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-dark.jpg') // 실제 구체 텍스처 랩핑
                .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
                .backgroundColor('rgba(0,0,0,0)') // 투명 우주 배경
                .pointsData(gData)
                .pointRadius('size')
                .pointColor('color')
                .pointAltitude(0.02)
                .pointLabel(d => `위험도 단계`)
                .controlsMaxZoom(3);

            // 홀로그램 관제실 특유의 청록빛 네온 대기 질감 투사
            globe.scene().fog = new THREE.FogExp2('#06B6D4', 0.002);
            
            // 자동 자전 궤도 생성 (홀로그램 회전 효과)
            globe.controls().autoRotate = true;
            globe.controls().autoRotateSpeed = 1.2;
            
            // 초기 배율 설정
            globe.pointOfView({{ lat: 20, lng: 110, alt: 1.8 }});
        </script>
        
        <div style="text-align: right; margin-top: 5px; font-size: 0.75rem;">
            <span style="color:#F43F5E;">■</span> 매우 높은 위험 &nbsp;&nbsp;
            <span style="color:#FB923C;">■</span> 중간 위험 &nbsp;&nbsp;
            <span style="color:#22D3EE;">■</span> 낮은 위험
        </div>
    </div>
    """
    # 스트림릿 내부에 보안 격리를 해제하고 3D 엔진 직접 투사
    st.components.v1.html(hologram_globe_html, height=520, scrolling=False)

with col_right_info:
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#38BDF8; margin-bottom:5px;'>📹 역학 조사 실험 결과 피드: 손씻기 6단계 분석</p>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=aE0MEPeaks4")
    
    st.markdown("""
        <div class='clinical-brief'>
            <b style='color:#FFF; font-size:0.9rem;'>🔬 CDC 감염병 역학 보고서: 최신 데이터 분석</b><br>
            • <b>종합 방어망 가동:</b> 코로나19 확산기 국민들의 손씻기 실천율이 14.2% 상승함에 따라 타 감염병(식중독, 결막염) 환자 수가 통계학적 최저치를 경신했습니다.<br>
            • <b>위생 불일치 통계:</b> 2,000명 관찰조사 결과 60% 이상이 비누 없이 물로만 세척하여 세균 전파 리스크가 여전히 높게 잔존하고 있습니다.<br>
            • <b>6단계 타겟 요격:</b> 장갑 물감 실험 결과, 1단계(손바닥) 세척법으로는 손등과 엄지손가락, 손톱 밑의 미생물이 전혀 제거되지 않으므로 질병관리청 공인 6단계 프로토콜을 반드시 이행해야 합니다.
        </div>
    """, unsafe_allow_html=True)


# --- 5. 하단 가로형 고정 임상 분석 제어판 (절대 안 깨짐) ---
st.markdown("<div class='control-center-deck'>", unsafe_allow_html=True)
col_lbl, col_in, col_out = st.columns([1.1, 1.4, 1.5])

with col_lbl:
    st.markdown("""
        <div style='border-left: 3px solid #06B6D4; padding-left: 12px;'>
            <div style='font-size: 0.95rem; font-weight: bold; color: #E2E8F0;'>분석 제어 및 빠른 검색</div>
            <div style='font-size: 0.75rem; color: #475569; margin-top: 4px;'>역학 조사가 필요한 국소 지역의 위경도를 입력하십시오.</div>
        </div>
    """, unsafe_allow_html=True)

with col_in:
    st.markdown("<span style='color: #38BDF8; font-size: 0.75rem; font-weight: bold;'>지정 좌표 실시간 추적 레이더</span>", unsafe_allow_html=True)
    lay_lat, lay_lon = st.columns(2)
    with lay_lat:
        lat = st.number_input("위도값", value=10.80, format="%.2f", label_visibility="collapsed")
    with lay_lon:
        lon = st.number_input("경도값", value=106.60, format="%.2f", label_visibility="collapsed")
    st.caption("🔍 지정 좌표 반경 500km 내 오염 확산 징후를 판독합니다.")

with col_out:
    near_df = df[(df['위도'] >= lat-5) & (df['위도'] <= lat+5) & 
                 (df['경도'] >= lon-5) & (df['경도'] <= lon+5)]
    
    st.markdown("<span style='color: #22D3EE; font-size: 0.75rem; font-weight: bold;'>보건안전부 긴급 진단 통보</span>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
    
    if not near_df.empty:
        main_cluster = int(near_df['cluster'].value_counts().idxmax())
        h_color = {0: '#22D3EE', 1: '#FB923C', 2: '#F43F5E'}[main_cluster]
        h_text = {0: '낮은 위험 단계 🟡', 1: '중간 위험 단계 🟠', 2: '매우 높은 위험 단계 🔴'}[main_cluster]
        
        st.markdown(f"""
            <div style='background:{h_color}12; color:{h_color}; border:1px solid {h_color}AA; padding:9px; border-radius:6px; text-align:center; font-weight:700; font-size:0.9rem;'>
                현재 구역 상태: {h_text}
            </div>
        """, unsafe_allow_html=True)
        
        if main_cluster == 2:
            st.error("☣️ 고오염성 감염 궤적 지역입니다. 비누를 사용하여 손톱 밑까지 세척하는 6단계 방역 요법을 즉각 명령합니다.")
        elif main_cluster == 1:
            st.warning("⚠️ 주의 관찰 지역입니다. 점막 감염의 통로가 되는 시간당 36회의 무의식적 얼굴 접촉을 제어하십시오.")
        else:
            st.success("🔬 청정 대조 구역입니다. 노래 2회 부르기 주기(30초 임계값)의 표준 예방 수칙을 준수하십시오.")
    else:
        st.markdown("<div style='background:#1E293B; color:#475569; padding:9px; border-radius:6px; text-align:center; font-size:0.85rem;'>🧪 비집계 지역 / 미생물 활동 흔적 없음</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
