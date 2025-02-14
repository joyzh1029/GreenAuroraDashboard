import folium
import json
import os
import requests
import logging
import streamlit as st
from pathlib import Path
from utils.data_refresh import should_refresh_data

logger = logging.getLogger(__name__)

class MapService:
    def __init__(self):
        self.cache_dir = Path("cache")
        self.geojson_path = self.cache_dir / "seoul_municipalities.geojson"
        self.ensure_cache_dir()
        
    def ensure_cache_dir(self):
        """Ensure cache directory exists"""
        self.cache_dir.mkdir(exist_ok=True)
        
    def get_seoul_geojson(self):
        """Get Seoul GeoJSON data with fallback mechanisms"""
        try:
            # Try to load from cache first
            if self.geojson_path.exists():
                with open(self.geojson_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # If not in cache, download from GitHub
            url = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            geojson_data = response.json()
            
            # Cache the downloaded data
            with open(self.geojson_path, 'w', encoding='utf-8') as f:
                json.dump(geojson_data, f)
            
            return geojson_data
            
        except Exception as e:
            logger.error(f"Error loading Seoul GeoJSON data: {str(e)}")
            # Return simplified fallback GeoJSON if everything fails
            return self.get_fallback_geojson()
    
    def get_fallback_geojson(self):
        """Return a simplified GeoJSON with basic Seoul boundaries"""
        return {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[126.734086, 37.413294],
                                   [126.977041, 37.413294],
                                   [127.183797, 37.715133],
                                   [126.734086, 37.715133],
                                   [126.734086, 37.413294]]]
                },
                "properties": {"name": "Seoul"}
            }]
        }

def render_map():
    """渲染地图"""
    # 检查是否需要刷新数据
    if should_refresh_data():
        # 触发页面刷新
        st.rerun()
    
    try:
        map_service = MapService()
        
        # Create base map
        folium_map = folium.Map(
            location=[37.5665, 126.9780],
            zoom_start=11,
            width='100%',
            height='100%',
            control_scale=True
        )
        
        # Add GeoJSON layer with error handling
        try:
            geojson_data = map_service.get_seoul_geojson()
            folium.GeoJson(
                geojson_data,
                name='Seoul Districts',
                style_function=lambda x: {
                    'fillColor': '#ffedea',
                    'color': '#666666',
                    'weight': 1,
                    'fillOpacity': 0.3
                }
            ).add_to(folium_map)
        except Exception as e:
            logger.error(f"Error adding GeoJSON layer: {str(e)}")
            # Map will still be usable even without the GeoJSON layer
        
        return folium_map
        
    except Exception as e:
        logger.error(f"Error creating map: {str(e)}")
        # Return a basic map as fallback
        return folium.Map(
            location=[37.5665, 126.9780],
            zoom_start=11,
            width='100%',
            height='100%'
        )