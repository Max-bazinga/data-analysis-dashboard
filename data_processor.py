import pandas as pd

class DataProcessor:
    def __init__(self, file):
        self.file = file
    
    def load_and_clean(self):
        """加载并清洗数据"""
        df = pd.read_csv(self.file)
        
        # 处理缺失值
        df = df.dropna()
        
        # 数据类型转换
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    pass
        
        return df
    
    def generate_report(self, df):
        """生成数据分析报告"""
        report = {
            'row_count': len(df),
            'column_count': len(df.columns),
            'numeric_columns': df.select_dtypes(include=['number']).columns.tolist(),
            'missing_values': df.isnull().sum().sum()
        }
        return report
