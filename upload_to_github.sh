#!/bin/bash
# GitHub 上传脚本 - 数据分析项目

echo "🚀 开始上传项目到 GitHub..."
echo ""

# 配置信息
PROJECT_NAME="data-analysis-dashboard"
GITHUB_USERNAME="YOUR_GITHUB_USERNAME"  # 修改为你的GitHub用户名

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}步骤 1: 初始化 Git 仓库${NC}"
git init

echo ""
echo -e "${BLUE}步骤 2: 添加所有文件${NC}"
git add .

echo ""
echo -e "${BLUE}步骤 3: 提交更改${NC}"
git commit -m "Initial commit: Professional Data Analysis Dashboard

Features:
- 6 types of interactive charts
- Statistical analysis with correlation heatmap
- Data export (CSV/Excel)
- Sample dataset for demonstration
- Responsive UI design

Tech Stack: Python, Streamlit, Plotly, Pandas"

echo ""
echo -e "${BLUE}步骤 4: 创建 GitHub 仓库${NC}"
echo "请在浏览器中完成以下操作："
echo "1. 访问 https://github.com/new"
echo "2. 仓库名称: $PROJECT_NAME"
echo "3. 描述: Professional data analysis dashboard built with Streamlit and Plotly"
echo "4. 选择 Public（公开）"
echo "5. 点击 'Create repository'"
echo ""
read -p "完成后按 Enter 继续..."

echo ""
echo -e "${BLUE}步骤 5: 连接远程仓库${NC}"
git branch -M main
git remote add origin "https://github.com/$GITHUB_USERNAME/$PROJECT_NAME.git"

echo ""
echo -e "${BLUE}步骤 6: 推送到 GitHub${NC}"
git push -u origin main

echo ""
echo -e "${GREEN}✅ 上传完成！${NC}"
echo ""
echo "项目地址: https://github.com/$GITHUB_USERNAME/$PROJECT_NAME"
echo ""
echo "下一步:"
echo "1. 在 GitHub 上查看项目"
echo "2. 添加 topics: streamlit, plotly, data-visualization, python"
echo "3. 准备 Toptal 申请"
