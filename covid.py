import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- 1. 페이지 설정 및 완전 검정(Pure Black) 미니멀 테마 ---
st.set_page_config(
    page_title="COVID-19 위험 분석 시스템",
    page_icon="▪️",
    layout="wide",
)

# 불필요한 장식을 모두 걷어낸 미니멀리즘 CSS (한국어 폰트 최적화)
st.markdown("""
    <style>
    /* 전체 배경을 완전한 검정색(#000000)으로 통일 */
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Noto Sans KR', sans-serif; }
    
    /* 미니멀 헤더 라인 */
    .title-container {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        padding-bottom: 8px;
        border-bottom: 1px solid #222222;
        margin-bottom: 30px;
    }
    .main-title { font-size: 1.4rem; font-weight: 500; letter-spacing: -0.5px; color: #FFFFFF; }
    .sub-title { color: #666666; font-size: 0.8rem; font-family: monospace; }
    
    /* 박스 테두리를 최소화한 미니멀 프레임 */
    .map-frame, .minimal-card {
        background-color: #000000;
        border: 1px solid #222222;
        border-radius: 0px; /* 라운드 제거로 더 날카롭고 미니멀하게 */
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* 검색 컨테이너 */
    .search-container {
        background-color: #000000;
        border: 1px solid #222222;
        border-radius: 0px;
        padding: 20px;
        margin-top: 20px;
    }
    
    /* 탭 메뉴 단순화 */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; background-color: #000000; }
    .stTabs [data-baseweb="tab"] { color: #555555; font-size: 0.9rem; font-weight: 500; }
    .stTabs [aria-selected="true"] { color: #FFFFFF !important; border-bottom-color: #FFFFFF !important; }
    
    /* 메트릭 라이브러리 커스텀 라인 */
    div[data-testid="stMetric"] {
        border-left: 1px solid #222222;
        padding-left: 15px;
    }
    </style>
""", unsafe_allow_html=True)


# --- 2. 데이터 로드 ---
@st.cache_data
def load_data():
    file_name = "covid_risk_analysis_result.csv"
    try:
        try: return pd.read_csv(file_name, encoding="utf-8")
        except: return pd.read_csv(file_name, encoding="cp949")
    except:
        return None

df_covid = load_data()

if df_covid is None:
    st.error("데이터 파일을 찾을 수 없습니다.")
    st.stop()


# --- 3. 미니멀리스트 컬러 매핑 ---
colors_map = {0: '#22C55E', 1: '#EAB308', 2: '#EF4444'} 
risk_dict = {0: '낮은 위험군', 1: '중간 위험군', 2: '높은 위험군'}


# --- 4. 미니멀 헤더 및 메트릭 현황 ---
st.markdown("""
    <div class='title-container'>
        <div class='main-title'>COVID-19 위험 분석 시스템</div>
        <div class='sub-title'>STATUS: LIVE // SYSTEM.ONLINE</div>
    </div>
""", unsafe_allow_html=True)

# 라인을 최소화한 원블랙 지표 판넬
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1: st.metric(label="글로벌 위험도 평균", value="LV. 1.84", delta="-0.02", delta_color="inverse")
with m_col2: st.metric(label="위중증 병상 가동률", value="42.3%", delta="-1.2%")
with m_col3: st.metric(label="백신 3차 접종률", value="78.9%", delta="+0.4%")
with m_col4: st.metric(label="주요 모니터링 변이", value="XBB / KP.3", delta="안정세")

st.markdown("<br>", unsafe_allow_html=True)

# 탭 구조 단순화
tab1, tab2, tab3 = st.tabs(["[01] 글로벌 지도 현황", "[02] 지정 구역 심층 분석", "[03] 방역 지침 안내"])


# --- 5. [탭 1] 글로벌 지도 현황 ---
with tab1:
    st.markdown("<div class='map-frame'>", unsafe_allow_html=True)
    
    # 지도의 디테일을 모두 숨긴 미니멀 다크 매터 테마
    m_global = folium.Map(location=[25, 20], zoom_start=2.2, tiles="CartoDB dark_matter")
    
    for i in range(len(df_covid)):
        cluster = int(df_covid.iloc[i]['cluster'])
        folium.CircleMarker(
            location=[df_covid.iloc[i]['위도'], df_covid.iloc[i]['경도']],
            radius=3.5, 
            color=colors_map[cluster],
            fill=True,
            fill_color=colors_map[cluster],
            fill_opacity=0.8,
            popup=f"{df_covid.iloc[i].get('국가_지역', '지역')} : {risk_dict[cluster]}"
        ).add_to(m_global)
    
    st_folium(m_global, width=1400, height=500, key="global_minimal_map")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 인덱스 범례 최소화 표시
    st.markdown(
        "<div style='text-align: right; font-size: 0.75rem; color: #666666; font-family: monospace;'> "
        "<span style='color:#EF4444;'>■</span> 고위험 &nbsp;&nbsp; "
        "<span style='color:#EAB308;'>■</span> 중간위험 &nbsp;&nbsp; "
        "<span style='color:#22C55E;'>■</span> 저위험"
        "</div>", 
        unsafe_allow_html=True
    )


