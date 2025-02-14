import streamlit as st
import functools
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def error_boundary(func):
    """错误边界装饰器，用于捕获和处理组件中的错误"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(f"Traceback:", exc_info=True)
            st.error(f"오류가 발생했습니다: {str(e)}")
            return None
    return wrapper 