import streamlit as st
import plotly.express as px
import numpy as np
from config.settings import COLORS

# 차트 렌더링 함수들
def render_district_usage():
    with st.container(border=True, height=400):
        st.subheader("구별 이용 현황")
        districts = ['강남구', '서초구', '종로구', '마포구', '영등포구']
        values = [150, 130, 120, 100, 90]
        fig = px.bar(
            x=districts, 
            y=values,
            labels={'x': '구', 'y': '이용량'},
            template='none'
        )
        fig.update_traces(marker_color=COLORS["primary"])
        st.plotly_chart(fig, use_container_width=True)

def render_hourly_usage():
    with st.container(border=True, height=400):
        st.subheader("시간대별 이용 추이")
        hours = list(range(24))
        usage = np.random.normal(100, 20, 24)
        fig = px.line(
            x=hours, 
            y=usage,
            labels={'x': '시간', 'y': '이용량'},
            template='none'
        )
        fig.update_traces(line_color=COLORS["primary"])
        st.plotly_chart(fig, use_container_width=True)

def render_age_distribution():
    with st.container(border=True, height=300):
        st.subheader("연령대별 이용")
        age_groups = ['20대', '30대', '40대', '50대', '60대 이상']
        usage_by_age = [25, 30, 20, 15, 10]
        fig = px.bar(
            x=age_groups,
            y=usage_by_age,
            labels={'x': '연령대', 'y': '이용률'},
            template='none'
        )
        fig.update_traces(marker_color=COLORS["primary"])
        st.plotly_chart(fig, use_container_width=True)

def render_member_types():
    with st.container(border=True, height=300):
        st.subheader("회원 유형별 이용")
        fig = px.pie(
            values=[60, 40],
            names=['정기권', '일일권'],
            template='none'
        )
        fig.update_traces(marker=dict(colors=[COLORS["primary"], COLORS["secondary"]]))
        st.plotly_chart(fig, use_container_width=True)

def render_monthly_trend():
    with st.container(border=True, height=300):
        st.subheader("월별 이용 추이")
        months = ['1월', '2월', '3월', '4월', '5월', '6월']
        monthly_usage = [80, 85, 90, 95, 100, 110]
        fig = px.line(
            x=months,
            y=monthly_usage,
            labels={'x': '월', 'y': '이용량'},
            template='none'
        )
        fig.update_traces(line_color=COLORS["primary"])
        st.plotly_chart(fig, use_container_width=True) 