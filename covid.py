import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- 1. 임상 연구소 고정형 레이아웃 설정 ---
st.set_page_config(
    page_title="CLINICAL PATHOGEN & HAND HYGIENE COGNITION SYSTEM",
    page_icon="🧬",
    layout="wide",
)

# 보건의료 기관 대시보드 특유의 세련된 다크 사이언(Cyan) & 스네이크 메디컬 스킨
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Noto+Sans+KR:wght@300;500;700&display=swap');

    .stApp { 
        background-color: #070B14; 
        color: #E2E8F0;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 최상단 의료 관제 센터 헤더 */
    .medical-gate {
        border-bottom: 2px solid #06B6D4;
        padding-bottom: 15px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .gate-title {
        font-family: 'Fira Code', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        color: #06B6D4;
        letter-spacing: -0.5px;
    }
    .gate-title span {
        color: #38BDF8;
        font-size: 0.9rem;
        font-weight: 300;
    }
    .status-pulse {
        background-color: rgba(6, 182, 212, 0.1);
        border: 1px solid #06B6D4;
        padding: 5px 14px;
        border-radius: 4px;
        font-size: 0.75rem;
        color: #22D3EE;
        font-family: 'Fira Code', monospace;
    }

    /* 연구용 역학 지도 프레임 */
    .clinical-map-box {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 14px;
        padding: 10px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    /* 하단 가로형 고정 임상 분석 제어판 (절대 깨지지 않는 구조) */
    .control-console {
        background: #0F172A;
        border-top: 4px solid #06B6D4;
        border-radius: 12px;
        padding: 20px;
        margin-top: 25px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }

    /* 의학 임상 가이드 박스 */
    div[data-baseweb="input"] { background-color: #070B14 !important; border: 1px solid #334155 !important; color: #fff !important; }
    .lab-badge {
        padding: 10px;
        border-radius: 6px;
        font-weight: 700;
        text-align: center;
        font-size: 0.85rem;
    }
    
    .clinical-briefing {
        background: rgba(6, 182, 212, 0.03);
        border-left: 4px solid #38BDF8;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        font-size: 0.85rem;
        line-height: 1.6;
        color: #94A3B8;
    }
    </style>
""", unsafe_allow_html=True)


# --- 2. 임상 코어 데이터 로드 ---
@st.cache_data
def load_clinical_data():
    file_name = "covid_risk_analysis_result.csv"
    try:
        try: return pd.read_csv(file_name, encoding="utf-8")
        except: return pd.read_csv(file_name, encoding="cp949")
    except: return None

df = load_clinical_data()

if df is None:
    st.error("🔬 CLINICAL ERROR: 역학조사 결과 데이터 매트릭스 로드 실패.")
    st.stop()


# --- 3. 위험 인덱스 및 의료 시각화 컬러 노드 ---
# 0: 안전(Cyan), 1: 주의(Amber), 2: 고위험(Magenta)
colors_node = {0: '#06B6D4', 1: '#F59E0B', 2: '#D946EF'}
status_node = {
    0: '🟢 BIO-SECURE ZONES (감염 억제 상태)', 
    1: '🟠 WATCH RECTANGLE (변이 및 확산 경계)', 
    2: '🔴 PATHOGEN OUTBREAK (바이러스 밀집 통제 구역)'
}


# --- 4. 메인 화면 상단 보건 네트워크 헤더 ---
st.markdown("""
    <div class='medical-gate'>
        <div class='gate-title'>🧪 KDCA BIOMETRIC EPIDEMIC RADAR <span>[CORE LAYER v4.11]</span></div>
        <div class='status-pulse'>● SECURE CLINICAL LINK (ONLINE)</div>
    </div>
""", unsafe_allow_html=True)


# --- 5. 2분할 메인 연구 레이아웃 (좌측: 글로벌 감염 지도 / 우측: 실험 검증 비디오 및 통계학 노트) ---
col_map_view, col_media_view = st.columns([2.1, 1.9])

with col_map_view:
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#38BDF8; margin-bottom:5px;'>📊 GEOGRAPHIC TRANSMISSION RISK MATRIX MAP</p>", unsafe_allow_html=True)
    st.markdown("<div class='clinical-map-box'>", unsafe_allow_html=True)
    
    # 임상 관제 감성을 주는 CartoDB Dark 스킨 사용
    m = folium.Map(location=[25, 12], zoom_start=1.8, tiles="CartoDB dark_matter")
    
    for i in range(len(df)):
        cluster = int(df.iloc[i]['cluster'])
        folium.CircleMarker(
            location=[df.iloc[i]['위도'], df.iloc[i]['경도']],
            radius=4,
            color=colors_node[cluster],
            fill=True,
            fill_color=colors_node[cluster],
            fill_opacity=0.45,
            weight=1,
            popup=f"BIO-INDEX: {cluster}"
        ).add_to(m)
        
    st_folium(m, width=760, height=460, key="clinical_biometric_map")
    st.markdown("</div>", unsafe_allow_html=True)

with col_media_view:
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#06B6D4; margin-bottom:5px;'>📹 CLINICAL EXPERIMENT: 손씻기 6단계 시각화 검증 피드</p>", unsafe_allow_html=True)
    
    # 요청하신 스브스뉴스 올바른 손씻기 6단계 분석 영상 임베드
    st.video("https://www.youtube.com/watch?v=aE0MEPeaks4")
    
    # 임상 데이터 및 실험 기반의 초정밀 아카이브 브리핑 노출
    st.markdown("""
        <div class='clinical-briefing'>
            <b style='color:#FFF; font-size:0.9rem;'>🔬 임상 역학조사 보고서 (질병관리청 & 스브스 임상 데이터 요약)</b><br>
            • <b>교차 감염 차단력 증명:</b> 코로나19 확산으로 손씻기 실천율이 14.2% 상승하자 식중독 환자 수가 수년 내 최저치를 기록했으며 결막염 등 타 감염병 환자 수도 동반 급감했습니다[00:00:21].<br>
            • <b>비누 세척 변수 (2,000명 전수조사):</b> 용변 후 화장실 이용자 조사 결과, 75.4%만 손을 씻었으며 이 중 <b>60% 이상이 물로만 씻어</b> 균이 제거되지 않는 가짜 위생 상태였습니다[00:01:06].<br>
            • <b>장갑 물감 실험을 통한 6단계 필연성 입증:</b><br>
            &nbsp;&nbsp;1단계(손바닥)만 완료 시: 손등, 손가락 사이, 엄지, 손톱 밑이 모두 사각지대로 잔류[00:01:47].<br>
            &nbsp;&nbsp;2단계(손등), 3단계(손가락 사이), 4단계(손가락 주먹)를 거쳐도 <b>엄지손가락과 손톱 밑</b>은 여전히 오염 상태 유지[00:02:20].<br>
            • <b>임상 권장 규격 (30초 임계값):</b> 30초 이상 세척을 유도하기 위해 '생일 축하 노래'(약 15초)를 연속 <b>2회 제창</b>하며 세척하는 글로벌 표준 요법 권장[00:03:07].
        </div>
    """, unsafe_allow_html=True)


# --- 6. 하단 3분할 가로형 의학 콘솔 패널 (절대 깨지지 않는 구조) ---
st.markdown("<div class='control-console'>", unsafe_allow_html=True)
col_info, col_scanner, col_report = st.columns([1.1, 1.4, 1.5])

# [6-1] 섹션 인포 레이블
with col_info:
    st.markdown("""
        <div style='border-left: 3px solid #06B6D4; padding-left: 12px;'>
            <span style='color: #475569; font-size: 0.75rem; font-weight: bold; font-family: "Fira Code";'>SECTION: LAB COORDINATES</span>
            <div style='font-size: 0.9rem; font-weight: bold; margin-top: 5px; color: #E2E8F0;'>역학 표본 타겟 스캔</div>
            <div style='font-size: 0.75rem; color: #334155; margin-top: 3px;'>환자 발생 지점의 좌표를 격리 스캔 필터에 입력하십시오.</div>
        </div>
    """, unsafe_allow_html=True)

# [6-2] 좌표 추적 입력 장치
with col_scanner:
    st.markdown("<span style='color: #38BDF8; font-size: 0.75rem; font-weight: bold; font-family: \"Fira Code\";'>PATHOGEN RADIUS RADAR</span>", unsafe_allow_html=True)
    in_lat, in_lon = st.columns(2)
    with in_lat:
        lat = st.number_input("LATITUDE", value=10.82, format="%.2f", label_visibility="collapsed")
    with in_lon:
        lon = st.number_input("LONGITUDE", value=106.63, format="%.2f", label_visibility="collapsed")
    st.caption("🔍 입력된 위경도 반경 500km 내 생체 복제 기전 유무를 파악합니다.")

# [6-3] 임상 예측 및 위생 처방 리포트
with col_report:
    # 데이터 매칭 연산
    near_df = df[(df['위도'] >= lat-5) & (df['위도'] <= lat+5) & 
                 (df['경도'] >= lon-5) & (df['경도'] <= lon+5)]
    
    st.markdown("<span style='color: #22D3EE; font-size: 0.75rem; font-weight: bold; font-family: \"Fira Code\";'>IMMEDIATE CLINICAL DIAGNOSIS</span>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
    
    if not near_df.empty:
        main_cluster = int(near_df['cluster'].value_counts().idxmax())
        target_color = colors_node[main_cluster]
        target_text = status_node[main_cluster]
        
        # 의학 위험 등급 배지 표출
        st.markdown(f"""
            <div class='lab-badge' style='background-color: {target_color}15; color: {target_color}; border: 1px solid {target_color}66;'>
                {target_text}
            </div>
        """, unsafe_allow_html=True)
        
        # 비디오 임상 수치를 접목한 특이 처방전 메시지 동적 바인딩
        if main_cluster == 2:
            st.error("☣️ [BIO-HAZARD] 감염 밀집 구역입니다. 물로만 씻는 행위는 무효하며, 반드시 비누와 함께 '30초 손씻기 6단계 요법'을 의무 시행하십시오.")
        elif main_cluster == 1:
            st.warning("⚠️ [WATCH INDICATION] 경계 구역입니다. 무의식적인 시간당 36회의 얼굴 접촉(눈·코·입 변수)을 철저히 차단하고 소독 보강을 권장합니다.")
        else:
            st.success("🔬 [STERILE STABLE] 환경 정화 대조군 수준의 안전선입니다. 생일 축하 노래 2회 주기 수준의 일상적 방역 만으로 통제 가능합니다.")
            
    else:
        st.markdown("<div class='lab-badge' style='background-color: #1E293B; color: #475569; border: 1px solid #334155;'>🧪 SECURE ISOLATION / ZERO PATHOGEN</div>", unsafe_allow_html=True)
        st.markdown("<div style='color: #475569; font-size: 0.75rem; margin-top: 8px; text-align: center;'>해당 지점은 미생물 군집 분석 클러스터가 식별되지 않은 완전 격리 구역입니다.</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
