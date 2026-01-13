"""
自定义工具集
定义Agent可以使用的各种工具
"""

import os
import json
import requests
from datetime import datetime
from typing import Optional
# langchain 0.3.x 的导入
from langchain_core.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
import math


class FileTools:
    """文件操作工具"""
    
    @staticmethod
    def read_file(filepath: str) -> str:
        """读取文件内容"""
        try:
            if not os.path.exists(filepath):
                return f"错误：文件 {filepath} 不存在"
            
            # 尝试多种编码方式读取
            encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
            content = None
            
            for encoding in encodings:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                # 如果所有编码都失败，使用二进制模式
                with open(filepath, 'rb') as f:
                    content = f.read().decode('utf-8', errors='ignore')
            
            # 限制长度
            if len(content) > 5000:
                content = content[:5000] + "\n...(内容过长，已截断)"
            
            return f"文件内容（{len(content)}字符）:\n{content}"
        except Exception as e:
            return f"读取文件错误: {str(e)}"
    
    @staticmethod
    def write_file(filepath_and_content: str) -> str:
        """
        写入文件
        参数格式: "filepath|||content"
        """
        try:
            parts = filepath_and_content.split("|||")
            if len(parts) != 2:
                return "错误：参数格式应为 'filepath|||content'"
            
            filepath, content = parts[0].strip(), parts[1].strip()
            
            # 确保目录存在
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"成功：文件已保存到 {filepath}"
        except Exception as e:
            return f"写入文件错误: {str(e)}"
    
    @staticmethod
    def list_directory(path: str = ".") -> str:
        """列出目录内容"""
        try:
            if not os.path.exists(path):
                return f"错误：路径 {path} 不存在"
            
            items = os.listdir(path)
            files = [f"📄 {item}" for item in items if os.path.isfile(os.path.join(path, item))]
            dirs = [f"📁 {item}" for item in items if os.path.isdir(os.path.join(path, item))]
            
            result = f"目录: {os.path.abspath(path)}\n\n"
            result += "文件夹:\n" + "\n".join(dirs) if dirs else "文件夹: (无)"
            result += "\n\n文件:\n" + "\n".join(files) if files else "\n\n文件: (无)"
            return result
        except Exception as e:
            return f"列出目录错误: {str(e)}"


class CalculatorTools:
    """计算器工具"""
    
    @staticmethod
    def calculate(expression: str) -> str:
        """
        执行数学计算
        支持: +, -, *, /, **, sqrt, sin, cos, tan, log等
        """
        try:
            # 安全的数学函数白名单
            safe_dict = {
                'abs': abs,
                'round': round,
                'max': max,
                'min': min,
                'sum': sum,
                'pow': pow,
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log,
                'log10': math.log10,
                'exp': math.exp,
                'pi': math.pi,
                'e': math.e,
            }
            
            # 计算结果
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            return f"计算结果: {expression} = {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"


class WebTools:
    """网络工具"""
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """清理文本，确保编码正确"""
        try:
            # 确保是字符串
            if not isinstance(text, str):
                text = str(text)
            
            # 移除不可打印的字符，保留中文
            cleaned = ''.join(char for char in text if char.isprintable() or char in '\n\t ')
            
            # 确保返回 UTF-8 编码的字符串
            return cleaned.encode('utf-8', errors='ignore').decode('utf-8')
        except Exception:
            # 如果清理失败，返回安全的字符串
            return str(text).encode('ascii', errors='ignore').decode('ascii')
    
    @staticmethod
    def search_web(query: str) -> str:
        """
        搜索网络信息
        """
        try:
            search = DuckDuckGoSearchRun()
            results = search.run(query)
            
            # 清理搜索结果
            cleaned_results = WebTools._clean_text(results)
            
            # 限制长度
            if len(cleaned_results) > 1500:
                cleaned_results = cleaned_results[:1500] + "\n...(结果过长，已截断)"
            
            return f"搜索结果:\n{cleaned_results}"
        except Exception as e:
            error_msg = WebTools._clean_text(str(e))
            return f"搜索错误: {error_msg}\n提示: 请确保网络连接正常"
    
    @staticmethod
    def get_webpage(url: str) -> str:
        """
        获取网页内容
        """
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            # 设置正确的编码
            response.encoding = response.apparent_encoding or 'utf-8'
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 移除script和style标签
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            
            # 清理文本
            text = WebTools._clean_text(text)
            
            # 清理多余空白
            lines = (line.strip() for line in text.splitlines())
            text = '\n'.join(line for line in lines if line)
            
            # 限制长度
            if len(text) > 2000:
                text = text[:2000] + "\n...(内容过长，已截断)"
            
            return f"网页内容:\n{text}"
        except Exception as e:
            error_msg = WebTools._clean_text(str(e))
            return f"获取网页错误: {error_msg}"


