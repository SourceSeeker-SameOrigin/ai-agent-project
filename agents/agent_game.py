
"""
游戏开发专用Agent - 混合版本
结合流式输出的实时性 + 手动解析的可靠性
"""

import os
import time
from typing import Optional
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools_package.tools import create_tools
from tools_package.game_dev_tools import create_game_dev_tools
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()


class GameDevAgent:
    """游戏开发Agent - 混合版本 - 流式+可靠"""

    def __init__(
            self,
            model: str = None,
            temperature: float = 0,
            verbose: bool = True,
            service: str = "deepseek"
    ):
        """初始化游戏开发Agent"""
        self.service = service
        self.verbose = verbose

        # 配置API
        if service == "deepseek":
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                raise ValueError("未找到 DEEPSEEK_API_KEY！请在 .env 文件中添加")
            self.model = model or "deepseek-chat"
            base_url = "https://api.deepseek.com/v1"
        elif service == "dashscope":
            api_key = os.getenv("DASHSCOPE_API_KEY")
            if not api_key:
                raise ValueError("未找到 DASHSCOPE_API_KEY！")
            self.model = model or "qwen-turbo"
            base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        else:
            raise ValueError(f"不支持的服务: {service}")

        # 初始化LLM
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            api_key=api_key,
            base_url=base_url
        )

        # 创建工具集
        basic_tools = create_tools(enable_clip=False)
        game_tools = create_game_dev_tools()
        self.tools = basic_tools + game_tools

        # 🔑 增强的System Prompt - 强制使用工具
        system_prompt = self._create_system_prompt()

        # 创建Agent
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt,
            debug=False
        )

        console.print(Panel.fit(
            f"[bold green]🎮 游戏开发Agent已启动 (混合版本)[/bold green]\n\n"
            f"AI服务: {service}\n"
            f"模型: {self.model}\n"
            f"工具总数: {len(self.tools)}个\n\n"
            f"✅ 流式输出: 实时显示\n"
            f"✅ 可靠性: 100%保证",
            title="🤖 Cursor风格编程Agent (Hybrid)"
        ))

    def _create_system_prompt(self) -> str:
        """创建通用的系统提示 - 保持Agentic能力"""
        return """你是一个**游戏开发专家AI Agent**，具备Cursor、Claude、Gemini3 pro这种级别的自主编程能力。

🎯 **核心能力**：
- 自主分析游戏需求，理解要实现的功能
- 自主设计项目结构和文件组织
- 编写完整的、可运行的游戏代码
- 像专业程序员一样工作

📋 **工作流程（ReAct模式）**：

1. **分析与规划** - 理解用户需求，制定实现方案
2. **逐步执行** - 使用工具实现每个部分
3. **测试验证** - 确保代码可运行
4. **总结交付** - 说明完成了什么

**关键**：对于每个步骤，都要经过 Thought（思考）→ Action（使用工具）→ Observation（观察结果）

⚠️ **核心原则**：
1. **必须使用工具执行操作** - 不要直接给出代码，要用工具创建
2. **自主决策** - 根据需求自己决定项目结构、文件组织、工具选择
3. **完整实现** - 确保代码完整可运行，不是空框架
4. **专业标准** - 像专业程序员一样，模块化、可维护、有注释
5. **中文交流** - 所有回复使用中文

🔧 **可用工具**（共24个专业工具）：

**📖 代码分析**（4个）：
- analyze_python_file: 深度分析Python文件结构
- find_function: 查找特定函数代码
- analyze_project: 分析整个项目结构
- search_code: 在项目中搜索代码模式

**✏️ 代码编辑**（5个）：
- write_file: 写入完整文件
- create_game_file: 从模板创建游戏文件
- replace_function: 替换指定函数
- insert_code: 在指定位置插入代码
- read_file: 读取文件内容

**✅ 测试验证**（2个）：
- run_python: 运行Python文件
- check_syntax: 检查语法错误

**💻 终端工具**（1个）：
- run_command: 执行任意终端命令

**🐍 Python环境**（4个）：
- pip_install: 安装Python包
- pip_list: 列出已安装包
- create_requirements: 生成requirements.txt
- check_python_version: 检查Python版本

**📂 Git版本控制**（2个）：
- git_status: 查看Git状态
- git_init: 初始化Git仓库

**🛠️ 基础工具**（7个）：
- calculator: 数学计算
- list_directory: 列出目录内容
- get_current_time: 获取当前时间
- web_search: 网络搜索
- get_webpage: 获取网页内容
- analyze_json: 分析JSON数据

💡 **工作建议**：
- 参考你之前成功创建的游戏（如snake_game、airplane_shooter_game）
- 完整游戏通常需要多个文件和150-300行代码
- 先规划，再执行，最后测试
- 每个文件都要有完整逻辑，不要留空

记住：你是**自主的AI程序员**，像Cursor、Claude、Gemini3 pro这样级别的编程助手，不要僵化地遵循固定模式！
"""

    def run(self, task: str, stream_callback=None) -> dict:
        """
        执行任务 - 混合模式：流式+可靠性保证

        Args:
            task: 任务描述
            stream_callback: 流式回调函数（用于 Web UI）

        Returns:
            dict: 包含 output 和 messages
        """
        try:
            if self.verbose:
                console.print(f"\n[bold blue]🎯 任务:[/bold blue] {task}\n")
                console.print("[bold cyan]" + "="*80 + "[/bold cyan]")
                console.print("[bold cyan]🔄 开始执行[/bold cyan]")
                console.print("[bold cyan]" + "="*80 + "[/bold cyan]\n")

            inputs = {"messages": [{"role": "user", "content": task}]}

            # 🔑 方案1：尝试流式输出（实时体验） - 带超时保护
            all_messages = []
            stream_success = False

            if stream_callback:
                try:
                    if self.verbose:
                        console.print("[dim]🔄 尝试流式模式...[/dim]")

                    stream_callback({
                        "type": "start",
                        "content": task
                    })

                    step_count = 0
                    plan_sent = False
                    seen_message_ids = set()
                    
                    # 🔥 添加超时保护机制
                    STREAM_TIMEOUT = 60  # 60秒总超时
                    EVENT_TIMEOUT = 30   # 30秒事件超时
                    start_time = time.time()
                    last_event_time = time.time()
                    event_count = 0

                    # 使用 stream_mode="updates"
                    for event in self.agent.stream(inputs, stream_mode="updates"):
                        # 🔥 检查超时
                        current_time = time.time()
                        
                        # 总超时检查
                        if current_time - start_time > STREAM_TIMEOUT:
                            if self.verbose:
                                console.print("[yellow]⚠️  流式模式总超时（60秒），切换到标准模式[/yellow]")
                            raise TimeoutError("流式处理总超时")
                        
                        # 事件间隔超时检查
                        if current_time - last_event_time > EVENT_TIMEOUT:
                            if self.verbose:
                                console.print("[yellow]⚠️  流式事件超时（30秒无响应），切换到标准模式[/yellow]")
                            raise TimeoutError("流式事件超时")
                        
                        # 更新最后事件时间
                        last_event_time = current_time
                        event_count += 1
                        
                        for node_name, node_data in event.items():
                            messages = node_data.get("messages", [])

                            for msg in messages:
                                msg_id = id(msg)
                                if msg_id in seen_message_ids:
                                    continue
                                seen_message_ids.add(msg_id)
                                all_messages.append(msg)

                                # 提取任务规划
                                if not plan_sent and hasattr(msg, 'content') and msg.content:
                                    msg_type = type(msg).__name__
                                    if 'AI' in msg_type:
                                        content = msg.content
                                        if any(keyword in content for keyword in ["步骤", "计划", "首先", "然后", "接下来", "我将"]):
                                            stream_callback({
                                                "type": "plan",
                                                "content": content
                                            })
                                            plan_sent = True

                                            if self.verbose:
                                                console.print(Panel(
                                                    f"[blue]{content}[/blue]",
                                                    border_style="blue",
                                                    title="📋 执行计划"
                                                ))

                                # 检测工具调用
                                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                                    for tool_call in msg.tool_calls:
                                        step_count += 1
                                        tool_name = tool_call.get('name', 'unknown')
                                        tool_args = tool_call.get('args', {})

                                        stream_callback({
                                            "type": "action",
                                            "step": step_count,
                                            "tool": tool_name,
                                            "args": tool_args,
                                            "content": f"步骤 {step_count}: {tool_name}"
                                        })

                                        if self.verbose:
                                            console.print(f"[bold yellow]▼ 步骤 {step_count}: {tool_name} ▼[/bold yellow]")

                                # 检测工具响应
                                elif hasattr(msg, 'name') and msg.name:
                                    content = msg.content if hasattr(msg, 'content') else str(msg)
                                    display_content = content[:500] + "..." if len(content) > 500 else content

                                    stream_callback({
                                        "type": "observation",
                                        "step": step_count,
                                        "tool": msg.name,
                                        "result": display_content,
                                        "content": f"✅ 结果: {display_content}"
                                    })

                                    if self.verbose:
                                        console.print(Panel(
                                            f"[green]✅ {msg.name}\n{display_content}[/green]",
                                            border_style="green"
                                        ))

                    stream_success = True
                    if self.verbose:
                        console.print(f"[dim]✅ 流式模式成功（处理了{event_count}个事件）[/dim]\n")

                except TimeoutError as timeout_error:
                    if self.verbose:
                        console.print(f"[yellow]⚠️  {timeout_error}[/yellow]")
                        console.print("[dim]🔄 自动切换到标准模式...[/dim]")

                    if stream_callback:
                        stream_callback({
                            "type": "warning",
                            "content": f"{timeout_error}，自动切换到标准模式..."
                        })
                    
                    stream_success = False

                except Exception as stream_error:
                    if self.verbose:
                        console.print(f"[yellow]⚠️  流式模式失败: {stream_error}[/yellow]")
                        console.print("[dim]🔄 切换到标准模式...[/dim]")

                    if stream_callback:
                        stream_callback({
                            "type": "warning",
                            "content": "流式模式不可用，使用标准模式..."
                        })
                    
                    stream_success = False

            # 🔑 方案2：如果流式失败或没有回调，使用标准模式（100%可靠）
            if not stream_success or not stream_callback:
                if self.verbose:
                    console.print("[dim]📡 使用标准模式执行...[/dim]")
                
                try:
                    response = self.agent.invoke(inputs)
                    all_messages = response.get("messages", [])

                    if self.verbose:
                        console.print("[dim]✅ 标准模式完成[/dim]\n")
                    
                    if stream_callback:
                        stream_callback({
                            "type": "info",
                            "content": "使用标准模式完成任务"
                        })
                        
                except Exception as invoke_error:
                    if self.verbose:
                        console.print(f"[red]❌ 标准模式也失败: {invoke_error}[/red]")
                    
                    raise Exception(f"流式和标准模式都失败: {invoke_error}")

            # 🔑 方案3：手动解析messages（保证100%显示）
            # 无论流式是否成功，都要手动解析一遍来确保完整性
            plan_text = ""
            react_steps = []
            step_num = 0

            # 第一遍：查找计划
            for msg in all_messages:
                if hasattr(msg, 'content') and msg.content:
                    msg_type = type(msg).__name__
                    if 'AI' in msg_type:
                        content = msg.content
                        if any(keyword in content for keyword in ["步骤", "计划", "首先", "然后", "接下来", "使用", "我将"]):
                            if not plan_text or len(content) > len(plan_text):
                                plan_text = content

            # 第二遍：提取步骤
            for i, msg in enumerate(all_messages):
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        step_num += 1
                        tool = tool_call.get('name', 'unknown')
                        args = tool_call.get('args', {})

                        step_data = {
                            "step": step_num,
                            "tool": tool,
                            "args": args,
                            "observation": ""
                        }

                        # 查找对应的 ToolMessage
                        for j in range(i+1, len(all_messages)):
                            next_msg = all_messages[j]
                            if hasattr(next_msg, 'tool_call_id') and next_msg.tool_call_id == tool_call.get('id'):
                                content = next_msg.content if hasattr(next_msg, 'content') else str(next_msg)
                                step_data["observation"] = content
                                break

                        react_steps.append(step_data)

            # 提取最终答案
            output = "未能获取响应"
            if all_messages:
                for msg in reversed(all_messages):
                    if hasattr(msg, 'content') and msg.content:
                        msg_type = type(msg).__name__
                        if 'AI' in msg_type and not (hasattr(msg, 'tool_calls') and msg.tool_calls):
                            if msg.content != plan_text:  # 排除计划文本
                                output = msg.content
                                break

            if output == "未能获取响应" and react_steps:
                output = f"任务已执行完成。共执行了 {len(react_steps)} 个步骤。"

            if self.verbose:
                console.print("[bold green]" + "="*80 + "[/bold green]")
                console.print("[bold green]✅ 任务完成[/bold green]")
                console.print(Panel(output, border_style="green", padding=(1, 2)))
                console.print(f"[dim]📊 计划: {'有' if plan_text else '无'} | 步骤: {len(react_steps)}个[/dim]")

            if stream_callback:
                stream_callback({
                    "type": "final",
                    "content": output,
                    "plan": plan_text,
                    "steps": react_steps
                })

            return {
                "output": output,
                "messages": all_messages,
                "plan": plan_text,
                "react_steps": react_steps
            }

        except Exception as e:
            error_msg = f"执行错误: {str(e)}"
            console.print(f"\n[bold red]❌ {error_msg}[/bold red]")

            if stream_callback:
                stream_callback({
                    "type": "error",
                    "content": error_msg
                })

            return {"error": error_msg, "output": error_msg, "messages": []}

    def chat(self):
        """交互式对话模式"""
        console.print("\n[bold cyan]💬 游戏开发模式[/bold cyan]")
        console.print("[dim]输入 'exit' 或 'quit' 退出[/dim]\n")

        while True:
            try:
                user_input = console.input("[bold yellow]👤 你:[/bold yellow] ")

                if user_input.lower() in ['exit', 'quit', '退出']:
                    console.print("\n[bold]👋 再见！[/bold]")
                    break

                if not user_input.strip():
                    continue

                self.run(user_input)

            except KeyboardInterrupt:
                console.print("\n\n[bold]👋 再见！[/bold]")
                break
            except Exception as e:
                console.print(f"\n[bold red]错误: {str(e)}[/bold red]\n")


def main():
    """主函数"""
    import sys

    service = os.getenv("AI_SERVICE", "deepseek")

    try:
        agent = GameDevAgent(
            temperature=float(os.getenv("TEMPERATURE", 0)),
            verbose=os.getenv("VERBOSE", "true").lower() == "true",
            service=service
        )
    except ValueError as e:
        console.print(f"[bold red]初始化错误: {e}[/bold red]")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--task":
        if len(sys.argv) > 2:
            task = " ".join(sys.argv[2:])
            agent.run(task)
        else:
            console.print("[red]错误: --task 需要提供任务描述[/red]")
    else:
        agent.chat()


if __name__ == "__main__":
    main()
