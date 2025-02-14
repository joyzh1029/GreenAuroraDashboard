import streamlit as st
import pandas as pd

try:
    # 当作为包的一部分导入时
    from .data_service import get_bike_data
except ImportError:
    # 当直接运行文件时
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from components.data_service import get_bike_data

def render_metrics():
    # Get real-time bike data
    bike_data = get_bike_data()
    
    # Convert string columns to numeric
    bike_data['parkingBikeTotCnt'] = pd.to_numeric(bike_data['parkingBikeTotCnt'])
    bike_data['rackTotCnt'] = pd.to_numeric(bike_data['rackTotCnt'])
    
    def render_left_metrics(col):
        """메트릭 표시"""
        # 使用st.columns在一行中创建三个等宽列
        cols = st.columns(3)
        
        # 전체 대여소 수 (Total rental stations)
        with cols[0]:
            st.metric("전체 대여소 수", f"{len(bike_data):,d}개")
        
        # 현재 이용 가능한 자전거 (Currently available bikes)
        with cols[1]:
            total_bikes = int(bike_data['parkingBikeTotCnt'].sum())
            st.metric("현재 이용 가능한 자전거", f"{total_bikes:,d}대")
        
        # 전체 이용률 (Overall usage rate)
        with cols[2]:
            usage_rate = (bike_data['parkingBikeTotCnt'].sum() / bike_data['rackTotCnt'].sum() * 100).round(1)
            st.metric("전체 이용률", f"{usage_rate:.1f}%")
   
    return render_left_metrics

if __name__ == "__main__":
    metrics = render_metrics()
    metrics(st)