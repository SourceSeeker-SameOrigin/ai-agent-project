"""
代码质量与可靠性工具集
支持代码检查、测试、备份等
"""

import os
import shutil
import subprocess
import ast
from typing import List
from datetime import datetime
from langchain_core.tools import Tool


class QualityTools:
    """代码质量工具"""
    
    @staticmethod
    def check_code_quality(filepath: str) -> str:
        """
        检查代码质量（语法、风格、类型）
        输入: 文件路径
        """
        try:
            if not os.path.exists(filepath):
                return f"错误：文件 {filepath} 不存在"
            
            results = []
            
            # 1. 语法检查
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    code = f.read()
                ast.parse(code)
                results.append("✅ 语法检查: 通过")
            except SyntaxError as e:
                results.append(f"❌ 语法错误: 第{e.lineno}行 - {e.msg}")
            
            # 2. 尝试使用ruff检查（如果可用）
            try:
                result = subprocess.run(
                    ['ruff', 'check', filepath],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    results.append("✅ 代码风格检查: 通过 (ruff)")
                else:
                    results.append(f"⚠️ 代码风格问题 (ruff):\n{result.stdout}")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                results.append("ℹ️  ruff未安装，跳过代码风格检查")
            
            # 3. 尝试使用mypy检查（如果可用）
            try:
                result = subprocess.run(
                    ['mypy', filepath],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    results.append("✅ 类型检查: 通过 (mypy)")
                else:
                    results.append(f"⚠️ 类型问题 (mypy):\n{result.stdout[:500]}")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                results.append("ℹ️  mypy未安装，跳过类型检查")
            
            return "\n".join(results)
        
        except Exception as e:
            return f"代码质量检查错误: {str(e)}"
    
    @staticmethod
    def run_tests(test_path: str) -> str:
        """
        运行测试
        输入: 测试文件路径或目录
        """
        try:
            if not os.path.exists(test_path):
                return f"错误：路径 {test_path} 不存在"
            
            # 尝试使用pytest
            try:
                result = subprocess.run(
                    ['pytest', test_path, '-v'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                output = f"📊 测试结果 ({test_path}):\n"
                output += result.stdout
                if result.stderr:
                    output += f"\n错误输出:\n{result.stderr}"
                
                if result.returncode == 0:
                    output = "✅ " + output
                else:
                    output = "❌ " + output
                
                return output
            
            except FileNotFoundError:
                # 如果没有pytest，尝试直接运行Python文件
                if test_path.endswith('.py'):
                    result = subprocess.run(
                        ['python', test_path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    return f"📊 测试执行结果:\n{result.stdout}\n{result.stderr}"
                else:
                    return "⚠️ pytest未安装，且路径不是Python文件"
        
        except subprocess.TimeoutExpired:
            return "⏱️ 测试执行超时"
        except Exception as e:
            return f"运行测试错误: {str(e)}"
    
    @staticmethod
    def backup_file(filepath: str) -> str:
        """
        备份文件
        输入: 文件路径
        """
        try:
            if not os.path.exists(filepath):
                return f"错误：文件 {filepath} 不存在"
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{filepath}.bak_{timestamp}"
            
            shutil.copy2(filepath, backup_path)
            
            return f"✅ 文件已备份到: {backup_path}"
        
        except Exception as e:
            return f"备份文件错误: {str(e)}"
    
    @staticmethod
    def restore_backup(backup_path: str) -> str:
        """
        恢复备份文件
        输入: 备份文件路径
        """
        try:
            if not os.path.exists(backup_path):
                return f"错误：备份文件 {backup_path} 不存在"
            
            # 移除.bak_时间戳后缀
            original_path = backup_path.rsplit('.bak_', 1)[0]
            
            shutil.copy2(backup_path, original_path)
            
            return f"✅ 文件已从备份恢复: {original_path}"
        
        except Exception as e:
            return f"恢复备份错误: {str(e)}"
    
    @staticmethod
    def create_test_file(filepath_and_params: str) -> str:
        """
        创建测试文件模板
        输入格式: "filepath|||target_module|||test_type"
        """
        try:
            parts = filepath_and_params.split("|||")
            if len(parts) != 3:
                return "错误：参数格式应为 'filepath|||target_module|||test_type'"
            
            filepath, target_module, test_type = parts[0].strip(), parts[1].strip(), parts[2].strip()
            
            template = f'''"""
测试文件 - {test_type}
目标模块: {target_module}
"""

import pytest
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from {target_module} import *


class Test{target_module.capitalize()}:
    """{target_module}测试类"""
    
    def setup_method(self):
        """测试前准备"""
        pass
    
    def teardown_method(self):
        """测试后清理"""
        pass
    
    def test_example(self):
        """示例测试"""
        assert True
    
    # TODO: 添加更多测试用例


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''
            
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(template)
            
            return f"✅ 成功创建测试文件: {filepath}"
        
        except Exception as e:
            return f"创建测试文件错误: {str(e)}"
    
    @staticmethod
    def install_quality_tools(input_text: str = "") -> str:
        """
        安装代码质量工具
        输入: 空字符串或任意文本
        """
        try:
            tools = ['ruff', 'mypy', 'pytest']
            
            result = subprocess.run(
                ['pip', 'install'] + tools,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=120
            )
            
            if result.returncode == 0:
                return f"✅ 成功安装代码质量工具: {', '.join(tools)}\n{result.stdout[:500]}"
            else:
                return f"❌ 安装失败:\n{result.stderr[:500]}"
        
        except Exception as e:
            return f"安装工具错误: {str(e)}"


def create_quality_tools() -> List[Tool]:
    """创建代码质量工具集"""
    tools = [
        Tool(
            name="check_code_quality",
            func=QualityTools.check_code_quality,
            description="检查代码质量（语法、风格、类型）。输入：文件路径。Check code quality."
        ),
        Tool(
            name="run_tests",
            func=QualityTools.run_tests,
            description="运行测试。输入：测试文件路径或目录。Run tests."
        ),
        Tool(
            name="backup_file",
            func=QualityTools.backup_file,
            description="备份文件。输入：文件路径。Backup file."
        ),
        Tool(
            name="restore_backup",
            func=QualityTools.restore_backup,
            description="恢复备份文件。输入：备份文件路径。Restore backup file."
        ),
        Tool(
            name="create_test_file",
            func=QualityTools.create_test_file,
            description="创建测试文件模板。输入格式：'文件路径|||目标模块|||测试类型'。Create test file template."
        ),
        Tool(
            name="install_quality_tools",
            func=QualityTools.install_quality_tools,
            description="安装代码质量工具（ruff, mypy, pytest）。输入：空字符串。Install quality tools."
        ),
    ]
    
    return tools


if __name__ == "__main__":
    # 测试工具
    print("=== 代码质量工具集测试 ===\n")
    
    print("1. 创建测试文件:")
    print(QualityTools.create_test_file("test_example.py|||example|||unit"))

