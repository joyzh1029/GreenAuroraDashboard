import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import requests
from folium.plugins import MarkerCluster
from .error_boundary import error_boundary
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

try:
    # When imported as a package
    from .station_panel import StationPanel
    from .data_service import BikeDataService
    from .map import MapService
except ImportError:
    # When run directly
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from components.station_panel import StationPanel
    from components.data_service import BikeDataService
    from components.map import MapService

# 지도 설정
MAP_CONFIG = {
    "seoul_center": [37.5665, 126.9780],
    "zoom_level": 11,
    "tile_style": 'OpenStreetMap'
}

# 配置 requests 的重试策略
retry_strategy = Retry(
    total=3,  # 最多重试3次
    backoff_factor=1,  # 重试间隔
    status_forcelist=[500, 502, 503, 504]  # 需要重试的HTTP状态码
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

def get_bike_data():
    """서울시 공공자전거 실시간 대여정보 API 호출"""
    service = BikeDataService()
    return service.get_bike_data()

def render_metrics(bike_data):
    """Display bike usage metrics"""
    if not bike_data.empty:
        try:
            total_stations = len(bike_data)
            # 确保转换为数值类型
            total_bikes = pd.to_numeric(bike_data['parkingBikeTotCnt'], errors='coerce').sum()
            total_racks = pd.to_numeric(bike_data['rackTotCnt'], errors='coerce').sum()
            usage_rate = (total_bikes / total_racks * 100) if total_racks > 0 else 0
            
            # Create metrics container with custom styling
            metrics_html = f"""
                <div class="metrics-container">
                    <div class="metric-box">
                        <div class="metric-value">{total_stations:,}</div>
                        <div class="metric-label">총 대여소</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{int(total_bikes):,}</div>
                        <div class="metric-label">이용 가능한 자전거</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{int(total_racks):,}</div>
                        <div class="metric-label">총 거치대</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{usage_rate:.1f}%</div>
                        <div class="metric-label">이용률</div>
                    </div>
                </div>
            """
            st.markdown(metrics_html, unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"통계 데이터를 계산하는 중 오류가 발생했습니다: {str(e)}")

@error_boundary
def get_geojson_data():
    """안전하게 GeoJSON 데이터를 가져옵니다"""
    try:
        map_service = MapService()
        return map_service.get_seoul_geojson()
    except Exception as e:
        st.error(f"지도 데이터를 불러올 수 없습니다: {str(e)}")
        return None

@error_boundary
def render_seoul_map():
    st.markdown("""
        <style>
            /* 地图容器样式 */
            [data-testid="column"] > div:has(> iframe) {
                height: 440px !important;  /* 保持一致的高度 */
                margin: 2.5rem 0.5rem 1rem 3rem !important;
                padding: 0 !important;
                width: calc(100% - 1.2rem) !important;
                position: relative;
            }
            
            /* iframe样式 */
            iframe {
                height: 440px !important;  /* 保持一致的高度 */
                width: 100% !important;
                border-radius: 8px !important;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            
            /* 移除地图周围的任何额外空间 */
            .element-container:has(> iframe) {
                margin: 2.5rem 0.5rem 1rem 3rem !important;
                padding: 0 !important;
                width: calc(100% - 1.2rem) !important;
                overflow: visible !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # 使用单个容器而不是嵌套列
    with st.container():
        try:
            # 首尔市的大致边界坐标 - 扩大边界范围
            SEOUL_BOUNDS = {
                'sw': [37.325, 126.664],  # 扩大西南角范围
                'ne': [37.801, 127.283]   # 扩大东北角范围
            }
            
            # 创建地图，设置限制范围
            m = folium.Map(
                location=MAP_CONFIG["seoul_center"],
                zoom_start=10.5,
                tiles='OpenStreetMap',
                control_scale=True,
                width='100%',
                height='440px',  # 增加回440px
                min_zoom=9.5,
                max_zoom=15,
                zoom_control=True,
                scrollWheelZoom=True,
                dragging=True
            )
            
            # 设置地图的最大边界并调整缩放级别
            m.fit_bounds([SEOUL_BOUNDS['sw'], SEOUL_BOUNDS['ne']], padding=[50, 50])  # 添加边界padding
            
            # 确保地图始终保持在首尔边界内
            m.options['maxBounds'] = [
                [SEOUL_BOUNDS['sw'][0] - 0.1, SEOUL_BOUNDS['sw'][1] - 0.1],  # 进一步扩大边界
                [SEOUL_BOUNDS['ne'][0] + 0.1, SEOUL_BOUNDS['ne'][1] + 0.1]
            ]
            m.options['minZoom'] = 9.5  # 微调最小缩放级别
            m.options['maxZoom'] = 15  # 限制最大缩放级别
            m.options['bounceAtZoomLimits'] = True  # 在缩放限制处反弹
            
            # 获取 GeoJSON 数据
            geo_data = get_geojson_data()
            if geo_data:
                # 添加首尔整体边界（外部边界）
                folium.GeoJson(
                    geo_data,
                    style_function=lambda x: {
                        'fillColor': 'transparent',
                        'color': '#128970',  # 使用 bermuda-600 的深色
                        'weight': 3,         # 较粗的线条
                        'opacity': 0.9
                    }
                ).add_to(m)
                
                # 添加内部行政区划（内部边界）
                folium.GeoJson(
                    geo_data,
                    style_function=lambda x: {
                        'fillColor': 'transparent',
                        'color': '#20a98a',  # 使用 bermuda-500 的颜色
                        'weight': 1,         # 较细的线条
                        'dashArray': '5, 5', # 虚线样式
                        'opacity': 0.7       # 稍微增加不透明度
                    }
                ).add_to(m)
            
            # 获取自行车数据
            bike_data = st.session_state.get('bike_data')
            
            if bike_data is not None and not bike_data.empty:
                # 调整聚类设置
                marker_cluster = MarkerCluster(
                    options={
                        'maxClusterRadius': 50,
                        'disableClusteringAtZoom': 14,
                        'spiderfyOnMaxZoom': True,
                        'maxZoom': 15  # 限制聚类的最大缩放级别
                    }
                ).add_to(m)
                
                for _, row in bike_data.iterrows():
                    try:
                        bikes = int(row['parkingBikeTotCnt'])
                        lat = float(row['stationLatitude'])
                        lon = float(row['stationLongitude'])
                        
                        # 根据自行车数量设置颜色和大小
                        if bikes > 20:
                            color = '#2ecc71'    # 多 (绿色)
                            radius = 6           # 大圆点
                        elif bikes > 10:
                            color = '#f1c40f'    # 中 (黄色)
                            radius = 5           # 中圆点
                        else:
                            color = '#e74c3c'    # 少 (红色)
                            radius = 4           # 小圆点
                        
                        folium.CircleMarker(
                            location=[lat, lon],
                            radius=radius,
                            color=color,
                            fill=True,
                            popup=folium.Popup(
                                f"""<div style='font-family: "Noto Sans KR", sans-serif; 
                                                      text-align: center;
                                                      padding: 5px;'>
                                    <b>{row['stationName']}</b><br>
                                    대여 가능한 자전거: <b>{bikes}대</b>
                                </div>""",
                                max_width=200
                            ),
                            fill_opacity=0.7,
                            weight=1
                        ).add_to(marker_cluster)
                    except (ValueError, KeyError) as e:
                        continue  # 跳过有问题的数据点
                
                # 添加图例
                legend_html = '''
                <div style="position: fixed; 
                            bottom: 50px; right: 50px; 
                            border-radius: 8px;
                            background-color: rgba(255, 255, 255, 0.95);
                            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                            padding: 12px 15px;
                            font-family: 'Noto Sans KR', sans-serif;
                            font-size: 13px;
                            color: #2c3e50;
                            z-index: 9999;">
                    <p style="margin: 0 0 8px 0;"><strong>자전거 대여 현황</strong></p>
                    <p style="margin: 4px 0;">● <span style="color: #2ecc71;">20대 이상</span></p>
                    <p style="margin: 4px 0;">● <span style="color: #f1c40f;">10-20대</span></p>
                    <p style="margin: 4px 0;">● <span style="color: #e74c3c;">10대 미만</span></p>
                </div>
                '''
                m.get_root().html.add_child(folium.Element(legend_html))
            
            # 在上方添加一些空间
            st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
            folium_static(m, width=1000, height=440)  # 增加回440px
            
        except Exception as e:
            st.error(f"地图渲染错误: {str(e)}")
            st.info("请刷新页面重试")

def main():
    # 获取自行车数据
    bike_data = get_bike_data()
    
    # 创建共享的 StationPanel 实例
    station_panel = StationPanel()
    station_panel.update_data(bike_data)
    
    # 将自行车数据和站点面板存储在会话状态中
    st.session_state['bike_data'] = bike_data
    st.session_state['station_panel'] = station_panel
    
    # 渲染首尔地图
    render_seoul_map()

    # 渲染站点面板
    station_panel.render()

if __name__ == "__main__":
    st.set_page_config(page_title="Seoul Bike Map", layout="wide")
    main()
