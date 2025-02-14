from datetime import datetime
import pytz
from .data_service import get_bike_data

class BikeStationStatus:
    def get_realtime_status(self):
        """获取实时的自行车站状态数据"""
        try:
            # 从 data_service 获取数据
            bike_data = get_bike_data()
            
            if bike_data.empty:
                print("No stations data received")
                return self._get_empty_response()
            
            print(f"Total stations received: {len(bike_data)}")
            
            # 将车站分为两类：无法租赁(没有可用车辆)和无法返还(车架已满)
            no_rental_stations = []  # 无法租赁的站点（没有可用车辆）
            no_return_stations = []  # 无法返还的站点（车架已满）
            
            for _, station in bike_data.iterrows():
                try:
                    parking = int(station['parkingBikeTotCnt'])  # 当前可用车辆数
                    rack_total = int(station['rackTotCnt'])      # 总车架数
                    shared = int(station['shared'])              # 使用率
                    
                    station_info = {
                        'id': station['stationId'],
                        'name': station['stationName'].strip(),
                        'parking': parking,
                        'rack_count': rack_total,
                        'shared': shared
                    }
                    
                    # 如果没有可用车辆，归类为无法租赁
                    if parking == 0:
                        no_rental_stations.append(station_info)
                    # 只有当总车架数为0时，才归类为无法返还
                    if rack_total == 0:
                        no_return_stations.append(station_info)
                        
                except (ValueError, KeyError) as e:
                    print(f"Error processing station {station.get('stationName', 'Unknown')}: {e}")
                    continue
            
            # 获取当前韩国时间
            seoul_tz = pytz.timezone('Asia/Seoul')
            current_time = datetime.now(seoul_tz).strftime('%Y-%m-%d %H:%M:%S')
            
            # 按站点ID排序（处理带有 'ST-' 前缀的ID）
            def get_station_number(station):
                try:
                    # 移除 'ST-' 前缀并转换为整数
                    return int(station['id'].replace('ST-', ''))
                except (ValueError, AttributeError):
                    return 0  # 如果转换失败，返回0
            
            no_rental_stations.sort(key=get_station_number)
            no_return_stations.sort(key=get_station_number)
            
            result = {
                'no_rental': {
                    'count': len(no_rental_stations),
                    'stations': no_rental_stations
                },
                'no_return': {
                    'count': len(no_return_stations),
                    'stations': no_return_stations
                },
                'last_updated': current_time,
                'total_stations': len(bike_data)
            }
            
            print(f"Processing complete: Found {len(no_rental_stations)} no-rental and {len(no_return_stations)} no-return stations")
            return result
            
        except Exception as e:
            print(f"Error processing bike station status: {str(e)}")
            import traceback
            print("Traceback:", traceback.format_exc())
            return self._get_empty_response()

    def _get_empty_response(self):
        """返回空响应"""
        return {
            'no_rental': {'count': 0, 'stations': []},
            'no_return': {'count': 0, 'stations': []},
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_stations': 0
        }

    def format_station_display(self):
        """
        格式化站点显示信息
        
        Returns:
            str: 格式化后的显示文本
        """
        data = self.get_realtime_status()
        if not data:
            return "데이터를 가져올 수 없습니다"
            
        output = f"""
{data['no_rental']['count']}개
대여 불가 대여소

"""
        # 添加无法租赁的车站列表
        for station in data['no_rental']['stations']:
            output += f"{station['id']}. {station['name']}\n"
            
        output += f"""
{data['no_return']['count']}개
반환 불가 대여소

"""
        # 添加无法返还的车站列表
        for station in data['no_return']['stations']:
            output += f"{station['id']}. {station['name']}\n"
            
        output += f"\n마지막 업데이트: {data['last_updated']} (5분마다 자동 업데이트)"
        
        return output

    def get_status_metrics(self):
        """
        获取状态指标
        
        Returns:
            dict: 包含各类指标的字典
        """
        data = self.get_realtime_status()
        if not data:
            return None
            
        return {
            'total_stations': data['total_stations'],
            'no_rental_stations': data['no_rental']['count'],
            'no_return_stations': data['no_return']['count'],
            'last_updated': data['last_updated']
        } 