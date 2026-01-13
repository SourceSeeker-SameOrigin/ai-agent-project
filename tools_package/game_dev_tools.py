"""
游戏开发专用工具集 - 让Agent具备Cursor级别的编程能力
"""

import os
import ast
import json
import re
import subprocess
from typing import Dict, List, Optional
from langchain_core.tools import Tool


class CodeAnalysisTools:
    """代码分析工具 - 理解代码结构"""
    
    @staticmethod
    def analyze_python_file(filepath: str) -> str:
        """
        深度分析Python文件结构
        提取：类、函数、导入、文档字符串等
        """
        try:
            if not os.path.exists(filepath):
                return f"错误：文件 {filepath} 不存在"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            
            result = {
                "imports": [],
                "classes": [],
                "functions": [],
                "global_vars": []
            }
            
            for node in ast.walk(tree):
                # 导入语句
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        result["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        result["imports"].append(f"{module}.{alias.name}")
                
                # 类定义
                elif isinstance(node, ast.ClassDef):
                    methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                    result["classes"].append({
                        "name": node.name,
                        "methods": methods,
                        "docstring": ast.get_docstring(node) or "无文档"
                    })
                
                # 函数定义（顶层）
                elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                    args = [arg.arg for arg in node.args.args]
                    result["functions"].append({
                        "name": node.name,
                        "args": args,
                        "docstring": ast.get_docstring(node) or "无文档"
                    })
            
            # 格式化输出
            output = f"📄 文件分析: {filepath}\n\n"
            output += f"📦 导入 ({len(result['imports'])}个):\n"
            for imp in result["imports"][:10]:  # 限制显示数量
                output += f"  - {imp}\n"
            
            output += f"\n🏛️ 类定义 ({len(result['classes'])}个):\n"
            for cls in result["classes"]:
                output += f"  - {cls['name']}\n"
                output += f"    方法: {', '.join(cls['methods'][:5])}\n"
                output += f"    说明: {cls['docstring'][:100]}\n"
            
            output += f"\n⚙️ 函数 ({len(result['functions'])}个):\n"
            for func in result["functions"]:
                output += f"  - {func['name']}({', '.join(func['args'])})\n"
                output += f"    说明: {func['docstring'][:100]}\n"
            
            return output
        
        except Exception as e:
            return f"代码分析错误: {str(e)}"
    
    @staticmethod
    def find_function_in_file(filepath_and_function: str) -> str:
        """
        在文件中查找特定函数的代码
        输入格式: "filepath|||function_name"
        """
        try:
            parts = filepath_and_function.split("|||")
            if len(parts) != 2:
                return "错误：参数格式应为 'filepath|||function_name'"
            
            filepath, function_name = parts[0].strip(), parts[1].strip()
            
            if not os.path.exists(filepath):
                return f"错误：文件 {filepath} 不存在"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    # 获取函数代码
                    lines = code.split('\n')
                    func_code = '\n'.join(lines[node.lineno-1:node.end_lineno])
                    
                    return f"找到函数 {function_name}:\n\n```python\n{func_code}\n```"
            
            return f"未找到函数: {function_name}"
        
        except Exception as e:
            return f"查找函数错误: {str(e)}"


class CodeEditingTools:
    """代码编辑工具 - 智能修改代码"""
    
    @staticmethod
    def replace_function(filepath_and_code: str) -> str:
        """
        替换文件中的某个函数
        输入格式: "filepath|||function_name|||new_code"
        """
        try:
            parts = filepath_and_code.split("|||")
            if len(parts) != 3:
                return "错误：参数格式应为 'filepath|||function_name|||new_code'"
            
            filepath, function_name, new_code = parts[0].strip(), parts[1].strip(), parts[2].strip()
            
            if not os.path.exists(filepath):
                return f"错误：文件 {filepath} 不存在"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            lines = code.split('\n')
            
            # 找到函数位置
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    # 替换函数代码
                    start_line = node.lineno - 1
                    end_line = node.end_lineno
                    
                    new_lines = lines[:start_line] + [new_code] + lines[end_line:]
                    new_content = '\n'.join(new_lines)
                    
                    # 写回文件
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    return f"✅ 成功替换函数 {function_name} 在文件 {filepath}"
            
            return f"未找到函数: {function_name}"
        
        except Exception as e:
            return f"替换函数错误: {str(e)}"
    
    @staticmethod
    def insert_code(filepath_and_params: str) -> str:
        """
        在文件指定位置插入代码
        输入格式: "filepath|||line_number|||code_to_insert"
        """
        try:
            parts = filepath_and_params.split("|||")
            if len(parts) != 3:
                return "错误：参数格式应为 'filepath|||line_number|||code_to_insert'"
            
            filepath, line_num, new_code = parts[0].strip(), int(parts[1].strip()), parts[2].strip()
            
            if not os.path.exists(filepath):
                return f"错误：文件 {filepath} 不存在"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 插入代码
            lines.insert(line_num - 1, new_code + '\n')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            return f"✅ 成功在文件 {filepath} 的第 {line_num} 行插入代码"
        
        except Exception as e:
            return f"插入代码错误: {str(e)}"
    
    @staticmethod
    def create_python_file(filepath_and_template: str) -> str:
        """
        创建新的Python文件（包含基础模板）
        输入格式: "filepath|||template_type"
        template_type: game_class, game_manager, player, enemy等
        """
        try:
            parts = filepath_and_template.split("|||")
            if len(parts) != 2:
                return "错误：参数格式应为 'filepath|||template_type'"
            
            filepath, template_type = parts[0].strip(), parts[1].strip()
            
            templates = {
                "game_class": '''"""
游戏主类
"""

import pygame


class Game:
    """游戏主类"""
    
    def __init__(self, width=800, height=600):
        """初始化游戏"""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        """更新游戏逻辑"""
        pass
    
    def render(self):
        """渲染画面"""
        self.screen.fill((0, 0, 0))  # 黑色背景
        pygame.display.flip()
    
    def run(self):
        """游戏主循环"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
''',
                "player": '''"""
玩家类
"""

import pygame


class Player:
    """玩家角色"""
    
    def __init__(self, x, y, width=50, height=50):
        """初始化玩家"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.color = (0, 255, 0)  # 绿色
        
    def move(self, keys):
        """根据按键移动"""
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
    
    def draw(self, screen):
        """绘制玩家"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        """获取碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
''',
                "enemy": '''"""
敌人类
"""

import pygame
import random


class Enemy:
    """敌人角色"""
    
    def __init__(self, x, y, width=40, height=40):
        """初始化敌人"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = random.randint(2, 4)
        self.color = (255, 0, 0)  # 红色
        
    def update(self):
        """更新敌人位置"""
        self.y += self.speed
    
    def draw(self, screen):
        """绘制敌人"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        """获取碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self, screen_height):
        """检查是否离开屏幕"""
        return self.y > screen_height
'''
            }
            
            if template_type not in templates:
                return f"错误：未知模板类型 '{template_type}'。可用模板: {', '.join(templates.keys())}"
            
            # 确保目录存在
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(templates[template_type])
            
            return f"✅ 成功创建文件 {filepath}（模板: {template_type}）"
        
        except Exception as e:
            return f"创建文件错误: {str(e)}"


class ProjectTools:
    """项目级工具 - 理解整个项目"""
    
    @staticmethod
    def analyze_project_structure(directory: str = ".") -> str:
        """
        分析项目结构
        列出所有Python文件及其主要组成
        """
        try:
            if not os.path.exists(directory):
                return f"错误：目录 {directory} 不存在"
            
            python_files = []
            for root, dirs, files in os.walk(directory):
                # 跳过虚拟环境和缓存目录
                dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'node_modules']]
                
                for file in files:
                    if file.endswith('.py'):
                        filepath = os.path.join(root, file)
                        python_files.append(filepath)
            
            if not python_files:
                return "未找到Python文件"
            
            result = f"📁 项目结构分析 ({directory})\n\n"
            result += f"找到 {len(python_files)} 个Python文件:\n\n"
            
            for filepath in python_files[:20]:  # 限制显示数量
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    tree = ast.parse(code)
                    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.col_offset == 0]
                    
                    result += f"📄 {filepath}\n"
                    if classes:
                        result += f"   类: {', '.join(classes[:5])}\n"
                    if functions:
                        result += f"   函数: {', '.join(functions[:5])}\n"
                    result += "\n"
                
                except:
                    result += f"📄 {filepath} (无法解析)\n\n"
            
            return result
        
        except Exception as e:
            return f"项目分析错误: {str(e)}"
    
    @staticmethod
    def search_code(directory_and_pattern: str) -> str:
        """
        在项目中搜索代码模式
        输入格式: "directory|||search_pattern"
        """
        try:
            parts = directory_and_pattern.split("|||")
            if len(parts) != 2:
                return "错误：参数格式应为 'directory|||search_pattern'"
            
            directory, pattern = parts[0].strip(), parts[1].strip()
            
            if not os.path.exists(directory):
                return f"错误：目录 {directory} 不存在"
            
            results = []
            for root, dirs, files in os.walk(directory):
                dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git']]
                
                for file in files:
                    if file.endswith('.py'):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                            
                            for i, line in enumerate(lines, 1):
                                if re.search(pattern, line):
                                    results.append(f"{filepath}:{i}: {line.strip()}")
                        except:
                            continue
            
            if not results:
                return f"未找到匹配 '{pattern}' 的代码"
            
            output = f"🔍 搜索结果 (模式: '{pattern}'):\n\n"
            for result in results[:30]:  # 限制显示数量
                output += f"{result}\n"
            
            return output
        
        except Exception as e:
            return f"搜索错误: {str(e)}"