# --- 6. 하단 미니멀 검색 컨트롤 바 ---
st.markdown("<div class='search-container'>", unsafe_allow_html=True)
st.markdown("<div style='font-size: 0.85rem; color: #666666; margin-bottom: 15px;'>// 역학조사 좌표 분석 검색 엔진</div>", unsafe_allow_html=True)

input_col1, input_col2, result_col = st.columns([1, 1, 2])

with input_col1:
    lat = st.number_input("위도 (LATITUDE)", value=10.8, format="%.4f")
with input_col2:
    lon = st.number_input("경도 (LONGITUDE)", value=106.6, format="%.4f")

near_df = df_covid[(df_covid['위도'] >= lat-5) & (df_covid['위도'] <= lat+5) & 
                   (df_covid['경도'] >= lon-5) & (df_covid['경도'] <= lon+5)]

with result_col:
    st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)
    if not near_df.empty:
        main_cluster = int(near_df['cluster'].value_counts().idxmax())
        st.markdown(
            f"<div style='border: 1px solid #222222; padding: 15px; font-size: 0.9rem;'>"
            f"분석 결과: 해당 반경은 <span style='color: {colors_map[main_cluster]}; font-weight: bold;'>[{risk_dict[main_cluster]}]</span> 우세 지역입니다."
            f"</div>", 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='border: 1px solid #222222; padding: 15px; font-size: 0.9rem; color: #666666;'>"
            f"분석 결과: 반경 내 수집 데이터 없음 (안전 혹은 미체크 지역)"
            f"</div>", 
            unsafe_allow_html=True
        )
st.markdown("</div>", unsafe_allow_html=True)


# --- 7. [탭 2] 지정 지역 집중 분석 지도 ---
with tab2:
    st.markdown("<div class='map-frame'>", unsafe_allow_html=True)
    m_local = folium.Map(location=[lat, lon], zoom_start=5, tiles="CartoDB dark_matter")
    
    for i in range(len(df_covid)):
        cluster = int(df_covid.iloc[i]['cluster'])
        folium.CircleMarker(
            location=[df_covid.iloc[i]['위도'], df_covid.iloc[i]['경도']],
            radius=3.5, 
            color=colors_map[cluster], 
            fill=True, 
            fill_color=colors_map[cluster],
            fill_opacity=0.35
        ).add_to(m_local)
        
    # 미니멀리즘 기본 마커
    folium.Marker(
        location=[lat, lon],
        popup="지정 분석 좌표"
    ).add_to(m_local)
    
    st_folium(m_local, width=1400, height=500, key="local_minimal_map")
    st.markdown("</div>", unsafe_allow_html=True)


# --- 8. [탭 3] 미니멀리스트 방역 수칙 & 비디오 (임베드 링크 수정 완료) ---
with tab3:
    col_video, col_text = st.columns([5, 6])
    
    with col_video:
        st.markdown("<div class='minimal-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.9rem; margin-bottom:15px; color:#FFFFFF;'>// 질병관리청 공식 예방 가이드</div>", unsafe_allow_html=True)
        
        # 보안 차단을 우회하기 위해 임베드 전용 주소(youtube.com/embed/...) 구문 사용
        st.video("https://www.youtube.com/embed/AunK7E2S58g")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_text:
        st.markdown("<div class='minimal-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.9rem; margin-bottom:15px; color:#FFFFFF;'>// WHO 감염병 예방 핵심 수칙</div>", unsafe_allow_html=True)
        
        # 선과 텍스트로만 이루어진 극도의 미니멀 레이아웃
        st.markdown("""
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; font-size: 0.85rem;'>
                <div style='border-top: 1px solid #333333; padding-top: 10px;'>
                    <span style='color: #666666;'>01. 올바른 손 씻기</span><br>
                    <span style='color: #FFFFFF;'>흐르는 물에 비누로 30초 이상 빈틈없이 씻기.</span>
                </div>
                <div style='border-top: 1px solid #333333; padding-top: 10px;'>
                    <span style='color: #666666;'>02. 주기적 환기</span><br>
                    <span style='color: #FFFFFF;'>밀폐된 실내 공간은 하루 3회 이상 자연 환기.</span>
                </div>
                <div style='border-top: 1px solid #333333; padding-top: 10px;'>
                    <span style='color: #666666;'>03. 기침 예절</span><br>
                    <span style='color: #FFFFFF;'>기침이나 재채기 시 옷소매 안쪽으로 입 가리기.</span>
                </div>
                <div style='border-top: 1px solid #333333; padding-top: 10px;'>
                    <span style='color: #666666;'>04. 마스크 착용</span><br>
                    <span style='color: #FFFFFF;'>밀집도가 높은 대중교통 및 의료기관 내 착용 권고.</span>
                </div>
            </div>
            <div style='margin-top: 35px; padding: 15px; border: 1px solid #333333; font-size: 0.8rem; color: #888888;'>
                ⚠️ 공지사항: 호흡기 이상 증상 발생 시, 일반 병의원 방문 전에 보건소 또는 1339 콜센터에 사전 문의를 권장합니다.
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)