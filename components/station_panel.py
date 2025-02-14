import streamlit as st
from utils.data_refresh import should_refresh_data
import pandas as pd

class StationPanel:
    def __init__(self):
        self.bike_data = None
        
    def update_data(self, bike_data):
        """Update the bike data"""
        self.bike_data = bike_data
        
    def render(self):
        """Render the station panel"""
        # 检查是否需要刷新数据
        if should_refresh_data():
            # 触发页面刷新
            st.rerun()
        
        st.markdown("""
            <style>
                /* 主容器样式 */
                .station-panel {
                    margin-left: 1rem;
                    border-radius: 12px;                    
                    padding: 0.5rem !important;  /* 减小内边距 */
                    overflow: hidden !important;
                    
                }

                /* 移除表格上方的空白 */
                div[data-testid="stVerticalBlock"] > div {
                    padding-top: 0 !important;
                    padding-bottom: 0 !important;
                    margin-top: 0 !important;
                    margin-bottom: 0 !important;
                }

                /* 移除 DataFrame 容器的多余空白 */
                div[data-testid="stDataFrameResizable"] {
                    padding: 0 !important;
                    margin: 0 !important;
                }

                /* 调整表格容器样式 */
                .element-container {
                    margin: 0 !important;
                    padding: 0 !important;
                }

                /* 确保列容器没有额外的空白 */
                [data-testid="column"] {
                    padding: 0 !important;
                    margin: 0 !important;
                }

                .station-panel-content {
                    height: 100% !important;
                    display: flex !important;
                    flex-direction: column !important;
                    padding: 0 !important;
                    margin: 0 !important;
                }

                /* 表格容器样式 */
                .station-table {
                    flex: 1 !important;
                    overflow: auto !important;
                    padding: 0 !important;
                    margin: 0 !important;
                    border-radius: 4px !important;
                }
                
                /* 调整表格单元格样式 */
                div[data-testid="stDataFrameResizable"] td, 
                div[data-testid="stDataFrameResizable"] th {
                    padding: 4px 8px !important;
                    font-size: 10px !important;
                    border: 1px solid #e0e0e0 !important;
                }

                /* 调整表格行高 */
                div[data-testid="stDataFrameResizable"] tr {
                    height: 24px !important;
                }
                
                /* 表格头部样式 */
                div[data-testid="stDataFrameResizable"] th {
                    font-size: 11px !important;
                    font-weight: 600 !important;
                    background-color: #f8f9fa !important;
                    border-bottom: 2px solid rgba(0, 0, 0, 0.1) !important;
                    padding: 8px !important;
                    height: 32px !important;
                    white-space: nowrap !important;
                }
                
                /* 调整表格滚动区域样式 */
                .stDataFrameResizable > div:first-child {
                    overflow: auto !important;
                    border-radius: 12px !important;
                }

                /* 隐藏全屏按钮 */
                div[data-testid="stDataFrameResizable"] [data-testid="StyledFullScreenButton"] {
                    display: none !important;
                }
                
                /* 设置表格编辑器变量 */
                .stDataFrameGlideDataEditor {
                    --gdg-header-font-style: normal !important;
                    --gdg-base-font-style: normal !important;
                    --gdg-font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
                }

                /* 响应式布局 */
                @media screen and (max-width: 768px) {
                    .station-panel {
                        height: calc(100vh - 240px) !important;
                    }
                    
                    div[data-testid="stDataFrameResizable"] td {
                        padding: 3px 6px !important;
                        font-size: 11px !important;
                    }
                    
                    div[data-testid="stDataFrameResizable"] th {
                        font-size: 12px !important;
                        padding: 6px !important;
                        height: 28px !important;
                    }
                }

                @media screen and (max-width: 480px) {
                    .station-panel {
                        height: calc(100vh - 200px) !important;
                    }
                    
                    div[data-testid="stDataFrameResizable"] td {
                        padding: 2px 4px !important;
                        font-size: 10px !important;
                    }
                    
                    div[data-testid="stDataFrameResizable"] th {
                        font-size: 11px !important;
                        padding: 4px !important;
                        height: 24px !important;
                    }
                }

                /* 调整表格列宽 */
                div[data-testid="stDataFrameResizable"] table {
                    table-layout: fixed !important;
                }
                
                /* 设置第一列宽度 */
                div[data-testid="stDataFrameResizable"] td:first-child,
                div[data-testid="stDataFrameResizable"] th:first-child {
                    width: 200px !important;
                    max-width: 200px !important;
                }
                
                /* 设置数字列宽度 */
                div[data-testid="stDataFrameResizable"] td:not(:first-child),
                div[data-testid="stDataFrameResizable"] th:not(:first-child) {
                    width: 100px !important;
                    max-width: 100px !important;
                    text-align: center !important;
                }

                /* 确保单元格内容不换行 */
                div[data-testid="stDataFrameResizable"] td,
                div[data-testid="stDataFrameResizable"] th {
                    white-space: nowrap !important;
                    overflow: hidden !important;
                    text-overflow: ellipsis !important;
                }
            </style>
        """, unsafe_allow_html=True)

        # 创建主容器，移除额外的 padding
        with st.container():
            st.markdown('<div class="station-panel">', unsafe_allow_html=True)
            
            # 直接显示数据，不使用额外的列包装
            if self.bike_data is None or self.bike_data.empty:
                st.markdown("""
                    <div class="station-panel-content">
                        <div style="text-align: center; padding: 20px;">
                            데이터를 불러올 수 없습니다.
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                try:
                    # 直接显示数据，移除搜索相关代码
                    filtered_data = self.bike_data
                    
                    # 重命名列并选择要显示的列
                    filtered_data = filtered_data.rename(columns={
                        'stationName': '대여소명',
                        'parkingBikeTotCnt': '대여 가능 대수',
                        'rackTotCnt': '총 거치대 수'
                    })[['대여소명', '대여 가능 대수', '총 거치대 수']]
                    
                    # 确保数值列为数值类型
                    filtered_data['대여 가능 대수'] = pd.to_numeric(filtered_data['대여 가능 대수'], errors='coerce')
                    filtered_data['총 거치대 수'] = pd.to_numeric(filtered_data['총 거치대 수'], errors='coerce')

                    # 使用st.dataframe显示数据，移除额外的样式包装
                    st.dataframe(
                        filtered_data,
                        hide_index=True,
                        use_container_width=True,
                        height=None,
                        column_config={
                            "대여소명": st.column_config.TextColumn(
                                "대여소명",
                                width=200,  # 设置固定宽度
                            ),
                            "대여 가능 대수": st.column_config.NumberColumn(
                                "대여 가능 대수",
                                width=100,  # 减小宽度
                            ),
                            "총 거치대 수": st.column_config.NumberColumn(
                                "총 거치대 수",
                                width=100,  # 减小宽度
                            )
                        }
                    )
                except Exception as e:
                    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Station Panel Demo", layout="wide")
    
    # 测试数据
    test_data = pd.DataFrame({
        'stationName': ['Station 1', 'Station 2'],
        'parkingBikeTotCnt': [10, 20],
        'rackTotCnt': [15, 25],
        'shared': [30, 40]
    })
    
    panel = StationPanel()
    panel.update_data(test_data)
    panel.render()
