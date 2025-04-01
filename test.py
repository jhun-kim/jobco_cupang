import datetime

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
#import plotly.express as px
#from graphviz import Source
#import pdfkit
#import sqlite3
#from PIL import Image
from main import *
from cupang.main import *
from cupang.search_for_main import *

def test1():
    # 기업 데이터를 딕셔너리로 생성 (22개 기업 예시)
    # companies_data = {
    #     "기업명": ["기업 1", "기업 2", "기업 3", "기업 4", "기업 5", "기업 6", "기업 7", "기업 8", "기업 9", "기업 10",
    #             "기업 11", "기업 12", "기업 13", "기업 14", "기업 15", "기업 16", "기업 17", "기업 18", "기업 19", "기업 20",
    #             "기업 21", "기업 22"],
    #     "도달": [1200000, 890000, 2340000, 1900000, 1550000, 920000, 3500000, 2100000, 1700000, 1200000,
    #            2900000, 1600000, 1000000, 3100000, 1400000, 3200000, 2500000, 2700000, 3000000, 1300000,
    #            1400000, 1500000],
    #     "조회수": [150000, 80000, 240000, 190000, 155000, 92000, 350000, 210000, 170000, 120000,
    #             290000, 160000, 100000, 310000, 140000, 320000, 250000, 270000, 300000, 120000,
    #             140000, 150000],
    #     "지출금액": [500000, 400000, 600000, 550000, 500000, 420000, 700000, 620000, 570000, 530000,
    #              690000, 500000, 450000, 720000, 540000, 780000, 650000, 700000, 750000, 480000,
    #              520000, 540000]
    # }
    #
    # # 데이터프레임 생성
    # df = pd.DataFrame(companies_data)
    file = r'C:\Users\LeadersTrading\Documents\카카오톡 받은 파일\company_distribution_integer.csv'
    df = pd.read_csv(file, encoding='UTF-8')

    # Streamlit 앱 타이틀
    st.title("기업별 퍼포먼스 데이터")

    # 22개의 기업 정보를 카드 형식으로 출력
    for index, row in df.iterrows():
        st.markdown("---")  # 구분선
        st.subheader(f"{row['Company']}")
        col1, col2, col3 = st.columns(3)  # 3개의 열을 나란히 표시

        # 첫 번째 열: 도달 수
        with col1:
            st.metric(label="도달", value=f"{row['Views']:,}")

        # 두 번째 열: 조회수
        with col2:
            st.metric(label="조회 수", value=f"{row['Hits']:,}")

        # 세 번째 열: 지출 금액
        with col3:
            st.metric(label="리액션 수", value=f"{row['Likes']:,}")

def test_2():
    # Streamlit 페이지 제목 설정
    st.title("Seaborn과 Matplotlib을 활용한 데이터 시각화")

    # 샘플 데이터셋 로드 (seaborn 내장 데이터셋 사용)
    data = sns.load_dataset("penguins")

    # Seaborn을 이용하여 scatter plot 생성
    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x="flipper_length_mm", y="body_mass_g", hue="species", ax=ax)

    # Streamlit에 그래프 표시
    st.pyplot(fig)

def test_3():
    # 페이지 수에 맞춰 슬라이드 내용을 사전으로 정의
    slides = {
        1: "Slide 1: Introduction\n\nWelcome to the presentation!",
        2: "Slide 2: Overview\n\nHere's an overview of what we're going to cover.",
        3: "Slide 3: Details\n\nDetailed information goes here.",
        4: "Slide 4: Conclusion\n\nThank you for watching!"
    }

    # 세션 상태로 슬라이드 번호 관리 (초기값: 1)
    if "slide_number" not in st.session_state:
        st.session_state.slide_number = 1

    # 슬라이드 내용 출력
    st.markdown(f"### {slides[st.session_state.slide_number]}")

    # 이전 슬라이드 버튼
    if st.session_state.slide_number > 1:
        if st.button("Previous"):
            st.session_state.slide_number -= 1

    # 다음 슬라이드 버튼
    if st.session_state.slide_number < len(slides):
        if st.button("Next"):
            st.session_state.slide_number += 1

    # 슬라이드 번호 표시
    st.write(f"Slide {st.session_state.slide_number} of {len(slides)}")

