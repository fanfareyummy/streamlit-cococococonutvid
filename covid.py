import streamlit as st
import pandas as pd
import pydeck as pdk

# --- 1. 임상 관제 센터 레이아웃 및 홀로그램 이펙트 ---
st.set_page_config(
    page_title="글로벌 코로나 위험 분석 및 통제 시스템",
    page_icon="🔬",
    layout="wide",
)

# 100% 한국어 인터페이스 및 홀로그램 전용 폰트 스타일링
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Noto+Sans+KR:wght@300;500;700&display=swap');

    .stApp { 
        background: radial-gradient(circle at center, #06111E 0%, #02060D 100%);
        color: #E2E8F0;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 상단 시스템 헤더 */
    .system-header {
        border-bottom: 2px dashed #00FFCC;
        padding-bottom: 12px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .system-title {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #00FFCC;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.6);
    }
    .system-tag {
        background: rgba(0, 255, 204, 0.05);
        border: 1px solid #00FFCC;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.8rem;
        color: #00FFCC;
        font-family: 'Share Tech Mono', monospace;
    }

    /* 홀로그램 프로젝터 이펙트 코어 프레임 */
    .hologram-viewport {
        background: linear-gradient(180deg, rgba(0, 255, 204, 0.02) 0%, rgba(5, 12, 22, 0.8) 80%, rgba(0, 255, 204, 0.08) 100%);
        border: 1px solid #1E293B;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 0 50px rgba(0, 255, 204, 0.1), inset 0 0 30px rgba(0, 255, 204, 0.05);
        position: relative;
    }

    /* 하단 홀로그램 투사 레이저 이미터 장치 구현 */
    .hologram-emitter {
        width: 80%;
        height: 16px;
        background: linear-gradient(90deg, transparent 0%, #00FFCC 50%, transparent 100%);
        border-radius: 50%;
        margin: -10px auto 15px auto;
        box-shadow: 0 10px 40px rgba(0, 255, 204, 0.8), 0 -5px 20px rgba(0, 255, 204, 0.5);
        opacity: 0.85;
    }

    /* 하단 가로형 고정 임상 제어 데크 (깨짐 방지 가로 배치 프레임) */
    .control-deck {
        background: rgba(10, 20, 35, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid #1E293B;
        border-top: 3px solid #00FFCC;
        border-radius: 16px;
        padding: 22px;
        margin-top: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }

    div[data-baseweb="input"] { background-color: #030811 !important; border: 1px solid #1E293B !important; }
    
    .medical-report {
        background: rgba(0, 255, 204, 0.03);
        border-left: 4px solid #00FFCC;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        font-size: 0.85rem;
        color: #94A3B8;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)


# --- 2. 임상 데이터 로드 및 3D 피처 가공 ---
@st.cache_data
def load_hologram_data():
    file_name = "covid_risk_analysis_result.csv"
    try:
        data = pd.read_csv(file_name)
        # 네온 그리드 지구본 위에서 레이저빔처럼 솟구치도록 입체 높이값(Elevation)과 가열된 컬러 부여
        def assign_biometric(cluster):
            if cluster == 0: return [0, 255, 204, 220], 30000    # 낮은 위험: 형광 민트 / 30km 높이
            if cluster == 1: return [255, 170, 0, 240], 60000    # 중간 위험: 네온 오렌지 / 60km 높이
            return [255, 0, 100, 255], 120000                    # 매우 높은 위험: 핫핑크 레드 / 120km 높이
            
        bio_features = data['cluster'].apply(assign_biometric)
        data['color'] = [f[0] for f in bio_features]
        data['elevation'] = [f[1] for f in bio_features]
        return data
    except: return None

df = load_hologram_data()

if df is None:
    st.error("🔬 데이터 통신 오류: 원격 'covid_risk_analysis_result.csv' 코어를 인덱싱할 수 없습니다.")
    st.stop()

colors_hex = {0: '#00FFCC', 1: '#FFAA00', 2: '#FF0064'}
status_kr = {0: '낮은 위험 격리 상태 🟡', 1: '중간 위험 경계 단계 🟠', 2: '매우 높은 변이 Outbreak 🔴'}


# --- 3. 시스템 상단 바 ---
st.markdown("""
    <div class='system-header'>
        <div class='system-title'>🏥 글로벌 코로나 위험 분석 및 통제 시스템</div>
        <div class='system-tag'>HOLOGRAM GRID PORT CONNECTED</div>
    </div>
""", unsafe_allow_html=True)


# --- 4. 중앙 2분할 레이아웃 (좌측: 홀로그램 3D 지구본 / 우측: 위생 데이터 비디오) ---
col_left, col_right = st.columns([2.1, 1.9])

with col_left:
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#00FFCC; margin-bottom:5px;'>⚙️ 입체 레이저 프로젝션: 3D 디지털 홀로그램 지구본</p>", unsafe_allow_html=True)
    st.markdown("<div class='hologram-viewport'>", unsafe_allow_html=True)
    
    # [진짜 홀로그램의 핵심] 평면 점이 아니라, 대륙 그리드 위로 칼날처럼 솟구치는 3D ColumnLayer 활용
    hologram_layer = pdk.Layer(
        "ColumnLayer",
        df,
        get_position=["경도", "위도"],
        get_fill_color="color",
        get_elevation="elevation",
        elevation_scale=5,
        radius=60000,
        pickable=True,
        extruded=True, # 입체 기둥 형태로 돌출시켜 입체감 폭발
    )
    
    # 대륙선이 미래지향적 가상선으로 렌더링되는 다크 사이버 테마 맵 적용
    st.pydeck_chart(pdk.Deck(
        layers=[hologram_layer],
        initial_view_state=pdk.ViewState(
            latitude=20, 
            longitude=80, 
            zoom=0.4, 
            pitch=35, # 비스듬히 눕혀서 기둥이 하늘로 투사되는 간지 극대화
            bearing=10
        ),
        views=[pdk.View(type="_GlobeView", controller=True)],
        map_style="mapbox://styles/mapbox/dark-v11", # 미니멀 대륙 실루엣 스타일
        tooltip={"text": "바이러스 클러스터: {cluster}\n정밀 고도: {elevation}m\n위경도: {위도}, {경도}"}
    ))
    
    # 빔이 솟아나오는 레이저 베이스 기기 시각화 장치 배치
    st.markdown("<div class='hologram-emitter'></div>", unsafe_allow_html=True)
    
    # 우측 하단 미니멀 범례 박스
    st.markdown("""
        <div style='text-align: right; margin-top: 5px;'>
            <div style='display: inline-block; background: rgba(5, 12, 22, 0.9); border: 1px solid #00FFCC33; border-radius: 6px; padding: 6px 12px; text-align: left; font-size: 0.75rem; font-family: monospace;'>
                <span style='color:#FF0064;'>■</span> 매우 높은 위험 (120km 투사)<br>
                <span style='color:#FFAA00;'>■</span> 중간 위험 (60km 투사)<br>
                <span style='color:#00FFCC;'>■</span> 낮은 위험 (30km 투사)
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#00FFCC; margin-bottom:5px;'>📹 역학 조사 실험 결과 피드: 손씻기 6단계 분석</p>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=aE0MEPeaks4")
    
    st.markdown("""
        <div class='medical-report'>
            <b style='color:#FFF; font-size:0.9rem;'>🔬 CDC 감염병 역학 보고서: 최신 데이터 분석</b><br>
            • <b>종합 방어망 가동:</b> 코로나19 확산기 국민들의 손씻기 실천율이 14.2% 상승함에 따라 타 감염병(식중독, 결막염) 환자 수가 통계학적 최저치를 경신했습니다.<br>
            • <b>위생 불일치 통계:</b> 2,000명 관찰조사 결과 60% 이상이 비누 없이 물로만 세척하여 세균 전파 리스크가 여전히 높게 잔존하고 있습니다.<br>
            • <b>6단계 타겟 요격:</b> 장갑 물감 실험 결과, 1단계(손바닥) 세척법으로는 손등과 엄지손가락, 손톱 밑의 미생물이 전혀 제거되지 않으므로 질병관리청 공인 6단계 프로토콜을 반드시 이행해야 합니다.
        </div>
    """, unsafe_allow_html=True)


# --- 5. 하단 3분할 가로형 의학 제어 콘솔 패널 (절대 깨지지 않는 구조) ---
st.markdown("<div class='control-deck'>", unsafe_allow_html=True)
col_lbl, col_in, col_out = st.columns([1.1, 1.4, 1.5])

with col_lbl:
    st.markdown("""
        <div style='border-left: 3px solid #00FFCC; padding-left: 12px;'>
            <div style='font-size: 0.95rem; font-weight: bold; color: #E2E8F0;'>분석 제어 및 빠른 검색</div>
            <div style='font-size: 0.75rem; color: #475569; margin-top: 4px;'>역학 조사가 필요한 국소 지역의 위경도를 입력하십시오.</div>
        </div>
    """, unsafe_allow_html=True)

with col_in:
    st.markdown("<span style='color: #00FFCC; font-size: 0.75rem; font-weight: bold;'>지정 좌표 실시간 추적 레이더</span>", unsafe_allow_html=True)
    lay_lat, lay_lon = st.columns(2)
    with lay_lat:
        lat = st.number_input("위도값", value=10.80, format="%.2f", label_visibility="collapsed")
    with lay_lon:
        lon = st.number_input("경도값", value=106.60, format="%.2f", label_visibility="collapsed")
    st.caption("🔍 지정 좌표 반경 500km 내 오염 확산 징후를 판독합니다.")

with col_out:
    near_df = df[(df['위도'] >= lat-5) & (df['위도'] <= lat+5) & 
                 (df['경도'] >= lon-5) & (df['경도'] <= lon+5)]
    
    st.markdown("<span style='color: #00FFCC; font-size: 0.75rem; font-weight: bold;'>보건안전부 긴급 진단 통보</span>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
    
    if not near_df.empty:
        main_cluster = int(near_df['cluster'].value_counts().idxmax())
        h_color = colors_hex[main_cluster]
        h_text = status_kr[main_cluster]
        
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
