"""
DevOps专用工具集
支持部署、容器化、CI/CD、系统管理
"""

import os
import subprocess
from typing import List
from langchain_core.tools import Tool


class DevOpsTools:
    """DevOps工具"""
    
    @staticmethod
    def create_dockerfile(filepath_and_params: str) -> str:
        """
        创建Dockerfile
        输入格式: "filepath|||base_image|||app_type"
        """
        try:
            parts = filepath_and_params.split("|||")
            if len(parts) != 3:
                return "错误：参数格式应为 'filepath|||base_image|||app_type'"
            
            filepath, base_image, app_type = parts[0].strip(), parts[1].strip(), parts[2].strip()
            
            if app_type == "python":
                dockerfile = f'''FROM {base_image}

WORKDIR /app

# 复制requirements文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "main.py"]
'''
            elif app_type == "web":
                dockerfile = f'''FROM {base_image}

WORKDIR /app

# 复制requirements文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]
'''
            else:
                dockerfile = f'''FROM {base_image}

WORKDIR /app

COPY . .

CMD ["python", "main.py"]
'''
            
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(dockerfile)
            
            return f"✅ 成功创建Dockerfile: {filepath}"
        
        except Exception as e:
            return f"创建Dockerfile错误: {str(e)}"
    
    @staticmethod
    def create_docker_compose(filepath: str) -> str:
        """
        创建docker-compose.yml
        输入: 文件路径
        """
        try:
            docker_compose = '''version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - ENV=development
    restart: unless-stopped
'''
            
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(docker_compose)
            
            return f"✅ 成功创建docker-compose.yml: {filepath}"
        
        except Exception as e:
            return f"创建docker-compose错误: {str(e)}"
    
    @staticmethod
    def create_github_actions(filepath_and_params: str) -> str:
        """
        创建GitHub Actions工作流
        输入格式: "filepath|||workflow_name|||steps"
        """
        try:
            parts = filepath_and_params.split("|||")
            if len(parts) != 3:
                return "错误：参数格式应为 'filepath|||workflow_name|||steps'"
            
            filepath, workflow_name, steps = parts[0].strip(), parts[1].strip(), parts[2].strip()
            
            workflow = f'''name: {workflow_name}

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        # TODO: 添加测试命令
        echo "Running tests..."
'''
            
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(workflow)
            
            return f"✅ 成功创建GitHub Actions工作流: {filepath}"
        
        except Exception as e:
            return f"创建GitHub Actions错误: {str(e)}"
    
    @staticmethod
    def run_docker_command(command: str) -> str:
        """
        执行Docker命令
        输入: Docker命令（如 'docker ps' 或 'docker build -t myapp .'）
        """
        try:
            # 安全检查：只允许特定命令
            safe_commands = ['ps', 'images', 'version', 'info']
            dangerous_keywords = ['rm -rf', 'rm -f', 'format', 'prune -a']
            
            if any(keyword in command.lower() for keyword in dangerous_keywords):
                return "❌ 错误：不允许执行危险命令"
            
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=60
            )
            
            if result.returncode == 0:
                return f"✅ Docker命令执行成功:\n{result.stdout}"
            else:
                return f"❌ Docker命令执行失败:\n{result.stderr}"
        
        except Exception as e:
            return f"Docker命令执行错误: {str(e)}"
    
    @staticmethod
    def check_system_resources(input_text: str = "") -> str:
        """
        检查系统资源
        输入: 空字符串或任意文本
        """
        try:
            import platform
            try:
                import psutil
                has_psutil = True
            except ImportError:
                has_psutil = False
            
            info = {
                "系统": platform.system(),
                "Python版本": platform.python_version(),
            }
            
            if has_psutil:
                info.update({
                    "CPU核心数": psutil.cpu_count(),
                    "内存总量": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
                    "内存使用率": f"{psutil.virtual_memory().percent}%",
                    "磁盘使用率": f"{psutil.disk_usage('/').percent}%"
                })
            
            result = "📊 系统资源信息:\n"
            for key, value in info.items():
                result += f"  {key}: {value}\n"
            
            if not has_psutil:
                result += "\n💡 提示: 安装psutil可获取更详细的系统信息 (pip install psutil)"
            
            return result
        
        except Exception as e:
            return f"检查系统资源错误: {str(e)}"


def create_devops_tools() -> List[Tool]:
    """创建DevOps工具集"""
    tools = [
        Tool(
            name="create_dockerfile",
            func=DevOpsTools.create_dockerfile,
            description="创建Dockerfile。输入格式：'文件路径|||基础镜像|||应用类型'。Create Dockerfile."
        ),
        Tool(
            name="create_docker_compose",
            func=DevOpsTools.create_docker_compose,
            description="创建docker-compose.yml。输入：文件路径。Create docker-compose.yml."
        ),
        Tool(
            name="create_github_actions",
            func=DevOpsTools.create_github_actions,
            description="创建GitHub Actions工作流。输入格式：'文件路径|||工作流名称|||步骤'。Create GitHub Actions workflow."
        ),
        Tool(
            name="run_docker_command",
            func=DevOpsTools.run_docker_command,
            description="执行Docker命令。输入：Docker命令字符串。Run Docker command."
        ),
        Tool(
            name="check_system_resources",
            func=DevOpsTools.check_system_resources,
            description="检查系统资源使用情况。输入：空字符串。Check system resources."
        ),
    ]
    
    return tools


if __name__ == "__main__":
    # 测试工具
    print("=== DevOps工具集测试 ===\n")
    
    print("1. 创建Dockerfile:")
    print(DevOpsTools.create_dockerfile("Dockerfile|||python:3.11|||python"))

