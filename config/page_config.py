import streamlit as st

def setup_page():
    """设置页面基本配置"""
    st.set_page_config(
        page_title="Green Aurora Dashboard",
        page_icon="static/images/bicycle-icon.png",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # 设置全局样式
    st.markdown("""
        <style>
            .main {
                max-width: 1920px;
                padding: 1rem;
                background-color: white;
            }
            
            /* 隐藏Streamlit默认元素 */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True) 