class TestingTools:
    """测试工具 - 运行和验证代码"""
    
    @staticmethod
    def run_python_file(filepath: str) -> str:
        """
        运行Python文件并返回输出
        """
        try:
            if not os.path.exists(filepath):
                return f"错误：文件 {filepath} 不存在"
            
            result = subprocess.run(
                ['python', filepath],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=10
            )
            
            output = f"🚀 运行文件: {filepath}\n\n"
            
            if result.returncode == 0:
                output += f"✅ 执行成功\n\n"
                output += f"输出:\n{result.stdout}"
            else:
                output += f"❌ 执行失败 (退出码: {result.returncode})\n\n"
                output += f"错误:\n{result.stderr}"
            
            return output
        
        except subprocess.TimeoutExpired:
            return f"⏱️ 执行超时 (>10秒)"
        except Exception as e:
            return f"运行错误: {str(e)}"
    
    @staticmethod
    def check_syntax(filepath: str) -> str:
        """
        检查Python文件的语法错误
        """
        try:
            if not os.path.exists(filepath):
                return f"错误：文件 {filepath} 不存在"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            try:
                ast.parse(code)
                return f"✅ 语法检查通过: {filepath}"
            except SyntaxError as e:
                return f"❌ 语法错误: 第{e.lineno}行\n{e.msg}\n{e.text}"
        
        except Exception as e:
            return f"语法检查错误: {str(e)}"


