import streamlit as st
from datetime import datetime, timedelta
import time

def should_refresh_data():
    """检查是否需要刷新数据"""
    current_time = datetime.now()
    
    # 获取或初始化上次更新时间
    if 'last_update_time' not in st.session_state:
        st.session_state['last_update_time'] = current_time
        return True
        
    last_update = st.session_state['last_update_time']
    
    # 如果距离上次更新已经超过5分钟，则需要更新
    if (current_time - last_update) >= timedelta(minutes=5):
        st.session_state['last_update_time'] = current_time
        return True
    return False

def update_timestamp():
    """更新时间戳"""
    st.session_state['last_update_time'] = datetime.now()

def get_current_time():
    """获取当前时间"""
    return datetime.now()

def get_last_update_time():
    """获取上次更新时间"""
    if 'last_update_time' not in st.session_state:
        st.session_state['last_update_time'] = datetime.now()
    return st.session_state['last_update_time']

def setup_auto_refresh():
    """设置自动刷新"""
    # 使用 Streamlit 的 rerun 触发自动刷新
    if should_refresh_data():
        time.sleep(1)  # 短暂延迟以避免过于频繁刷新
        st.rerun()
