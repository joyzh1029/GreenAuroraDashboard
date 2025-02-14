import pandas as pd
import requests
from datetime import datetime
import pytz
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BikeDataService:
    def __init__(self):
        """初始化数据服务"""
        self.api_key = "4a5148476d7a657238397858415851"
        self.base_url = "http://openapi.seoul.go.kr:8088"
        
    def get_bike_data(self):
        """서울시 공공자전거 실시간 대여정보 API 호출"""
        try:
            urls = [
                f"{self.base_url}/{self.api_key}/json/bikeList/1/1000",
                f"{self.base_url}/{self.api_key}/json/bikeList/1001/2000",
                f"{self.base_url}/{self.api_key}/json/bikeList/2001/3000"
            ]
            
            dfs = []
            for url in urls:
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    
                    data = response.json()
                    if 'rentBikeStatus' not in data:
                        logger.warning(f"Unexpected API response format: {data}")
                        continue
                        
                    df = pd.DataFrame(data['rentBikeStatus']['row'])
                    dfs.append(df)
                except Exception as e:
                    logger.error(f"Error fetching data from {url}: {str(e)}")
                    continue
            
            if not dfs:
                raise ValueError("No data retrieved from any API endpoint")
                
            final_df = pd.concat(dfs, ignore_index=True)
            self._clean_data(final_df)
            return final_df
            
        except Exception as e:
            logger.error(f"Error in get_bike_data: {str(e)}")
            return pd.DataFrame()
    
    def _clean_data(self, df):
        """清理和转换数据"""
        numeric_columns = ['parkingBikeTotCnt', 'rackTotCnt', 'shared']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df['stationLatitude'] = pd.to_numeric(df['stationLatitude'], errors='coerce')
        df['stationLongitude'] = pd.to_numeric(df['stationLongitude'], errors='coerce')
        
        return df
    
    def get_station_status(self):
        """获取站点状态统计"""
        try:
            df = self.get_bike_data()
            if df.empty:
                logger.warning("No bike data available")
                return self._get_empty_status()
            
            # 计算每个站点的剩余车架数
            df['remaining_racks'] = df['rackTotCnt'] - df['parkingBikeTotCnt']
            
            # 识别无法租赁和无法返还的站点
            no_rental_stations = df[df['parkingBikeTotCnt'] == 0]
            no_return_stations = df[df['remaining_racks'] == 0]
            
            # 获取当前韩国时间
            seoul_tz = pytz.timezone('Asia/Seoul')
            current_time = datetime.now(seoul_tz).strftime('%Y-%m-%d %H:%M:%S')
            
            result = {
                'no_rental': {
                    'count': len(no_rental_stations),
                    'stations': self._convert_stations(no_rental_stations)
                },
                'no_return': {
                    'count': len(no_return_stations),
                    'stations': self._convert_stations(no_return_stations)
                },
                'total_stations': len(df),
                'last_updated': current_time
            }
            
            logger.info(f"Station status updated: {result['total_stations']} total stations")
            return result
            
        except Exception as e:
            logger.error(f"Error processing station status: {str(e)}")
            return self._get_empty_status()
    
    def _convert_stations(self, stations_df):
        """转换站点数据为列表格式"""
        try:
            return [
                {
                    'id': row['stationId'],
                    'name': row['stationName'].strip(),
                    'parking': int(row['parkingBikeTotCnt']),    
                    'rack_count': int(row['rackTotCnt']),        
                    'remaining_racks': int(row['remaining_racks']),
                    'shared': int(row['shared']),
                    'lat': float(row['stationLatitude']),
                    'lng': float(row['stationLongitude'])
                }
                for _, row in stations_df.iterrows()
            ]
        except Exception as e:
            logger.error(f"Error converting station data: {str(e)}")
            return []
    
    def _get_empty_status(self):
        """返回空状态响应"""
        return {
            'no_rental': {'count': 0, 'stations': []},
            'no_return': {'count': 0, 'stations': []},
            'total_stations': 0,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def get_realtime_status(self):
        """获取实时状态"""
        return self.get_station_status()
        
    def get_status_metrics(self):
        """获取状态指标"""
        status = self.get_station_status()
        return {
            'total_stations': status['total_stations'],
            'no_rental_count': status['no_rental']['count'],
            'no_return_count': status['no_return']['count'],
            'last_updated': status['last_updated']
        }

# 创建单例实例
bike_service = BikeDataService()

# 导出便捷函数
def get_bike_data():
    return bike_service.get_bike_data()

def get_station_status():
    return bike_service.get_station_status() 