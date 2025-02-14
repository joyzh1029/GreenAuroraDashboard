import streamlit as st
from components.maps import render_seoul_map
from components.header import render_header
from components.station_panel import StationPanel
from components.dynamic_scroll_view import DynamicScrollView
from components.data_service import bike_service
from config.page_config import setup_page
from utils.data_refresh import setup_auto_refresh, should_refresh_data

# 确保这是第一个被执行的命令
setup_page()

def load_styles():
    """加载样式文件"""
    with open('static/styles/main.css', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def init_session_state():
    """初始化session state"""
    if 'bike_data' not in st.session_state:
        st.session_state['bike_data'] = None
    if 'station_panel' not in st.session_state:
        st.session_state['station_panel'] = StationPanel()
    if 'is_loading' not in st.session_state:
        st.session_state['is_loading'] = False

def render_layout():
    """渲染页面布局"""
    # 添加主容器
    with st.container():
        # 添加页面顶部边距
        st.markdown("""
            <style>
                /* 添加页面顶部边距 */
                section.main {
                    padding-top: 4rem !important;
                }
                
                .main-content {
                    max-width: 1600px;
                    margin: 0 auto;
                    padding: 0;
                }
                .columns-container {
                    margin-top: 1rem;
                    display: flex;
                }
                /* 确保列容器与header对齐 */
                [data-testid="column"] {
                    padding-left: 0 !important;
                    padding-right: 0 !important;
                }
                /* 调整列间距 */
                [data-testid="column"]:not(:first-child) {
                    margin-left: 1rem !important;
                }
                
                /* 调整整体容器的边距 */
                .block-container {
                    padding-top: 2rem !important;
                    margin-top: 1rem !important;
                }
            </style>
            <div class="main-content">
        """, unsafe_allow_html=True)
        
        # 1. 首先渲染 header
        render_header()

        # 2. 显示加载状态
        if st.session_state.get('is_loading', False):
            st.markdown("""
                <div class="loading-message">
                    데이터를 업데이트 중입니다...
                </div>
            """, unsafe_allow_html=True)

        # 3. 创建内容容器，移除左右padding以确保对齐
        st.markdown("""
            <style>
                .main-content {
                    max-width: 1600px;
                    margin: 0 auto;
                    padding: 0;  /* 移除padding */
                }
                .columns-container {
                    margin-top: 1rem;
                    display: flex;
                }
                /* 确保列容器与header对齐 */
                [data-testid="column"] {
                    padding-left: 0 !important;
                    padding-right: 0 !important;
                }
                /* 调整列间距 */
                [data-testid="column"]:not(:first-child) {
                    margin-left: 1rem !important;
                }
            </style>
            <div class="main-content">
        """, unsafe_allow_html=True)
        
        # 4. 创建三列布局，使用small间距
        col1, col2, col3 = st.columns([2.5, 4.5, 3], gap="small")
        
        # 5. 在列中渲染各个组件
        with col1:
            DynamicScrollView().render()
            
        with col2:
            render_seoul_map()
            
        with col3:
            st.session_state['station_panel'].render()

        st.markdown('</div>', unsafe_allow_html=True)

def update_data():
    """更新数据"""
    if should_refresh_data():
        st.session_state['is_loading'] = True
        try:
            bike_data = bike_service.get_bike_data()
            if not bike_data.empty:
                st.session_state['bike_data'] = bike_data
                st.session_state['station_panel'].update_data(bike_data)
        except Exception as e:
            st.error(f"데이터 업데이트 중 오류 발생: {str(e)}")
        finally:
            st.session_state['is_loading'] = False

def main():
    load_styles()
    init_session_state()
    
    try:
        # 设置自动刷新
        setup_auto_refresh()
        
        # 更新数据
        update_data()
        
        # 如果没有数据，尝试首次加载
        if st.session_state['bike_data'] is None:
            bike_data = bike_service.get_bike_data()
            if bike_data.empty:
                st.warning("데이터를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.")
                return
            st.session_state['bike_data'] = bike_data
            st.session_state['station_panel'].update_data(bike_data)
            
        render_layout()
        
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
        print(f"Error in app: {str(e)}")

if __name__ == "__main__":
    main()
