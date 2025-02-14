import streamlit as st
import time
from datetime import datetime
from .error_boundary import error_boundary
from .bike_status import BikeStationStatus
from utils.data_refresh import should_refresh_data

try:
    # 当作为包的一部分导入时
    from .data_service import get_station_status
except ImportError:
    # 当直接运行文件时
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from components.data_service import get_station_status
    from components.error_boundary import error_boundary

class DynamicScrollView:
    def __init__(self):
        """初始化视图"""
        self.setup_styles()
        self.bike_status = BikeStationStatus()
        
    def setup_styles(self):
        """设置自定义样式"""
        st.markdown("""
            <style>
                .container {
                    padding: 12px;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    height: 440px;
                    overflow: hidden;
                    margin: 1rem 1rem 1rem 2rem;
                    width: calc(100% + 1rem);
                }
                .stats-column {
                    display: flex;
                    flex-direction: column;
                    height: 100%;
                }
                .section-box {
                    background-color: #f8f9fa;
                    border-radius: 6px;
                    padding: 10px;
                    display: flex;
                    flex-direction: column;
                    height: 100%;
                }
                .section-header {
                    margin-bottom: 6px;
                }
                .section-title {
                    font-size: 17px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 2px;
                    padding: 0 4px;
                    height: 28px;
                    display: flex;
                    align-items: center;
                }
                .section-subtitle {
                    font-size: 14px;
                    color: #34495e;
                    padding: 0 4px;
                    height: 20px;
                    display: flex;
                    align-items: center;
                }
                .station-list {
                    flex: 1;
                    overflow-y: auto;
                    background-color: white;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    padding: 5px;
                }
                
                .empty-message {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100%;
                    color: #666;
                    font-size: 0.9rem;
                    padding: 1rem;
                }
                
                .station-item {
                    padding: 4px 6px;
                    border-bottom: 1px solid #e9ecef;
                    font-size: 14px;
                    line-height: 1.5;
                    height: 28px;
                    display: flex;
                    align-items: center;
                    box-sizing: border-box;
                }
                .station-item:last-child {
                    border-bottom: none;
                }
                /* 自定义滚动条样式 */
                .station-list::-webkit-scrollbar {
                    width: 8px;
                }
                .station-list::-webkit-scrollbar-track {
                    background: var(--primary-50);
                    border-radius: 4px;
                }
                .station-list::-webkit-scrollbar-thumb {
                    background: var(--primary-200);
                    border-radius: 4px;
                }
                .station-list::-webkit-scrollbar-thumb:hover {
                    background: var(--primary-300);
                }

                /* 响应式布局 */
                @media screen and (max-width: 768px) {
                    .container {
                        margin: 0.75rem 0.75rem 0.75rem 1.5rem;
                        padding: 8px;
                    }
                    .section-title {
                        font-size: 16px;
                    }
                    .section-subtitle {
                        font-size: 13px;
                    }
                    .station-item {
                        font-size: 13px;
                        height: 26px;
                    }
                }

                @media screen and (max-width: 480px) {
                    .container {
                        margin: 0.5rem 0.5rem 0.5rem 1rem;
                        padding: 6px;
                    }
                    .section-title {
                        font-size: 15px;
                    }
                    .section-subtitle {
                        font-size: 12px;
                    }
                    .station-item {
                        font-size: 12px;
                        height: 24px;
                    }
                }
            </style>
        """, unsafe_allow_html=True)

    @error_boundary
    def render(self):
        """渲染动态滚动视图"""
        # 检查是否需要刷新数据
        if should_refresh_data():
            # 触发页面刷新
            st.rerun()
        data = self.bike_status.get_realtime_status()
        unavailable_rental = data['no_rental']['stations']
        
        st.markdown(f"""
            <div class="container">
                <div class="stats-column">
                    <div class="section-box">
                        <div class="section-header">
                            <div class="section-title">대여 불가 대여소</div>
                            <div class="section-subtitle">{len(unavailable_rental)} 개</div>
                        </div>
                        <div class="station-list">
                            {self._generate_station_list_html(unavailable_rental)}
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    def _generate_station_list_html(self, stations):
        """生成站点列表的HTML"""
        if not stations:
            return '<div class="empty-message">해당하는 대여소가 없습니다</div>'
            
        station_items = []
        for station in stations:
            station_items.append(
                f'<div class="station-item">{station["name"]}</div>'
            )
        return '\n'.join(station_items)

if __name__ == "__main__":
    from config.page_config import setup_page
    setup_page()
    view = DynamicScrollView()
    view.render() 