#슬라이드 및 다중 페이지 대시보드 템플릿
def test_4():
    # 사이드바로 페이지 선택
    st.sidebar.title("Presentation Navigation")
    page = st.sidebar.radio("Go to", ["jobco", "cupang_goldenbox", "cupang_details"])

    # 페이지 내용 구성
    if page == "jobco":
        st.title("jobco")
        st.write("Welcome to the presentation!")
        if st.button("jobco"):
            print_hi('PyCharm')

    elif page == "cupang_goldenbox":
        st.title("cupang_goldenbox")
        st.write("Here's an overview of what we're going to cover.")
        if st.button("cupang_goldenbox"):
            cu_print_hi('PyCharm')

    elif page == "cupang_details":
        st.title("cupang_details")
        st.write("Here is the detailed information.")
        # with st.form("order_form"):
        user_name = st.text_input("검색명", placeholder="검색명")
        if st.button("cupang_details"):
            cu_main(user_name)

    elif page == "Conclusion":
        st.title("Conclusion")
        st.write("Thank you for watching!")

#모던한 카드 레이아웃
def test_5():
    # 3개의 칼럼으로 카드 스타일 구성
    st.title("Modern Dashboard")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Metric 1")
        st.metric(label="Sales", value="70k", delta="-5%")
        st.write("Monthly sales performance.")

    with col2:
        st.header("Metric 2")
        st.metric(label="Revenue", value="$100k", delta="8%")
        st.write("Monthly revenue growth.")

    with col3:
        st.header("Metric 3")
        st.metric(label="Customer Satisfaction", value="95%", delta="2%")
        st.write("Customer feedback summary.")


#탭을 이용한 인터페이스
def test_6():
    st.title("Report Dashboard")

    tab1, tab2, tab3 = st.tabs(["Summary", "Detailed Analysis", "Conclusions"])

    with tab1:
        st.header("Executive Summary")
        st.write("Summary content goes here.")

    with tab2:
        st.header("Detailed Analysis")
        st.write("Detailed analysis content goes here.")
        st.line_chart([1, 2, 3, 4, 5])  # 예제 차트 추가

    with tab3:
        st.header("Conclusions")
        st.write("Conclusion content goes here.")


#CSS로 텍스트 스타일링 및 배경색 추가
def test_7():
    st.markdown("""
        <style>
        .card {
            background-color: #f8f9fa;
            padding: 20px;
            margin: 10px;
            border-radius: 5px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        }
        .card h3 {
            color: #007bff;
        }
        </style>
        """, unsafe_allow_html=True)

    # 카드 레이아웃을 적용하여 섹션을 구성
    st.markdown('<div class="card"><h3>Section 1</h3><p>Content for section 1 goes here.</p></div>',
                unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>Section 2</h3><p>Content for section 2 goes here.</p></div>',
                unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>Section 3</h3><p>Content for section 3 goes here.</p></div>',
                unsafe_allow_html=True)

