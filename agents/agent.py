"""
AI Agent 主程序
基于 LangChain + OpenAI 实现的智能代理
"""

import os
from typing import Optional
from dotenv import load_dotenv
# langchain 1.2.x 的新导入方式
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools_package.tools import create_tools
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import print as rprint


# 加载环境变量
load_dotenv()

console = Console()


class AIAgent:
    """AI Agent 类"""
    
    def __init__(
        self,
        model: str = None,
        temperature: float = 0,
        max_iterations: int = 10,
        verbose: bool = True
    ):
        """
        初始化AI Agent
        
        Args:
            model: OpenAI模型名称（默认从环境变量读取）
            temperature: 温度参数，控制输出随机性（0-1）
            max_iterations: 最大迭代次数
            verbose: 是否显示详细日志
        """
        # 检查API密钥
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "未找到 OPENAI_API_KEY！\n"
                "请在项目根目录创建 .env 文件，并添加：\n"
                "OPENAI_API_KEY=sk-your-api-key-here"
            )
        
        # 初始化LLM
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            api_key=api_key
        )
        
        # 创建工具
        self.tools = create_tools()
        
        # 创建系统提示
        system_prompt = self._create_system_prompt()
        
        # 使用新的 create_agent API (langchain 1.2.x)
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt,
            debug=verbose
        )
        
        self.verbose = verbose
        self.max_iterations = max_iterations
        
        console.print(Panel.fit(
            f"[bold green]🤖 AI Agent 已启动[/bold green]\n\n"
            f"模型: {self.model}\n"
            f"可用工具数: {len(self.tools)}\n"
            f"最大迭代: {max_iterations}",
            title="系统信息"
        ))
    
    def _create_system_prompt(self) -> str:
        """创建系统提示"""
        return """你是一个强大的AI助手，可以使用各种工具来帮助用户完成任务。

工作方式：
1. 仔细分析用户的问题
2. 选择合适的工具来解决问题
3. 根据工具的执行结果进行思考
4. 重复以上步骤，直到得出最终答案

重要规则：
- 仔细阅读工具描述，确保正确使用
- "写入文件"工具的输入格式必须是: 文件路径|||文件内容（用三个竖线分隔）
- "获取时间"工具不需要任何输入参数，直接调用即可
- 如果工具返回错误，尝试调整参数或使用其他方法
- 始终用中文回复用户，给出友好、清晰的答案
- 当你完成任务后，直接给出最终答案，不需要说明使用了哪些工具"""
    
    def run(self, task: str) -> dict:
        """
        执行任务
        
        Args:
            task: 用户输入的任务描述
            
        Returns:
            执行结果字典
        """
        try:
            if self.verbose:
                console.print(f"\n[bold blue]🎯 任务:[/bold blue] {task}\n")
            
            # langchain 1.2.x 使用新的消息格式
            inputs = {"messages": [{"role": "user", "content": task}]}
            
            # 执行 agent
            response = self.agent.invoke(inputs)
            
            # 提取最后一条消息作为输出
            messages = response.get("messages", [])
            if messages:
                last_message = messages[-1]
                output = last_message.content if hasattr(last_message, 'content') else str(last_message)
            else:
                output = "未能获取响应"
            
            if self.verbose:
                console.print("\n[bold green]✅ 最终答案:[/bold green]")
                console.print(Panel(output, border_style="green"))
            
            return {"output": output, "messages": messages}
        
        except Exception as e:
            error_msg = f"执行错误: {str(e)}"
            console.print(f"\n[bold red]❌ {error_msg}[/bold red]")
            return {"error": error_msg, "output": error_msg}
    
    def chat(self):
        """交互式对话模式"""
        console.print("\n[bold cyan]💬 进入对话模式[/bold cyan]")
        console.print("[dim]输入 'exit' 或 'quit' 退出[/dim]\n")
        
        while True:
            try:
                # 获取用户输入
                user_input = console.input("[bold yellow]👤 你:[/bold yellow] ")
                
                if user_input.lower() in ['exit', 'quit', '退出']:
                    console.print("\n[bold]👋 再见！[/bold]")
                    break
                
                if not user_input.strip():
                    continue
                
                # 执行任务
                self.run(user_input)
                
            except KeyboardInterrupt:
                console.print("\n\n[bold]👋 再见！[/bold]")
                break
            except Exception as e:
                console.print(f"\n[bold red]错误: {str(e)}[/bold red]\n")
    
    def list_tools(self):
        """列出所有可用工具"""
        console.print("\n[bold cyan]🔧 可用工具列表:[/bold cyan]\n")
        
        for i, tool in enumerate(self.tools, 1):
            console.print(f"[bold]{i}. {tool.name}[/bold]")
            console.print(f"   {tool.description}\n")


def main():
    """主函数"""
    import sys
    
    # 创建Agent
    try:
        agent = AIAgent(
            temperature=float(os.getenv("TEMPERATURE", 0)),
            max_iterations=int(os.getenv("MAX_ITERATIONS", 10)),
            verbose=os.getenv("VERBOSE", "true").lower() == "true"
        )
    except ValueError as e:
        console.print(f"[bold red]初始化错误: {e}[/bold red]")
        return
    
    # 命令行参数处理
    if len(sys.argv) > 1:
        if sys.argv[1] == "--tools":
            agent.list_tools()
        elif sys.argv[1] == "--task":
            if len(sys.argv) > 2:
                task = " ".join(sys.argv[2:])
                agent.run(task)
            else:
                console.print("[red]错误: --task 需要提供任务描述[/red]")
        else:
            console.print(f"[red]未知参数: {sys.argv[1]}[/red]")
            console.print("\n使用方法:")
            console.print("  python agent.py              # 进入对话模式")
            console.print("  python agent.py --tools      # 列出所有工具")
            console.print("  python agent.py --task <任务> # 执行单个任务")
    else:
        # 默认进入对话模式
        agent.chat()


if __name__ == "__main__":
    main()

