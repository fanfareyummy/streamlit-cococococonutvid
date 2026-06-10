import streamlit as st
import pandas as pd
import pydeck as pdk

# --- 1. 임상 관제 테마 및 홀로그램 이펙트 CSS 설정 ---
st.set_page_config(
    page_title="글로벌 코로나 위험 분석 및 통제 시스템",
    page_icon="🔬",
    layout="wide",
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700&display=swap');

    .stApp { 
        background: linear-gradient(135deg, #09111E 0%, #050A12 100%);
        color: #E2E8F0;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 최상단 시스템 통합 타이틀 바 */
    .system-header {
        border-bottom: 2px solid #06B6D4;
        padding-bottom: 12px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .system-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #22D3EE;
        text-shadow: 0 0 12px rgba(6, 182, 212, 0.6);
    }
    .system-tag {
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid #06B6D4;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.8rem;
        color: #38BDF8;
    }

    /* 홀로그램 프로젝터 장치 프레임 */
    .hologram-deck {
        background: radial-gradient(circle at center, #0B192C 0%, #050C16 100%);
        border: 2px solid #1E293B;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 0 40px rgba(6, 182, 212, 0.15);
        position: relative;
    }

    /* 홀로그램 하단 원형 프로젝터 베이스 기기 재현 */
    .projector-base {
        width: 100%;
        height: 12px;
        background: linear-gradient(90deg, #1E293B 0%, #06B6D4 50%, #1E293B 100%);
        border-radius: 50%;
        margin-top: -15px;
        box-shadow: 0 10px 30px rgba(6, 182, 212, 0.4);
        opacity: 0.7;
    }

    /* 하단 가로형 고정 임상 분석 제어판 (UI 깨짐 완벽 방지) */
    .control-console {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid #334155;
        border-top: 3px solid #06B6D4;
        border-radius: 16px;
        padding: 22px;
        margin-top: 25px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.5);
    }

    /* 인풋 박스 메디컬 스타일링 */
    div[data-baseweb="input"] { background-color: #050A12 !important; border: 1px solid #334155 !important; }
    
    .report-card {
        background: rgba(6, 182, 212, 0.04);
        border-left: 4px solid #06B6D4;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        font-size: 0.85rem;
        color: #94A3B8;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)


# --- 2. 임상 데이터 아카이브 로드 ---
@st.cache_data
def load_epidemic_data():
    file_name = "covid_risk_analysis_result.csv"
    try:
        data = pd.read_csv(file_name)
        # 이미지 속 3가지 위험도 색상 노드 매핑 (민트 계열 홀로그램 맵과 대비 효과)
        # 0: 노랑, 1: 주황, 2: 빨강 (반투명 발광 효과를 위해 알파값 조정)
        def assign_rgba(cluster):
            if cluster == 0: return [254, 240, 138, 180] # 낮은 위험 (노랑)
            if cluster == 1: return [249, 115, 22, 210]  # 중간 위험 (주황)
            return [239, 68, 68, 240]                    # 매우 높은 위험 (빨강)
            
        data['color'] = data['cluster'].apply(assign_rgba)
        return data
    except: return None

df = load_epidemic_data()

if df is None:
    st.error("🔬 국립 보건 데이터 시스템 에러: 'covid_risk_analysis_result.csv' 아카이브를 찾을 수 없습니다.")
    st.stop()


# --- 3. 위험 지수 정의 테이블 ---
colors_hex = {0: '#FEF08A', 1: '#F97316', 2: '#EF4444'}
status_kr = {0: '낮은 위험 단계 🟡', 1: '중간 위험 단계 🟠', 2: '매우 높은 위험 단계 🔴'}


# --- 4. 메인 관제 센터 상단 타이틀 ---
st.markdown("""
    <div class='system-header'>
        <div class='system-title'>🏥 글로벌 코로나 위험 분석 및 통제 시스템</div>
        <div class='system-tag'>● 실시간 보건 네트워크 연동됨</div>
    </div>
""", unsafe_allow_html=True)


# --- 5. 2분할 메인 레이아웃 (좌측: 3D 홀로그램 지구본 / 우측: 실시간 위생 검증 비디오) ---
col_hologram, col_media = st.columns([2.1, 1.9])

with col_hologram:
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#22D3EE; margin-bottom:5px;'>⚙️ 3D 홀로그램 입체 병원균 분포 매트릭스</p>", unsafe_allow_html=True)
    st.markdown("<div class='hologram-deck'>", unsafe_allow_html=True)
    
    # pydeck 3D 가상 레이어 구축
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position=["경도", "위도"],
        get_fill_color="color",
        get_radius=85000,
        pickable=True,
        opacity=0.85,
        filled=True,
    )
    
    # 민트색 홀로그램 우주 구체 공간 연출
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=pdk.ViewState(latitude=22, longitude=20, zoom=0.5, pitch=5, bearing=0),
        views=[pdk.View(type="_GlobeView", controller=True)],
        map_style=None, 
        tooltip={"text": "위험 등급 기전: {cluster}\n측정 좌표: {위도}, {경도}"}
    ))
    
    # 하단 빔 프로젝터 물리 장치 가시화 구현
    st.markdown("<div class='projector-base'></div>", unsafe_allow_html=True)
    
    # 이미지 우측 하단 범례 박스 완벽 복제
    st.markdown("""
        <div style='text-align: right; margin-top: 15px;'>
            <div style='display: inline-block; background: rgba(15, 23, 42, 0.8); border: 1px solid #1E293B; border-radius: 8px; padding: 8px 12px; text-align: left; font-size: 0.8rem;'>
                <span style='color:#EF4444;'>🔴</span> 매우 높은 위험<br>
                <span style='color:#F97316;'>🟠</span> 중간 위험<br>
                <span style='color:#FEF08A;'>🟡</span> 낮은 위험
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_media:
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#38BDF8; margin-bottom:5px;'>📹 역학 조사 실험: 손씻기 6단계 시각화 검증 분석</p>", unsafe_allow_html=True)
    
    # 스브스뉴스 손씻기 6단계 분석 비디오
    st.video("https://www.youtube.com/watch?v=aE0MEPeaks4")
    
    st.markdown("""
        <div class='report-card'>
            <b style='color:#FFF; font-size:0.9rem;'>🔬 CDC 감염병 역학 보고서: 최신 데이터 분석</b><br>
            • <b>종합 방어망 가동:</b> 코로나19 확산기 국민들의 손씻기 실천율이 14.2% 상승함에 따라 타 감염병(식중독, 결막염) 환자 수가 통계학적 최저치를 경신했습니다.<br>
            • <b>위생 불일치 통계:</b> 2,000명 관찰조사 결과 60% 이상이 비누 없이 물로만 세척하여 세균 전파 리스크가 여전히 높게 잔존하고 있습니다.<br>
            • <b>6단계 타겟 요격:</b> 장갑 물감 실험 결과, 1단계(손바닥) 세척법으로는 손등과 엄지손가락, 손톱 밑의 미생물이 전혀 제거되지 않으므로 질병관리청 공인 6단계 프로토콜을 반드시 이행해야 합니다.
        </div>
    """, unsafe_allow_html=True)


# --- 6. 하단 3분할 가로형 의학 제어 콘솔 패널 (절대 깨지지 않는 구조) ---
st.markdown("<div class='control-console'>", unsafe_allow_html=True)
col_lbl, col_in, col_out = st.columns([1.1, 1.4, 1.5])

# [6-1] 제어 헤드 설명 섹션
with col_lbl:
    st.markdown("""
        <div style='border-left: 3px solid #06B6D4; padding-left: 12px;'>
            <div style='font-size:0.75rem; color:#64748B; font-weight:bold;'>SECTION: SCANNERS</div>
            <div style='font-size: 0.95rem; font-weight: bold; margin-top: 5px; color: #E2E8F0;'>분석 제어 및 빠른 검색</div>
            <div style='font-size: 0.75rem; color: #475569; margin-top: 3px;'>역학 조사가 필요한 국소 지역의 위경도를 입력하십시오.</div>
        </div>
    """, unsafe_allow_html=True)

# [6-2] 위경도 좌표 인풋 창
with col_in:
    st.markdown("<span style='color: #38BDF8; font-size: 0.75rem; font-weight: bold;'>지정 좌표 실시간 추적 레이더</span>", unsafe_allow_html=True)
    lay_lat, lay_lon = st.columns(2)
    with lay_lat:
        lat = st.number_input("위도값", value=10.80, format="%.2f", label_visibility="collapsed")
    with lay_lon:
        lon = st.number_input("경도값", value=106.60, format="%.2f", label_visibility="collapsed")
    st.caption("🔍 지정 좌표 반경 500km 내 오염 확산 징후를 판독합니다.")

# [6-3] 임상 판독 결과 및 위생 처방 리포트
with col_out:
    # 지정 좌표 필터링 연산
    near_df = df[(df['위도'] >= lat-5) & (df['위도'] <= lat+5) & 
                 (df['경도'] >= lon-5) & (df['경도'] <= lon+5)]
    
    st.markdown("<span style='color: #22D3EE; font-size: 0.75rem; font-weight: bold;'>보건안전부 긴급 진단 통보</span>", unsafe_allow_html=True)
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
        
        # 위험 클러스터별 임상 처방전 문구 출력
        if main_cluster == 2:
            st.error("☣️ 고오염성 감염 궤적 지역입니다. 비누를 사용하여 손톱 밑까지 세척하는 6단계 방역 요법을 즉각 명령합니다.")
        elif main_cluster == 1:
            st.warning("⚠️ 주의 관찰 지역입니다. 점막 감염의 통로가 되는 시간당 36회의 무의식적 얼굴 접촉을 제어하십시오.")
        else:
            st.success("🔬 청정 대조 구역입니다. 노래 2회 부르기 주기(30초 임계값)의 표준 예방 수칙을 준수하십시오.")
    else:
        st.markdown("<div style='background:#1E293B; color:#475569; padding:9px; border-radius:6px; text-align:center; font-size:0.85rem;'>🧪 비집계 지역 / 미생물 활동 흔적 없음</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