#커스텀 폰트 및 컬러 스키마 추가
def test_8():
    st.markdown("""
        <style>
        body {
            font-family: 'Arial', sans-serif;
            color: #333;
            background-color: #e9ecef;
        }
        .highlight {
            font-size: 24px;
            color: #FF5733;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="highlight">This is a highlighted text section.</div>', unsafe_allow_html=True)

#드롭다운 메뉴와 상호작용 기반 인터페이스
def test_9():
    st.title("Interactive Dashboard")

    # 드롭다운을 이용한 선택 메뉴
    option = st.selectbox("Select a Data Category", ("Sales", "Marketing", "Customer Feedback"))

    if option == "Sales":
        st.write("Sales data visualization goes here.")
    elif option == "Marketing":
        st.write("Marketing data visualization goes here.")
    elif option == "Customer Feedback":
        st.write("Customer feedback analysis goes here.")

    # 체크박스 기반 추가 옵션
    if st.checkbox("Show Advanced Metrics"):
        st.write("Advanced metrics are displayed here.")

#데이터 테이블과 차트를 활용한 분석 섹션
def test_10():
    # 더미 데이터 생성
    data = pd.DataFrame(np.random.randn(10, 5), columns=("A", "B", "C", "D", "E"))

    # 컬럼 배치
    col1, col2 = st.columns(2)

    with col1:
        st.write("Data Table")
        st.dataframe(data)

    with col2:
        st.write("Chart")
        st.bar_chart(data)


def test_df():


    file = "['강서구', '양천구', '영등포구', '마포구', '용산구']_python_잡코리아.csv"
    df = pd.read_csv(file, encoding='cp949')

    today = str(datetime.datetime.today()).split(' ')[0]
    df = df[df['마감일'] >= today].reset_index(drop=True)
    df = df.sort_values(['마감일'], ascending=True).reset_index(drop=True)

    df.to_csv(f'new_{file}', encoding='cp949')


def test():
    plt.figurl(figsize=(10, 4))
    sns.histplot(date['거래금액'], kde=True)
    plt.tilte()
    plt.xlabel()
    plt.ylabel()
    plt.show()

def test_11():
    # 데이터 생성
    # 데이터 생성
    # Streamlit 레이아웃 설정: 전체 화면 사용
    st.set_page_config(layout="wide", page_title="판매 데이터 분석 대시보드", page_icon="📊")

    # 데이터 생성
    @st.cache_data
    def load_data():
        np.random.seed(42)
        data = pd.DataFrame({
            'Country': np.random.choice(['USA', 'Canada', 'Germany', 'France', 'Japan'], 100),
            'Product': np.random.choice(['Product A', 'Product B', 'Product C'], 100),
            'Sales': np.random.randint(100, 1000, 100),
            'Date': pd.date_range(start='2023-01-01', periods=100)
        })
        return data

    # 데이터 로드
    df = load_data()

    # 피벗 테이블 생성
    pivot_table = df.pivot_table(index='Country', columns='Product', values='Sales', aggfunc='sum', fill_value=0)
    pivot_table = pivot_table.reset_index()

    # 제목
    st.title("📊 나라별 판매 데이터 분석")

    # 피벗 테이블 표시 (화면을 더 활용)
    st.subheader("📋 피벗 테이블")
    st.dataframe(pivot_table, height=500, width=2600)  # 높이 증가

    # 사이드바를 이용한 선택
    st.sidebar.header("🔍 필터 설정")
    selected_country = st.sidebar.selectbox("나라를 선택하세요", options=pivot_table['Country'])
    selected_product = st.sidebar.selectbox("제품을 선택하세요", options=pivot_table.columns[1:])

    # 필터링된 데이터
    filtered_data = df[(df['Country'] == selected_country) & (df['Product'] == selected_product)]

    if filtered_data.empty:
        st.warning(f"{selected_country}의 {selected_product} 데이터가 없습니다.")
    else:
        # 시각화 제목
        st.subheader(f"{selected_country} - {selected_product} 시각화")

        # 4분할 그래프를 위한 레이아웃
        col1, col2 = st.columns(2, gap="large")  # 너비 간격 조정

        # 그래프 생성
        fig1 = px.bar(filtered_data, x='Date', y='Sales',
                      title=f"Bar Chart of {selected_product} Sales in {selected_country}")
        fig2 = px.line(filtered_data, x='Date', y='Sales',
                       title=f"Line Chart of {selected_product} Sales in {selected_country}")
        fig3 = px.scatter(filtered_data, x='Date', y='Sales',
                          title=f"Scatter Plot of {selected_product} Sales in {selected_country}")
        fig4 = px.histogram(filtered_data, x='Sales', nbins=10,
                            title=f"Histogram of {selected_product} Sales in {selected_country}")

        # 왼쪽 열
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
            st.plotly_chart(fig3, use_container_width=True)

        # 오른쪽 열
        with col2:
            st.plotly_chart(fig2, use_container_width=True)
            st.plotly_chart(fig4, use_container_width=True)

def test_12():
    # Streamlit 레이아웃 설정: 전체 화면 사용
    st.set_page_config(layout="wide", page_title="동적 시각화 대시보드", page_icon="📊")

    # 데이터 생성
    @st.cache_data
    def load_data():
        np.random.seed(42)
        data = pd.DataFrame({
            'Country': np.random.choice(['USA', 'Canada', 'Germany', 'France', 'Japan'], 100),
            'Product': np.random.choice(['Product A', 'Product B', 'Product C'], 100),
            'Sales': np.random.randint(100, 1000, 100),
            'Quantity': np.random.randint(1, 50, 100),
            'Profit': np.random.uniform(10, 500, 100).round(2),
            'Date': pd.date_range(start='2023-01-01', periods=100)
        })
        return data

    # 데이터 로드
    df = load_data()

    # 제목
    st.title("📊 동적 시각화 대시보드")

    # 피벗 테이블 생성
    pivot_table = df.pivot_table(index='Country', columns='Product', values='Sales', aggfunc='sum', fill_value=0)
    pivot_table = pivot_table.reset_index()

    # 피벗 테이블 표시
    st.subheader("📋 데이터프레임 (컬럼값으로 시각화 설정)")
    st.dataframe(pivot_table, height=300)

    # 시각화 축 설정: 컬럼 선택
    st.sidebar.header("🔍 시각화 설정")
    x_axis = st.sidebar.selectbox("X축 컬럼 선택", options=df.columns, index=0)
    y_axis = st.sidebar.selectbox("Y축 컬럼 선택", options=df.columns, index=2)
    color_axis = st.sidebar.selectbox("컬러 기준 선택 (옵션)", options=[None] + list(df.columns), index=0)

    # 시각화 타입 선택
    chart_type = st.sidebar.radio("시각화 타입 선택", options=['Bar Chart', 'Line Chart', 'Scatter Plot'])

    # 선택한 옵션으로 시각화
    st.subheader(f"📈 {chart_type}: {x_axis} vs {y_axis}")
    if not df.empty:
        if chart_type == 'Bar Chart':
            fig = px.bar(df, x=x_axis, y=y_axis, color=color_axis, title=f"Bar Chart of {x_axis} vs {y_axis}")
        elif chart_type == 'Line Chart':
            fig = px.line(df, x=x_axis, y=y_axis, color=color_axis, title=f"Line Chart of {x_axis} vs {y_axis}")
        elif chart_type == 'Scatter Plot':
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color_axis, title=f"Scatter Plot of {x_axis} vs {y_axis}")

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("데이터가 없습니다.")

    # 추가: 선택한 컬럼별 통계 요약
    st.subheader(f"📊 {x_axis} & {y_axis} 통계 요약")
    summary = df[[x_axis, y_axis]].describe()
    st.dataframe(summary)

def test13():
    st.set_page_config(page_title="Compact KAM-PD Workflow", layout="wide")

    # Title
    st.title("Compact KAM-PD Workflow")

    # Compact Workflow Diagram
    diagram_code = """
    digraph G {
        rankdir=TB;  // Top-to-Bottom layout
        node [shape=box, style="rounded, filled", color=lightblue, fontname="Arial"];

        KAM_Input [label="1. 데이터 입력 (KAM)"];
        KAM_Upload [label="2. 업로드 (KAM → DB)"];
        PD_Refresh [label="3. 리프레시 (PD → DB)"];
        PD_Review [label="4. 검토 (CONFIRM/RE-CHECK/COMMENT)"];
        PD_SendFeedback [label="5. SEND_FEEDBACK (PD → DB)"];
        DB_Resent [label="6. RE-CHECK 데이터 수정 (DB → KAM)"];
        PD_ResentCheck [label="7. RE-SENT 확인 (PD)"];
        PD_CreateTemplate [label="8. 템플릿 생성 (PD → DB)"];
        PD_SPMSID [label="9. SPMS ID 저장 (PD → DB)"];
        KAM_SPMSKey [label="10. SPMS KEY 확인 (KAM)"];

        // Workflow connections
        KAM_Input -> KAM_Upload;
        KAM_Upload -> PD_Refresh;
        PD_Refresh -> PD_Review;
        PD_Review -> PD_SendFeedback;
        PD_SendFeedback -> PD_ResentCheck;
        PD_ResentCheck -> DB_Resent;
        DB_Resent -> KAM_Input [label="수정 데이터 업로드"];
        PD_Review -> PD_CreateTemplate;
        PD_CreateTemplate -> PD_SPMSID;
        PD_SPMSID -> KAM_SPMSKey;
    }
    """

    st.graphviz_chart(diagram_code)

    st.write("""
    ### 워크플로우 단계 설명
    1. **KAM 데이터 입력**: 데이터를 입력하고 업로드합니다.
    2. **DB 저장**: KAM 프로그램에서 업로드한 데이터를 DB에 저장합니다.
    3. **PD 리프레시**: PD 프로그램에서 DB 데이터를 불러옵니다.
    4. **검토 및 피드백**: PD에서 데이터를 CONFIRM, RE-CHECK, COMMENT로 처리합니다.
    5. **RE-CHECK 데이터 수정**: KAM 프로그램에서 RE-CHECK 데이터를 수정하고 업로드합니다.
    6. **RE-SENT 확인**: PD 프로그램에서 수정된 데이터를 확인합니다.
    7. **템플릿 생성**: PD에서 템플릿을 생성합니다.
    8. **SPMS ID 저장**: SPMS KEY를 입력하고 저장합니다.
    9. **SPMS KEY 확인**: KAM 프로그램에서 SPMS KEY를 확인합니다.
    """)


def test14():
    # wkhtmltopdf 경로를 지정
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    st.set_page_config(page_title="Enhanced KAM-PD Workflow", layout="wide")

    # Title
    st.title("Enhanced KAM-PD Workflow")

    # Enhanced Workflow Diagram
    diagram_code = """
    digraph G {
        rankdir=TB; // Top-to-Bottom layout
        node [fontname="Arial", shape=box, style="rounded, filled"];

        // Define colors for KAM and PD
        KAM [color="#AEDFF7"]; // Light Blue for KAM
        PD [color="#FFE5A0"]; // Light Orange for PD
        DB [shape=cylinder, style="filled", color="#D3C4F3"]; // Cylinder shape for DB

        // Nodes
        KAM_Input [label="1. 데이터 입력 (KAM)", fillcolor="#AEDFF7"];
        KAM_Upload [label="2. 업로드 (KAM → DB)", fillcolor="#AEDFF7"];
        DB_Main [label="DB", shape=cylinder, style=filled, fillcolor="#D3C4F3"];
        PD_Refresh [label="3. 리프레시 (PD → DB)", fillcolor="#FFE5A0"];
        PD_Review [label="4. 검토 (CONFIRM/RE-CHECK/COMMENT)", fillcolor="#FFE5A0"];
        PD_SendFeedback [label="5. SEND_FEEDBACK (PD → DB)", fillcolor="#FFE5A0"];
        DB_Resent [label="6. RE-CHECK 데이터 수정 (DB → KAM)", fillcolor="#D3C4F3"];
        PD_ResentCheck [label="7. RE-SENT 확인 (PD)", fillcolor="#FFE5A0"];
        PD_CreateTemplate [label="8. 템플릿 생성 (PD → DB)", fillcolor="#FFE5A0"];
        PD_SPMSID [label="9. SPMS ID 저장 (PD → DB)", fillcolor="#FFE5A0"];
        KAM_SPMSKey [label="10. SPMS KEY 확인 (KAM)", fillcolor="#AEDFF7"];

        // Workflow connections
        KAM_Input -> KAM_Upload;
        KAM_Upload -> DB_Main;
        DB_Main -> PD_Refresh;
        PD_Refresh -> PD_Review;
        PD_Review -> PD_SendFeedback;
        PD_SendFeedback -> DB_Main [label="피드백 반영"];
        DB_Main -> DB_Resent;
        DB_Resent -> KAM_Input [label="수정 데이터 업로드"];
        PD_Review -> PD_CreateTemplate;
        PD_CreateTemplate -> PD_SPMSID;
        PD_SPMSID -> KAM_SPMSKey;

        // Align DB nodes to the center
        {rank=same; DB_Main; PD_CreateTemplate; PD_SPMSID;}
    }
    """

    # Render graph
    st.graphviz_chart(diagram_code)

    # Explanation
    st.write("""
    ### 개선된 워크플로우 설명
    - **KAM 단계**: KAM 관련 단계는 파란색 배경으로 강조되었습니다.
    - **PD 단계**: PD 관련 단계는 주황색 배경으로 구분됩니다.
    - **DB 관련 단계**: DB 관련 노드는 원통형 모양으로 표시되며, 보라색으로 강조되었습니다.
    - **구조 균형**: 상단에서 하단으로 자연스럽게 흐르는 레이아웃으로, 각 단계를 직관적으로 확인할 수 있습니다.
    """)

    # 설명 텍스트
    explanation = """
    <h3>개선된 워크플로우 설명</h3>
    <ul>
        <li><strong>KAM 단계</strong>: KAM 관련 단계는 파란색 배경으로 강조되었습니다.</li>
        <li><strong>PD 단계</strong>: PD 관련 단계는 주황색 배경으로 구분됩니다.</li>
        <li><strong>DB 관련 단계</strong>: DB 관련 노드는 원통형 모양으로 표시되며, 보라색으로 강조되었습니다.</li>
        <li><strong>구조 균형</strong>: 상단에서 하단으로 자연스럽게 흐르는 레이아웃으로, 각 단계를 직관적으로 확인할 수 있습니다.</li>
    </ul>
    """

    # HTML로 렌더링
    st.write(explanation, unsafe_allow_html=True)

    # Graphviz 다이어그램을 파일로 저장
    src = Source(diagram_code)
    diagram_path = "diagram.png"
    src.render(diagram_path, format="png", cleanup=True)

    # Streamlit 화면에 다이어그램 표시
    st.image(f"{diagram_path}.png", caption="Enhanced Workflow Diagram")

    # HTML 내용 정의
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ text-align: center; color: #333; }}
            .explanation {{ margin: 20px; line-height: 1.5; }}
        </style>
    </head>
    <body>
        <h1>Enhanced KAM-PD Workflow</h1>
        <img src="{diagram_path}.png" alt="Workflow Diagram" style="display: block; margin: auto;">
        <div class="explanation">
            <h3>개선된 워크플로우 설명</h3>
            <ul>
                <li><strong>KAM 단계</strong>: KAM 관련 단계는 파란색 배경으로 강조되었습니다.</li>
                <li><strong>PD 단계</strong>: PD 관련 단계는 주황색 배경으로 구분됩니다.</li>
                <li><strong>DB 관련 단계</strong>: DB 관련 노드는 원통형 모양으로 표시되며, 보라색으로 강조되었습니다.</li>
                <li><strong>구조 균형</strong>: 상단에서 하단으로 자연스럽게 흐르는 레이아웃으로, 각 단계를 직관적으로 확인할 수 있습니다.</li>
            </ul>
        </div>
    </body>
    </html>
    """

    # PDF 생성 버튼
    if st.button("PDF로 내보내기"):
        pdf_file_path = "Enhanced_KAM_PD_Workflow.pdf"
        options = {
            'enable-local-file-access': '',  # 로컬 파일 접근 활성화
        }
        pdfkit.from_string(html_content, pdf_file_path, configuration=pdfkit.configuration(
            wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'), options=options)
        st.success(f"PDF 생성 완료: {pdf_file_path}")

def test15():




    # 제목
    st.title("엑셀 데이터를 데이터베이스에 저장하기")

    # 엑셀 파일 업로드
    uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx", "xls"])

    if uploaded_file:
        try:
            # 엑셀 데이터 읽기
            df = pd.read_excel(uploaded_file)
            st.write("업로드된 데이터:")
            st.dataframe(df)

            # 데이터 저장 버튼
            if st.button("데이터 DB에 저장"):

                st.success("엑셀 데이터가 데이터베이스에 저장되었습니다.")
        except Exception as e:
            st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")

    # 데이터베이스에서 저장된 데이터 보기
    if st.checkbox("저장된 데이터 보기"):
        st.write("데이터베이스에 저장된 데이터:")

        st.dataframe(saved_data)

def test16():

    # 초기 데이터
    initial_data = {
        "이름": ["홍길동", "김철수", "이영희"],
        "나이": [25, 30, 35],
        "직업": ["학생", "개발자", "디자이너"]
    }
    df = pd.DataFrame(initial_data)

    # 제목
    st.title("사용자 입력 데이터를 데이터베이스로 저장하기")

    # 사용자 입력 가능 표 제공
    st.write("아래 표에 데이터를 입력하거나 수정하세요:")
    edited_df = st.data_editor(df, key="editable_table")


    # 저장 버튼
    if st.button("데이터 DB에 저장"):

        st.success("데이터가 데이터베이스에 저장되었습니다.")

    # 데이터베이스에서 저장된 데이터 확인
    if st.checkbox("저장된 데이터 보기"):
        st.write("데이터베이스에서 불러온 데이터:")

        st.dataframe(edited_df)

    # 종료 시 데이터베이스 연결 닫기
    if st.button("앱 종료"):
        st.stop()

def test17():
    # 초기 데이터프레임 설정
    if "df" not in st.session_state:
        # 기본적으로 20개 컬럼을 가진 데이터프레임 생성
        columns = [f"Column{i}" for i in range(1, 21)]
        st.session_state.df = pd.DataFrame(columns=columns)

    st.title("행 추가 및 데이터프레임 직접 입력")

    # 데이터프레임 편집 및 행 추가
    st.write("### 데이터프레임 수정")
    edited_df = st.data_editor(
        st.session_state.df,
        key="editable_table",
        use_container_width=True
    )

    # 데이터프레임 상태 업데이트
    st.session_state.df = edited_df

    # 플러스 버튼으로 행 추가
    if st.button("➕ 행 추가"):
        # 새로운 빈 행 추가
        new_row = {col: "" for col in st.session_state.df.columns}
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
        # st.experimental_rerun()

    # 데이터 저장 버튼
    if st.button("데이터 저장"):
        st.success("데이터가 저장되었습니다!")
        # 여기에서 데이터를 DB로 저장하는 로직을 추가 가능

    # 업데이트된 데이터프레임 표시
    st.write("### 업데이트된 데이터프레임")
    st.dataframe(st.session_state.df, use_container_width=True)


def test18():
    # Initialize database
    DB_FILE = "coffee_cause.db"

    def init_db():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                coffee_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                donation_percent REAL NOT NULL,
                donation_amount REAL NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def add_donation(user_name, coffee_type, quantity, donation_percent, donation_amount):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO donations (user_name, coffee_type, quantity, donation_percent, donation_amount)
            VALUES (?, ?, ?, ?, ?)
        """, (user_name, coffee_type, quantity, donation_percent, donation_amount))
        conn.commit()
        conn.close()

    def fetch_donations():
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query("SELECT * FROM donations ORDER BY date DESC", conn)
        conn.close()
        return df

    # Initialize database
    init_db()

    # Streamlit App Configuration
    st.set_page_config(
        page_title="Coffee for a Cause",
        page_icon="☕",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio(
        "Choose a page:",
        ("Home", "Order Coffee", "Donation Status", "Stories", "Settings")
    )

    # Home Page
    if menu == "Home":
        st.image("coffee_logo.png", use_container_width=True)  # Replace with your banner image
        st.title("☕ Coffee for a Cause")
        st.write("Welcome to 'Coffee for a Cause'! Make a difference with every cup of coffee.")
        st.markdown("""
            ### Why Choose Us?
            - **Transparency**: See how your contributions are making an impact.
            - **Community Stories**: Get inspired by stories of change.
            - **Simple & Convenient**: Donate seamlessly while enjoying your favorite coffee.
        """)
        st.button("Order Now", key="order_now", on_click=lambda: st.sidebar.radio("Choose a page:", ("Order Coffee")))

    # Order Coffee Page
    elif menu == "Order Coffee":
        st.title("📋 Order Coffee & Donate")
        with st.form("order_form"):
            user_name = st.text_input("Your Name", placeholder="Enter your name")
            coffee_type = st.selectbox("Choose Coffee Type", ["Espresso", "Latte", "Cappuccino", "Americano"])
            quantity = st.number_input("Quantity", min_value=1, step=1)
            donation_percent = st.slider("Donation Percentage", min_value=5, max_value=50, value=10)
            base_price = 5.0  # Assume a fixed base price per cup
            donation_amount = round(base_price * quantity * donation_percent / 100, 2)
            st.metric("Donation Amount", f"${donation_amount:.2f}")
            submitted = st.form_submit_button("Submit Order")
            if submitted:
                add_donation(user_name, coffee_type, quantity, donation_percent, donation_amount)
                st.success(
                    f"Thank you {user_name}! Your order has been placed and ${donation_amount:.2f} will be donated.")

    # Donation Status Page
    elif menu == "Donation Status":
        st.title("📊 Donation Status")
        donations = fetch_donations()
        if not donations.empty:
            total_donations = donations["donation_amount"].sum()
            total_cups = donations["quantity"].sum()
            st.metric("Total Donations Collected", f"${total_donations:.2f}")
            st.metric("Total Cups Sold", total_cups)
            st.line_chart(donations.groupby(donations["date"].str[:10])["donation_amount"].sum())
            st.dataframe(donations)
        else:
            st.info("No donations yet. Be the first to make a difference!")

    # Stories Page
    elif menu == "Stories":
        st.title("📖 Impact Stories")
        st.write("Read stories about how your contributions are changing lives.")
        st.markdown("""
            #### Maria's Story
            After receiving support, Maria was able to start her own small business. Your donations make stories like this possible!
        """)
        st.image("coffee_logo.png", use_container_width=True)  # Replace with a sample story image

    # Settings Page
    elif menu == "Settings":
        st.title("⚙️ Settings")
        st.write("Manage your preferences:")
        st.text_input("Name", placeholder="Update your name")
        st.text_input("Email", placeholder="Update your email")
        st.selectbox("Preferred Donation Region", ["Local", "National", "Global"])
        theme = st.radio("App Theme", ["Light", "Dark", "Warm"])
        st.success("Settings updated successfully!")

    # Footer
    st.markdown("""
        <footer style="text-align: center; padding: 10px 0; font-size: 0.85rem; color: #777;">
            Made with ❤️ by Coffee Enthusiasts | Transparency. Impact. Love.
        </footer>
    """, unsafe_allow_html=True)

def test19():
    file = r"C:\Users\LeadersTrading\Desktop\잡코\2025-03-13_AI_추천_잡코리아.csv"
    df = pd.read_csv(file, encoding='cp949')
    print(df)


test_4()
