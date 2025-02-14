import streamlit as st
import pandas as pd
from utils.data_refresh import get_last_update_time, should_refresh_data, update_timestamp, get_current_time
from datetime import datetime

def render_header():
    """渲染页面头部统计信息"""
    # 检查是否需要刷新数据
    if should_refresh_data() and 'bike_data' in st.session_state:
        # 更新时间戳
        update_timestamp()
        # 触发页面刷新，但仅在有bike_data时
        st.rerun()
    
    # 添加自定义CSS样式和JavaScript
    st.markdown("""
        <style>
        /* 隐藏所有Streamlit默认元素 */
        div[data-testid="stToolbar"] {
            display: none;
        }
        div[data-testid="stDecoration"] {
            display: none;
        }
        div[data-testid="stHeader"] {
            display: none;
        }
        section[data-testid="stSidebar"] {
            display: none;
        }
        
        /* 移除默认的padding和margin */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* 修改整体容器样式 */
        .header-container {
            width: 100%;
            max-width: 1600px;  /* 增加最大宽度 */
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        /* 修改标题容器样式 */
        .title-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            padding: 0;
            margin: 0.5rem 0;
        }
        
        /* 标题样式 */
        .dashboard-title {
            font-size: 1.8rem !important;
            font-weight: bold !important;
            color: #50c878 !important;
            margin: 0 !important;
            padding: 0 !important;
            font-family: 'Segoe UI', Arial, sans-serif !important;
            line-height: 1.2 !important;
        }

        /* 按钮样式 */
        .main-button {
            background-color: transparent !important;
            border: 1px solid #50c878 !important;
            color: #50c878 !important;
            font-size: 1rem !important;
            cursor: pointer !important;
            padding: 0.3rem 1rem !important;
            font-family: 'Segoe UI', Arial, sans-serif !important;
            transition: all 0.2s ease !important;
            border-radius: 4px !important;
            margin-left: auto;  /* 确保按钮靠右对齐 */
        }

        .main-button:hover {
            background-color: #50c878 !important;
            color: white !important;
        }
        
        /* 覆盖所有可能的padding-top */
        div.element-container {
            padding-top: 0 !important;
        }
        
        div.stMarkdown {
            padding-top: 0 !important;
        }
        
        .stApp > header {
            max-width: 1600px !important;
            margin: 0 auto !important;
        }
        
        .stApp {
            padding-top: 0 !important;
        }
        
        /* 其他样式保持不变 */
        .app-title {
            color: #2c3e50;
            font-size: 24px;
            font-weight: 500;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .nav-link {
            color: #666;
            text-decoration: none;
            font-size: 16px;
            font-weight: 400;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            transition: color 0.2s ease;
        }
        .nav-link:hover {
            color: #333;
        }
        /* 修改统计信息容器样式 */
        .stats-container {
            background-color: #f0f9f4;
            border-radius: 8px;
            padding: 0.5rem;
            margin: 0.5rem 0;
            width: 100%;
            max-width: 1600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);  /* 改为两列 */
            gap: 1rem;
            padding: 0.5rem;
        }
        
        .stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 1rem;
            background-color: white;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .stat-label {
            color: #666;
            font-size: 1rem;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        
        .stat-value {
            color: #50c878;  /* Bermuda绿色 */
            font-size: 1.8rem;
            font-weight: bold;
        }
        
        .stat-unit {
            font-size: 1rem;
            color: #666;
            margin-left: 2px;
        }

        .update-time {
            font-size: 0.8rem;
            color: #666;
            text-align: center;
            padding: 0.5rem;
        }
        
        /* 隐藏返回按钮 */
        button[kind="secondary"][data-testid="baseButton-secondary"] {
            display: none;
        }
        
        /* 调整页面内容的最大宽度 */
        .block-container {
            max-width: 1600px !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            margin: 0 auto !important;
        }
        
        /* 修改 Streamlit 按钮样式以匹配原有设计 */
        .stButton > button {
            background-color: transparent !important;
            border: 1px solid #50c878 !important;
            color: #50c878 !important;
            font-size: 1rem !important;
            cursor: pointer !important;
            padding: 0.3rem 1rem !important;
            font-family: 'Segoe UI', Arial, sans-serif !important;
            transition: all 0.2s ease !important;
            border-radius: 4px !important;
            float: right !important;
            margin-top: -40px !important;  /* 调整按钮位置 */
            margin-right: 1rem !important;
        }
        
        .stButton > button:hover {
            background-color: #50c878 !important;
            color: white !important;
        }
        
        /* 添加内容容器样式 */
        .content-container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 0 1rem;
            width: 100%;
            box-sizing: border-box;
        }
        
        /* 确保所有内容对齐 */
        .block-container {
            max-width: 1600px !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            margin: 0 auto !important;
        }
        
        /* 调整 Streamlit 默认容器样式 */
        .css-1d391kg, .css-12oz5g7 {
            max-width: 1600px !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            margin: 0 auto !important;
        }
        
        /* 确保地图和列表容器对齐 */
        .element-container {
            max-width: 1600px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        </style>
        
        <script>
        function redirectToMain() {
            window.location.href = 'http://localhost:8909/main';
        }
        </script>
    """, unsafe_allow_html=True)
    
    # 使用 container 来包装所有内容
    with st.container():
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        # 渲染标题
        st.markdown('''
            <div class="title-container">
                <h1 class="dashboard-title">Green Aurora Dashboard</h1>
            </div>
        ''', unsafe_allow_html=True)
        
        # 添加 Streamlit 按钮
        if st.button("메인으로"):
            st.markdown('<meta http-equiv="refresh" content="0;url=http://localhost:8909/main">', unsafe_allow_html=True)
        
        # 渲染统计信息
        bike_data = st.session_state.get('bike_data')
        if bike_data is not None:
            # 使用缓存的计算结果
            total_stations = st.session_state.get('total_stations', len(bike_data))
            current_available_bikes = st.session_state.get('current_available_bikes', 
                int(pd.to_numeric(bike_data['parkingBikeTotCnt'], errors='coerce').sum()))
            
            # 缓存计算结果
            if 'total_stations' not in st.session_state:
                st.session_state['total_stations'] = total_stations
            if 'current_available_bikes' not in st.session_state:
                st.session_state['current_available_bikes'] = current_available_bikes
            
            # 获取最新的更新时间
            last_update_time = get_last_update_time()
            
            st.markdown(f"""
                <div class="stats-container">
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-label">전체 대여소 수</div>
                            <div class="stat-value">{total_stations:,}<span class="stat-unit">개</span></div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">전체 이용 가능한 자전거</div>
                            <div class="stat-value">{current_available_bikes:,}<span class="stat-unit">대</span></div>
                        </div>
                    </div>
                    <div class="update-time">
                        마지막 업데이트: {last_update_time.strftime('%Y-%m-%d %H:%M:%S')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
