"""
数据科学专用工具集
支持数据分析、机器学习、数据可视化
"""

import os
import subprocess
from typing import List
from langchain_core.tools import Tool


class DataScienceTools:
    """数据科学工具"""
    
    @staticmethod
    def create_data_analysis_script(filepath_and_params: str) -> str:
        """
        创建数据分析脚本模板
        输入格式: "filepath|||data_file|||analysis_type"
        """
        try:
            parts = filepath_and_params.split("|||")
            if len(parts) != 3:
                return "错误：参数格式应为 'filepath|||data_file|||analysis_type'"
            
            filepath, data_file, analysis_type = parts[0].strip(), parts[1].strip(), parts[2].strip()
            
            template = f'''"""
数据分析脚本 - {analysis_type}
数据文件: {data_file}
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('{data_file}')

# 数据概览
print("数据形状:", df.shape)
print("\\n数据前5行:")
print(df.head())
print("\\n数据信息:")
print(df.info())
print("\\n数据统计:")
print(df.describe())

# 数据分析
# TODO: 根据{analysis_type}类型进行具体分析

# 保存结果
# df.to_csv('result.csv', index=False)
# plt.savefig('visualization.png')
'''
            
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(template)
            
            return f"✅ 成功创建数据分析脚本: {filepath}"
        
        except Exception as e:
            return f"创建数据分析脚本错误: {str(e)}"
    
    @staticmethod
    def create_ml_model(filepath_and_params: str) -> str:
        """
        创建机器学习模型模板
        输入格式: "filepath|||model_type|||target_column"
        """
        try:
            parts = filepath_and_params.split("|||")
            if len(parts) != 3:
                return "错误：参数格式应为 'filepath|||model_type|||target_column'"
            
            filepath, model_type, target = parts[0].strip(), parts[1].strip(), parts[2].strip()
            
            template = f'''"""
机器学习模型 - {model_type}
目标列: {target}
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# 读取数据
df = pd.read_csv('data.csv')

# 准备特征和目标
X = df.drop(columns=['{target}'])
y = df['{target}']

# 数据分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 特征缩放
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 创建模型
# TODO: 根据{model_type}选择模型
# from sklearn.linear_model import LogisticRegression
# model = LogisticRegression()

# 训练模型
# model.fit(X_train, y_train)

# 预测
# y_pred = model.predict(X_test)

# 评估
# print("准确率:", accuracy_score(y_test, y_pred))
# print("\\n分类报告:")
# print(classification_report(y_test, y_pred))
'''
            
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(template)
            
            return f"✅ 成功创建机器学习模型模板: {filepath}"
        
        except Exception as e:
            return f"创建机器学习模型错误: {str(e)}"
    
    @staticmethod
    def create_visualization(filepath_and_params: str) -> str:
        """
        创建数据可视化脚本
        输入格式: "filepath|||data_file|||chart_type"
        """
        try:
            parts = filepath_and_params.split("|||")
            if len(parts) != 3:
                return "错误：参数格式应为 'filepath|||data_file|||chart_type'"
            
            filepath, data_file, chart_type = parts[0].strip(), parts[1].strip(), parts[2].strip()
            
            template = f'''"""
数据可视化 - {chart_type}
数据文件: {data_file}
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('{data_file}')

# 创建图表
plt.figure(figsize=(10, 6))

# TODO: 根据{chart_type}类型创建对应图表
# if chart_type == 'line':
#     plt.plot(df['x'], df['y'])
# elif chart_type == 'bar':
#     plt.bar(df['x'], df['y'])
# elif chart_type == 'scatter':
#     plt.scatter(df['x'], df['y'])

plt.title('数据可视化')
plt.xlabel('X轴')
plt.ylabel('Y轴')
plt.tight_layout()

# 保存图表
plt.savefig('visualization.png', dpi=300, bbox_inches='tight')
plt.show()
'''
            
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(template)
            
            return f"✅ 成功创建可视化脚本: {filepath}"
        
        except Exception as e:
            return f"创建可视化脚本错误: {str(e)}"
    
    @staticmethod
    def install_data_science_packages(packages: str) -> str:
        """
        安装数据科学相关包
        输入: 包名（用逗号分隔）
        """
        try:
            package_list = [p.strip() for p in packages.split(',')]
            
            result = subprocess.run(
                ['pip', 'install'] + package_list,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=120
            )
            
            if result.returncode == 0:
                return f"✅ 成功安装包: {', '.join(package_list)}\n{result.stdout}"
            else:
                return f"❌ 安装失败: {result.stderr}"
        
        except Exception as e:
            return f"安装包错误: {str(e)}"


def create_data_science_tools() -> List[Tool]:
    """创建数据科学工具集"""
    tools = [
        Tool(
            name="create_data_analysis_script",
            func=DataScienceTools.create_data_analysis_script,
            description="创建数据分析脚本模板。输入格式：'文件路径|||数据文件|||分析类型'。Create data analysis script."
        ),
        Tool(
            name="create_ml_model",
            func=DataScienceTools.create_ml_model,
            description="创建机器学习模型模板。输入格式：'文件路径|||模型类型|||目标列'。Create ML model template."
        ),
        Tool(
            name="create_visualization",
            func=DataScienceTools.create_visualization,
            description="创建数据可视化脚本。输入格式：'文件路径|||数据文件|||图表类型'。Create visualization script."
        ),
        Tool(
            name="install_data_science_packages",
            func=DataScienceTools.install_data_science_packages,
            description="安装数据科学相关包。输入：包名（用逗号分隔，如 'pandas,numpy,matplotlib'）。Install data science packages."
        ),
    ]
    
    return tools


if __name__ == "__main__":
    # 测试工具
    print("=== 数据科学工具集测试 ===\n")
    
    print("1. 创建数据分析脚本:")
    print(DataScienceTools.create_data_analysis_script("test_analysis.py|||data.csv|||统计分析"))