class SystemTools:
    """系统工具"""
    
    @staticmethod
    def get_current_time(dummy: str = "") -> str:
        """获取当前时间（不需要输入参数）"""
        now = datetime.now()
        return f"当前时间: {now.strftime('%Y年%m月%d日 %H:%M:%S')} 星期{['一', '二', '三', '四', '五', '六', '日'][now.weekday()]}"
    
    @staticmethod
    def get_weather(city: str) -> str:
        """
        获取天气信息（示例实现）
        注意：实际使用需要申请天气API密钥
        """
        return f"天气功能需要配置API密钥。您可以在 https://www.weatherapi.com/ 申请免费密钥"


class DataTools:
    """数据处理工具"""
    
    @staticmethod
    def analyze_json(json_str: str) -> str:
        """分析JSON数据"""
        try:
            data = json.loads(json_str)
            
            def analyze(obj, depth=0):
                indent = "  " * depth
                if isinstance(obj, dict):
                    result = f"对象 (包含{len(obj)}个键):\n"
                    for key, value in obj.items():
                        result += f"{indent}- {key}: {analyze(value, depth+1)}"
                    return result
                elif isinstance(obj, list):
                    return f"数组 (包含{len(obj)}个元素)\n"
                else:
                    return f"{type(obj).__name__}: {obj}\n"
            
            return analyze(data)
        except Exception as e:
            return f"JSON解析错误: {str(e)}"


def create_tools(enable_clip=False):
    """
    创建所有工具的列表
    
    参数:
        enable_clip: 是否启用CLIP图像分析工具（需要先安装CLIP库）
    """
    
    tools = [
        # 文件操作工具
        Tool(
            name="read_file",
            func=FileTools.read_file,
            description="读取文件内容。输入：文件路径（如 'data.txt'）。Read file content."
        ),
        Tool(
            name="write_file",
            func=FileTools.write_file,
            description="写入文件。输入格式：'文件路径|||文件内容'（用三个竖线分隔）。Write file."
        ),
        Tool(
            name="list_directory",
            func=FileTools.list_directory,
            description="列出目录中的文件和文件夹。输入：目录路径（默认为当前目录'.'）。List directory contents."
        ),
        
        # 计算工具
        Tool(
            name="calculator",
            func=CalculatorTools.calculate,
            description="执行数学计算。支持基本运算和数学函数（如sqrt, sin, cos等）。输入：数学表达式。Calculate math expressions."
        ),
        
        # 网络工具
        Tool(
            name="web_search",
            func=WebTools.search_web,
            description="搜索网络信息。输入：搜索关键词。Search the web."
        ),
        Tool(
            name="get_webpage",
            func=WebTools.get_webpage,
            description="获取网页文本内容。输入：完整URL（如 'https://example.com'）。Get webpage content."
        ),
        
        # 系统工具
        Tool(
            name="get_current_time",
            func=SystemTools.get_current_time,
            description="获取当前日期和时间。输入：空字符串或任意文本（将被忽略）。Get current time."
        ),
        
        # 数据工具
        Tool(
            name="analyze_json",
            func=DataTools.analyze_json,
            description="分析JSON数据结构。输入：JSON字符串。Analyze JSON data."
        ),
    ]
    
    # 可选：添加CLIP图像分析工具
    if enable_clip:
        try:
            from .clip_tools import create_clip_tools
            clip_tools = create_clip_tools()
            tools.extend(clip_tools)
            print("✅ CLIP图像分析工具已启用")
        except ImportError:
            print("⚠️  CLIP工具未能加载（CLIP库未安装或不可用）")
    
    return tools


if __name__ == "__main__":
    # 测试工具
    print("=== 测试工具集 ===\n")
    
    print("1. 获取时间:")
    print(SystemTools.get_current_time())
    
    print("\n2. 计算:")
    print(CalculatorTools.calculate("2 + 2 * 3"))
    print(CalculatorTools.calculate("sqrt(16) + pow(2, 3)"))
    
    print("\n3. 列出当前目录:")
    print(FileTools.list_directory("."))

