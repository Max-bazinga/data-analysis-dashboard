import pandas as pd
import plotly.express as px
import streamlit as st
from data_processor import DataProcessor

def main():
    st.title("数据分析仪表板")
    
    # 上传数据
    uploaded_file = st.file_uploader("上传CSV文件", type=['csv'])
    
    if uploaded_file is not None:
        # 数据处理
        processor = DataProcessor(uploaded_file)
        df = processor.load_and_clean()
        
        # 显示统计信息
        st.subheader("数据概览")
        st.write(df.describe())
        
        # 可视化
        st.subheader("数据可视化")
        fig = px.histogram(df, x=df.columns[0])
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