class TerminalTools:
    """终端工具 - 像Cursor一样执行命令"""
    
    @staticmethod
    def run_terminal_command(command: str) -> str:
        """
        执行终端命令并返回结果
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
            )
            
            output = f"🔧 命令: {command}\n"
            output += f"📊 退出码: {result.returncode}\n\n"
            
            if result.returncode == 0:
                output += f"✅ 执行成功\n\n"
                if result.stdout:
                    output += f"输出:\n{result.stdout}"
            else:
                output += f"❌ 执行失败\n\n"
                if result.stderr:
                    output += f"错误:\n{result.stderr}"
            
            return output
        
        except subprocess.TimeoutExpired:
            return f"⏱️ 命令执行超时 (>30秒): {command}"
        except Exception as e:
            return f"执行命令错误: {str(e)}"


class PythonTools:
    """Python环境管理工具"""
    
    @staticmethod
    def pip_install(package: str) -> str:
        """
        安装Python包
        """
        try:
            result = subprocess.run(
                ['pip', 'install', package],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=120
            )
            
            if result.returncode == 0:
                return f"✅ 成功安装包: {package}\n{result.stdout}"
            else:
                return f"❌ 安装失败: {package}\n{result.stderr}"
        
        except subprocess.TimeoutExpired:
            return f"⏱️ 安装超时: {package}"
        except Exception as e:
            return f"安装错误: {str(e)}"
    
    @staticmethod
    def pip_list(input_text: str = "") -> str:
        """
        列出已安装的Python包
        参数input_text: 占位参数（不使用）
        """
        try:
            result = subprocess.run(
                ['pip', 'list'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
            )
            
            if result.returncode == 0:
                return f"📦 已安装的包:\n{result.stdout}"
            else:
                return f"❌ 获取包列表失败\n{result.stderr}"
        
        except Exception as e:
            return f"列出包错误: {str(e)}"
    
    @staticmethod
    def create_requirements(directory: str = ".") -> str:
        """
        生成requirements.txt文件
        """
        try:
            filepath = os.path.join(directory, "requirements.txt")
            
            result = subprocess.run(
                ['pip', 'freeze'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
            )
            
            if result.returncode == 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                return f"✅ 成功生成 requirements.txt\n位置: {filepath}"
            else:
                return f"❌ 生成失败\n{result.stderr}"
        
        except Exception as e:
            return f"生成requirements错误: {str(e)}"
    
    @staticmethod
    def check_python_version(input_text: str = "") -> str:
        """
        检查Python版本
        参数input_text: 占位参数（不使用）
        """
        try:
            result = subprocess.run(
                ['python', '--version'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=10
            )
            
            version = result.stdout.strip() or result.stderr.strip()
            return f"🐍 Python版本: {version}"
        
        except Exception as e:
            return f"检查版本错误: {str(e)}"


class GitTools:
    """Git版本控制工具"""
    
    @staticmethod
    def git_status(input_text: str = "") -> str:
        """
        查看Git状态
        参数input_text: 占位参数（不使用）
        """
        try:
            result = subprocess.run(
                ['git', 'status'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=10
            )
            
            if result.returncode == 0:
                return f"📊 Git状态:\n{result.stdout}"
            else:
                return f"❌ 获取Git状态失败（可能不是Git仓库）\n{result.stderr}"
        
        except Exception as e:
            return f"Git状态错误: {str(e)}"
    
    @staticmethod
    def git_init() -> str:
        """
        初始化Git仓库
        """
        try:
            result = subprocess.run(
                ['git', 'init'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=10
            )
            
            if result.returncode == 0:
                return f"✅ Git仓库初始化成功\n{result.stdout}"
            else:
                return f"❌ 初始化失败\n{result.stderr}"
        
        except Exception as e:
            return f"Git初始化错误: {str(e)}"


def create_game_dev_tools() -> List[Tool]:
    """
    创建完整的游戏开发工具集（像Cursor一样全面）
    """
    
    # ==================== Wrapper函数（处理无参数工具） ====================
    def safe_pip_list(input_arg=None) -> str:
        """安全的pip_list wrapper，处理任何类型的输入"""
        return PythonTools.pip_list("")
    
    def safe_check_python_version(input_arg=None) -> str:
        """安全的check_python_version wrapper，处理任何类型的输入"""
        return PythonTools.check_python_version("")
    
    def safe_git_status(input_arg=None) -> str:
        """安全的git_status wrapper，处理任何类型的输入"""
        return GitTools.git_status("")
    
    tools = [
        # ==================== 代码分析工具 ====================
        Tool(
            name="analyze_python_file",
            func=CodeAnalysisTools.analyze_python_file,
            description="深度分析Python文件结构，提取类、函数、导入等信息。输入：文件路径。Analyze Python file structure."
        ),
        Tool(
            name="find_function",
            func=CodeAnalysisTools.find_function_in_file,
            description="在文件中查找特定函数的代码。输入格式：'文件路径|||函数名'。Find function in file."
        ),
        
        # ==================== 代码编辑工具 ====================
        Tool(
            name="replace_function",
            func=CodeEditingTools.replace_function,
            description="替换文件中的某个函数。输入格式：'文件路径|||函数名|||新代码'。Replace function in file."
        ),
        Tool(
            name="insert_code",
            func=CodeEditingTools.insert_code,
            description="在文件指定位置插入代码。输入格式：'文件路径|||行号|||要插入的代码'。Insert code at line."
        ),
        Tool(
            name="create_game_file",
            func=CodeEditingTools.create_python_file,
            description="创建新的游戏文件（使用模板）。输入格式：'文件路径|||模板类型'。模板类型：game_class, player, enemy。Create game file from template."
        ),
        
        # ==================== 项目管理工具 ====================
        Tool(
            name="analyze_project",
            func=ProjectTools.analyze_project_structure,
            description="分析项目结构，列出所有Python文件及其组成。输入：目录路径（默认'.'）。Analyze project structure."
        ),
        Tool(
            name="search_code",
            func=ProjectTools.search_code,
            description="在项目中搜索代码模式。输入格式：'目录|||搜索模式'。Search code in project."
        ),
        
        # ==================== 测试验证工具 ====================
        Tool(
            name="run_python",
            func=TestingTools.run_python_file,
            description="运行Python文件并返回输出。输入：文件路径。Run Python file."
        ),
        Tool(
            name="check_syntax",
            func=TestingTools.check_syntax,
            description="检查Python文件的语法错误。输入：文件路径。Check syntax errors."
        ),
        
        # ==================== 终端工具 ====================
        Tool(
            name="run_command",
            func=TerminalTools.run_terminal_command,
            description="执行终端命令。输入：命令字符串（如 'ls -la' 或 'npm install'）。Run terminal command."
        ),
        
        # ==================== Python环境工具 ====================
        Tool(
            name="pip_install",
            func=PythonTools.pip_install,
            description="安装Python包。输入：包名（如 'pygame' 或 'numpy'）。Install Python package."
        ),
        Tool(
            name="pip_list",
            func=safe_pip_list,
            description="列出已安装的Python包。输入：'list'或任意文本。List installed packages."
        ),
        Tool(
            name="create_requirements",
            func=PythonTools.create_requirements,
            description="生成requirements.txt文件。输入：目录路径（默认'.'）。Create requirements.txt."
        ),
        Tool(
            name="check_python_version",
            func=safe_check_python_version,
            description="检查Python版本。输入：'check'或任意文本。Check Python version."
        ),
        
        # ==================== Git工具 ====================
        Tool(
            name="git_status",
            func=safe_git_status,
            description="查看Git状态。输入：'status'或任意文本。Check git status."
        ),
        Tool(
            name="git_init",
            func=GitTools.git_init,
            description="初始化Git仓库。输入：空字符串或任意文本。Initialize git repository."
        ),
    ]
    
    return tools


if __name__ == "__main__":
    # 测试工具
    print("=== 游戏开发工具集测试 ===\n")
    
    # 创建测试文件
    test_code = '''
def hello():
    """打招呼"""
    print("Hello, World!")

class TestClass:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        self.value += 1
'''
    
    with open('test_game.py', 'w') as f:
        f.write(test_code)
    
    print("1. 分析文件:")
    print(CodeAnalysisTools.analyze_python_file('test_game.py'))
    
    print("\n2. 查找函数:")
    print(CodeAnalysisTools.find_function_in_file('test_game.py|||hello'))
    
    print("\n3. 语法检查:")
    print(TestingTools.check_syntax('test_game.py'))
    
    # 清理
    os.remove('test_game.py')

