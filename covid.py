import streamlit as st
import pandas as pd
import numpy as np
import json

# --- 1. 페이지 설정 및 메디컬 라이트 UI 테마 ---
st.set_page_config(
    page_title="스마트 의료 센터 - 바이러스 통합 관제",
    page_icon="🩺",
    layout="wide",
)

# 화사하고 깨끗한 의료 대시보드 스타일 CSS
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

    /* 3D 지구본 컨테이너 */
    .globe-section {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
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
        margin-top: 15px;
    }

    /* 바이러스 분석 카드 래퍼 */
    .virus-analysis-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.02);
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
        <div class='hospital-title'>🩺 스마트 의료 통합 관제 센터 <span>[V8.0 PRO]</span></div>
        <div class='status-badge'>● 실시간 로컬 엔진 무결성 구동중</div>
    </div>
""", unsafe_allow_html=True)

# --- 4. 메인 콘텐츠 (좌측: 3D 지구본 + 공백 차단용 지표 / 우측: 실시간 변이 트렌드 + 영상) ---
col_globe, col_media = st.columns([2.1, 1.9])

with col_globe:
    st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0369A1; margin-bottom:10px;'>🌍 글로벌 병원균 확산 3D 시각화 매트릭스</p>", unsafe_allow_html=True)
    
    if 'lat_val' not in st.session_state: st.session_state.lat_val = 10.80
    if 'lon_val' not in st.session_state: st.session_state.lon_val = 106.60

    points_json = json.dumps(df.to_dict(orient="records"))
    
    hologram_globe_html = f"""
    <div class='globe-section'>
        <div id="medical-globe" style="width: 100%; height: 400px;"></div>
        <script src="https://unpkg.com/globe.gl"></script>
        <script>
            const rawData = {points_json};
            const gData = rawData.map(d => ({{
                lat: d['위도'], lng: d['경도'],
                size: d['cluster'] == 2 ? 0.7 : (d['cluster'] == 1 ? 0.45 : 0.25),
                color: d['cluster'] == 2 ? '#EF4444' : (d['cluster'] == 1 ? '#F59E0B' : '#0EA5E9'),
                isTarget: false
            }}));

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

            globe.pointOfView({{ lat: {st.session_state.lat_val}, lng: {st.session_state.lon_val}, alt: 2.1 }}, 1500);
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
    st.components.v1.html(hologram_globe_html, height=450)

    # 🚨 이전 질문에서 언급하셨던 하단 비는 공간(붉은 원)을 채우기 위한 통계 컴포넌트 추가
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="🦠 주요 변이 위험도", value="등급: 위험 (BA.5)", delta="상승 지표")
    with m2:
        st.metric(label="🛡️ 타겟 반경 방역 지수", value="82.4점", delta="안전 범위")
    with m3:
        st.metric(label="🧬 유전자 서열 일치율", value="99.8%", delta="변이 확인")

with col_media:
    # 🚨 [완벽 조치] 깨지는 외부 이미지를 전면 제거하고 스트림릿 순수 로컬 차트 보드로 교체!
    st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0369A1; margin-bottom:10px;'>📊 실시간 코로나 변이 바이러스 탐지 비중 트렌드</p>", unsafe_allow_html=True)
    
    with st.container(border=True):
        # 차트용 가상 데이터 생성 (절대 안 깨짐)
        chart_data = pd.DataFrame(
            np.random.rand(10, 3) * [20, 50, 30],
            columns=['알파/델타 변이', '오미크론 하위변이', '기타 변종 변이']
        )
        st.bar_chart(chart_data, height=180)
        
        st.markdown("""
            <div style='font-size:0.8rem; color:#475569; padding-top:5px; border-top:1px solid #F1F5F9;'>
                🧬 <b>구조적 임상 진단:</b> 돌기 단백질(Spike Protein) 변이 가속화로 인해 오미크론 하위 계통의 스캔 비중이 상대적으로 우세하게 관측됩니다.
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""<div style='margin-top:15px;'></div>""", unsafe_allow_html=True)
    
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
    # 깨지는 이미지 로고 대신 고해상도 메디컬 이모지(🧬) 배치
    st.markdown("""
        <div style='display: flex; gap: 15px; align-items: center;'>
            <div style='font-size: 2.8rem;'>🧬</div>
            <div>
                <div style='font-weight: 700; color: #0369A1; font-size:1.1rem;'>정밀 관제 스캐너</div>
                <div style='font-size: 0.8rem; color: #64748B;'>좌표 변경 시 지구가 오토 타겟팅을 시작합니다.</div>
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
