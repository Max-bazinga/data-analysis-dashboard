"""
Enhanced Data Analysis Dashboard
A professional data visualization tool for Toptal portfolio
Author: AI-Assisted Developer
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import Optional, List, Dict, Any
import io
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="专业数据分析仪表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stAlert {
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

class DataAnalyzer:
    """Professional data analysis class with comprehensive features"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Generate comprehensive summary statistics"""
        stats = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
            'missing_values': self.df.isnull().sum().sum(),
            'duplicate_rows': self.df.duplicated().sum()
        }
        return stats
    
    def correlation_matrix(self) -> Optional[pd.DataFrame]:
        """Calculate correlation matrix for numeric columns"""
        if len(self.numeric_cols) < 2:
            return None
        return self.df[self.numeric_cols].corr()
    
    def detect_outliers(self, column: str, method: str = 'iqr') -> pd.Series:
        """Detect outliers using IQR or Z-score method"""
        data = self.df[column].dropna()
        
        if method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return (data < lower_bound) | (data > upper_bound)
        
        elif method == 'zscore':
            z_scores = np.abs((data - data.mean()) / data.std())
            return z_scores > 3
        
        return pd.Series([False] * len(data), index=data.index)

def create_sample_dataset() -> pd.DataFrame:
    """Create a sample dataset for demonstration"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        '日期': pd.date_range('2024-01-01', periods=n_samples, freq='D'),
        '销售额': np.random.normal(1000, 200, n_samples),
        '客户数': np.random.poisson(50, n_samples),
        '转化率': np.random.beta(2, 5, n_samples),
        '地区': np.random.choice(['北京', '上海', '广州', '深圳'], n_samples),
        '产品类别': np.random.choice(['电子产品', '服装', '食品', '家居'], n_samples),
        '满意度评分': np.random.randint(1, 6, n_samples)
    }
    
    df = pd.DataFrame(data)
    df['转化率'] = df['转化率'].round(4)
    df['销售额'] = df['销售额'].clip(lower=0).round(2)
    return df

def render_sidebar() -> Optional[pd.DataFrame]:
    """Render sidebar with file upload and options"""
    with st.sidebar:
        st.header("📁 数据上传")
        
        # File upload
        uploaded_file = st.file_uploader(
            "上传 CSV 或 Excel 文件",
            type=['csv', 'xlsx', 'xls'],
            help="支持 CSV 和 Excel 格式"
        )
        
        # Sample data option
        use_sample = st.checkbox("使用示例数据集", value=False)
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                st.success(f"✅ 成功加载: {uploaded_file.name}")
                return df
            except Exception as e:
                st.error(f"❌ 加载失败: {str(e)}")
                return None
        
        elif use_sample:
            df = create_sample_dataset()
            st.info("📊 已加载示例销售数据")
            return df
        
        return None

def render_overview(df: pd.DataFrame, analyzer: DataAnalyzer):
    """Render data overview section"""
    st.header("📋 数据概览")
    
    # Summary metrics
    stats = analyzer.get_summary_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总行数", f"{stats['total_rows']:,}")
    with col2:
        st.metric("总列数", stats['total_columns'])
    with col3:
        st.metric("缺失值", stats['missing_values'])
    with col4:
        st.metric("重复行", stats['duplicate_rows'])
    
    # Data preview
    st.subheader("数据预览")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Column information
    st.subheader("字段信息")
    col_info = pd.DataFrame({
        '字段名': df.columns,
        '数据类型': df.dtypes.astype(str),
        '非空值数': df.count(),
        '唯一值数': df.nunique(),
        '缺失值数': df.isnull().sum()
    })
    st.dataframe(col_info, use_container_width=True)

def render_statistics(df: pd.DataFrame, analyzer: DataAnalyzer):
    """Render statistical analysis section"""
    st.header("📈 统计分析")
    
    if not analyzer.numeric_cols:
        st.warning("⚠️ 数据中没有数值型字段")
        return
    
    # Descriptive statistics
    st.subheader("描述性统计")
    desc_stats = df[analyzer.numeric_cols].describe()
    st.dataframe(desc_stats.round(4), use_container_width=True)
    
    # Correlation analysis
    if len(analyzer.numeric_cols) >= 2:
        st.subheader("相关性分析")
        corr_matrix = analyzer.correlation_matrix()
        
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="RdBu_r",
                title="相关性热力图"
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("强相关性（|r| > 0.7）:")
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:
                        strong_corr.append({
                            '字段1': corr_matrix.columns[i],
                            '字段2': corr_matrix.columns[j],
                            '相关系数': round(corr_val, 3)
                        })
            
            if strong_corr:
                st.dataframe(pd.DataFrame(strong_corr), use_container_width=True)
            else:
                st.info("未发现强相关性")

def render_visualization(df: pd.DataFrame, analyzer: DataAnalyzer):
    """Render data visualization section"""
    st.header("📊 数据可视化")
    
    # Chart type selection
    chart_type = st.selectbox(
        "选择图表类型",
        ["直方图", "散点图", "箱线图", "折线图", "柱状图", "饼图"]
    )
    
    if chart_type == "直方图":
        if analyzer.numeric_cols:
            col = st.selectbox("选择字段", analyzer.numeric_cols)
            bins = st.slider("分组数", 5, 100, 30)
            
            fig = px.histogram(
                df, x=col, nbins=bins,
                title=f"{col} 分布直方图",
                marginal="box"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("需要数值型字段")
    
    elif chart_type == "散点图":
        if len(analyzer.numeric_cols) >= 2:
            col1 = st.selectbox("X轴", analyzer.numeric_cols, index=0)
            col2 = st.selectbox("Y轴", analyzer.numeric_cols, index=1)
            
            color_col = None
            if analyzer.categorical_cols:
                color_col = st.selectbox(
                    "颜色分组（可选）",
                    ["无"] + analyzer.categorical_cols
                )
                if color_col == "无":
                    color_col = None
            
            fig = px.scatter(
                df, x=col1, y=col2, color=color_col,
                title=f"{col1} vs {col2} 散点图",
                opacity=0.6
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("需要至少2个数值型字段")
    
    elif chart_type == "箱线图":
        if analyzer.numeric_cols and analyzer.categorical_cols:
            num_col = st.selectbox("数值字段", analyzer.numeric_cols)
            cat_col = st.selectbox("分类字段", analyzer.categorical_cols)
            
            fig = px.box(
                df, x=cat_col, y=num_col,
                title=f"{num_col} 按 {cat_col} 分组的箱线图"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("需要数值型和分类型字段")
    
    elif chart_type == "折线图":
        if analyzer.numeric_cols:
            # Try to find a date column for x-axis
            x_col = st.selectbox("X轴", df.columns)
            y_cols = st.multiselect("Y轴（可多选）", analyzer.numeric_cols)
            
            if y_cols:
                fig = px.line(
                    df, x=x_col, y=y_cols,
                    title="趋势折线图"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("需要数值型字段")
    
    elif chart_type == "柱状图":
        if analyzer.categorical_cols:
            cat_col = st.selectbox("分类字段", analyzer.categorical_cols)
            agg_col = st.selectbox("聚合字段", analyzer.numeric_cols) if analyzer.numeric_cols else None
            agg_func = st.selectbox("聚合方式", ["计数", "求和", "平均值", "最大值", "最小值"])
            
            func_map = {"计数": "count", "求和": "sum", "平均值": "mean", 
                       "最大值": "max", "最小值": "min"}
            
            if agg_col and agg_func != "计数":
                grouped = df.groupby(cat_col)[agg_col].agg(func_map[agg_func]).reset_index()
                y_col = agg_col
            else:
                grouped = df[cat_col].value_counts().reset_index()
                grouped.columns = [cat_col, '计数']
                y_col = '计数'
            
            fig = px.bar(
                grouped, x=cat_col, y=y_col,
                title=f"{cat_col} 的 {agg_func} 柱状图"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "饼图":
        if analyzer.categorical_cols:
            cat_col = st.selectbox("分类字段", analyzer.categorical_cols)
            value_counts = df[cat_col].value_counts()
            
            # Limit to top 10 categories
            if len(value_counts) > 10:
                value_counts = value_counts.head(10)
                st.info("显示前10个类别")
            
            fig = px.pie(
                values=value_counts.values,
                names=value_counts.index,
                title=f"{cat_col} 分布饼图"
            )
            st.plotly_chart(fig, use_container_width=True)

def render_export(df: pd.DataFrame):
    """Render data export section"""
    st.header("💾 数据导出")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("导出为 CSV")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 下载 CSV",
            data=csv,
            file_name=f"processed_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv'
        )
    
    with col2:
        st.subheader("导出为 Excel")
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
        
        st.download_button(
            label="📥 下载 Excel",
            data=buffer.getvalue(),
            file_name=f"processed_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

def main():
    """Main application entry point"""
    # Header
    st.markdown('<p class="main-header">📊 专业数据分析仪表板</p>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar - File upload
    df = render_sidebar()
    
    if df is None:
        st.info("👆 请在左侧上传数据文件，或使用示例数据集")
        
        # Show feature highlights
        st.subheader("✨ 功能特性")
        features = [
            "📁 支持 CSV/Excel 文件上传",
            "📈 多种图表类型（直方图、散点图、箱线图等）",
            "🔍 数据统计与相关性分析",
            "🎨 交互式可视化",
            "💾 数据导出（CSV/Excel）",
            "📱 响应式设计"
        ]
        for feature in features:
            st.write(feature)
        return
    
    # Initialize analyzer
    try:
        analyzer = DataAnalyzer(df)
    except Exception as e:
        st.error(f"数据分析初始化失败: {str(e)}")
        return
    
    # Navigation tabs
    tabs = st.tabs([
        "📋 数据概览",
        "📈 统计分析",
        "📊 可视化",
        "💾 导出"
    ])
    
    with tabs[0]:
        render_overview(df, analyzer)
    
    with tabs[1]:
        render_statistics(df, analyzer)
    
    with tabs[2]:
        render_visualization(df, analyzer)
    
    with tabs[3]:
        render_export(df)
    
    # Footer
    st.markdown("---")
    st.caption(f"📅 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 🚀 Powered by Streamlit & Plotly")

if __name__ == "__main__":
    main()
