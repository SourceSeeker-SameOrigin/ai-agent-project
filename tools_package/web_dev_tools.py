"""
Web开发专用工具集
支持Flask、FastAPI、Django等Web框架开发
"""

import os
import json
import subprocess
import requests
from typing import Dict, List
from langchain_core.tools import Tool


class WebDevTools:
    """Web开发工具"""
    
    @staticmethod
    def create_flask_app(filepath_and_name: str) -> str:
        """
        创建Flask应用模板
        输入格式: "filepath|||app_name"
        """
        try:
            parts = filepath_and_name.split("|||")
            if len(parts) != 2:
                return "错误：参数格式应为 'filepath|||app_name'"
            
            filepath, app_name = parts[0].strip(), parts[1].strip()
            
            template = f'''"""
{app_name} - Flask应用
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    """首页"""
    return jsonify({{"message": "Welcome to {app_name}", "status": "ok"}})

@app.route('/api/health')
def health():
    """健康检查"""
    return jsonify({{"status": "healthy"}})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
            
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(template)
            
            return f"✅ 成功创建Flask应用: {filepath}"
        
        except Exception as e:
            return f"创建Flask应用错误: {str(e)}"
    
    @staticmethod
    def create_fastapi_app(filepath_and_name: str) -> str:
        """
        创建FastAPI应用模板
        输入格式: "filepath|||app_name"
        """
        try:
            parts = filepath_and_name.split("|||")
            if len(parts) != 2:
                return "错误：参数格式应为 'filepath|||app_name'"
            
            filepath, app_name = parts[0].strip(), parts[1].strip()
            
            template = f'''"""
{app_name} - FastAPI应用
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="{app_name}", version="1.0.0")

@app.get("/")
async def root():
    """首页"""
    return {{"message": "Welcome to {app_name}", "status": "ok"}}

@app.get("/api/health")
async def health():
    """健康检查"""
    return {{"status": "healthy"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
            
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(template)
            
            return f"✅ 成功创建FastAPI应用: {filepath}"
        
        except Exception as e:
            return f"创建FastAPI应用错误: {str(e)}"
    
    @staticmethod
    def create_api_route(filepath_and_route: str) -> str:
        """
        创建API路由
        输入格式: "filepath|||method|||path|||function_name"
        """
        try:
            parts = filepath_and_route.split("|||")
            if len(parts) != 4:
                return "错误：参数格式应为 'filepath|||method|||path|||function_name'"
            
            filepath, method, path, func_name = parts[0].strip(), parts[1].strip().upper(), parts[2].strip(), parts[3].strip()
            
            if not os.path.exists(filepath):
                return f"错误：文件 {filepath} 不存在"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 生成路由代码
            if 'fastapi' in content.lower():
                route_code = f'''
@app.{method.lower()}("{path}")
async def {func_name}():
    """{func_name}路由"""
    return {{"message": "Hello from {func_name}"}}
'''
            elif 'flask' in content.lower():
                route_code = f'''
@app.route("{path}", methods=["{method}"])
def {func_name}():
    """{func_name}路由"""
    return jsonify({{"message": "Hello from {func_name}"}})
'''
            else:
                return "错误：无法识别Web框架类型"
            
            # 在文件末尾添加路由
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(route_code)
            
            return f"✅ 成功添加{method}路由 {path} -> {func_name}"
        
        except Exception as e:
            return f"创建API路由错误: {str(e)}"
    
    @staticmethod
    def test_http_endpoint(url: str) -> str:
        """
        测试HTTP端点
        输入: URL地址
        """
        try:
            response = requests.get(url, timeout=5)
            result = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text[:500]  # 限制长度
            }
            return f"✅ HTTP测试结果:\n{json.dumps(result, indent=2, ensure_ascii=False)}"
        except Exception as e:
            return f"HTTP测试错误: {str(e)}"
    
    @staticmethod
    def create_requirements_web(filepath: str) -> str:
        """
        创建Web项目requirements.txt
        输入: 目录路径
        """
        try:
            req_file = os.path.join(filepath, "requirements.txt")
            
            # 检测项目类型并生成对应的requirements
            flask_files = [f for f in os.listdir(filepath) if f.endswith('.py')] if os.path.exists(filepath) else []
            is_flask = any('flask' in open(os.path.join(filepath, f), 'r', encoding='utf-8', errors='ignore').read().lower() for f in flask_files if os.path.isfile(os.path.join(filepath, f)))
            is_fastapi = any('fastapi' in open(os.path.join(filepath, f), 'r', encoding='utf-8', errors='ignore').read().lower() for f in flask_files if os.path.isfile(os.path.join(filepath, f)))
            
            requirements = []
            if is_fastapi:
                requirements = ["fastapi>=0.100.0", "uvicorn[standard]>=0.23.0", "pydantic>=2.0.0"]
            elif is_flask:
                requirements = ["flask>=2.3.0", "werkzeug>=2.3.0"]
            else:
                requirements = ["flask>=2.3.0", "fastapi>=0.100.0", "uvicorn[standard]>=0.23.0"]
            
            with open(req_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(requirements))
            
            return f"✅ 成功创建requirements.txt: {req_file}"
        
        except Exception as e:
            return f"创建requirements错误: {str(e)}"


def create_web_dev_tools() -> List[Tool]:
    """创建Web开发工具集"""
    tools = [
        Tool(
            name="create_flask_app",
            func=WebDevTools.create_flask_app,
            description="创建Flask应用模板。输入格式：'文件路径|||应用名称'。Create Flask app template."
        ),
        Tool(
            name="create_fastapi_app",
            func=WebDevTools.create_fastapi_app,
            description="创建FastAPI应用模板。输入格式：'文件路径|||应用名称'。Create FastAPI app template."
        ),
        Tool(
            name="create_api_route",
            func=WebDevTools.create_api_route,
            description="创建API路由。输入格式：'文件路径|||HTTP方法|||路径|||函数名'。Create API route."
        ),
        Tool(
            name="test_http_endpoint",
            func=WebDevTools.test_http_endpoint,
            description="测试HTTP端点。输入：URL地址。Test HTTP endpoint."
        ),
        Tool(
            name="create_requirements_web",
            func=WebDevTools.create_requirements_web,
            description="创建Web项目requirements.txt。输入：目录路径。Create web project requirements."
        ),
    ]
    
    return tools


if __name__ == "__main__":
    # 测试工具
    print("=== Web开发工具集测试 ===\n")
    
    print("1. 创建Flask应用:")
    print(WebDevTools.create_flask_app("test_flask.py|||MyFlaskApp"))
    
    print("\n2. 创建FastAPI应用:")
    print(WebDevTools.create_fastapi_app("test_fastapi.py|||MyFastAPIApp"))

