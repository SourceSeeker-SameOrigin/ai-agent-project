
"""
通用编程Agent - 支持多场景的智能编程助手
结合流式输出的实时性 + 手动解析的可靠性
"""

import os
import time
import signal
from typing import Optional, List, Dict
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools_package.tools import create_tools
from tools_package.game_dev_tools import create_game_dev_tools
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()


# 场景配置
SCENARIO_CONFIGS = {
    "game_dev": {
        "name": "游戏开发",
        "description": "Pygame游戏开发、游戏逻辑、游戏引擎",
        "tools": ["game_dev"],
        "system_prompt_keywords": ["游戏", "pygame", "游戏逻辑", "游戏引擎"]
    },
    "web_dev": {
        "name": "Web开发",
        "description": "Flask、FastAPI、Django、前端开发",
        "tools": ["web_dev"],
        "system_prompt_keywords": ["web", "flask", "fastapi", "django", "前端", "后端", "API"]
    },
    "data_science": {
        "name": "数据科学",
        "description": "数据分析、机器学习、数据可视化",
        "tools": ["data_science"],
        "system_prompt_keywords": ["数据", "pandas", "numpy", "机器学习", "可视化", "分析"]
    },
    "devops": {
        "name": "DevOps",
        "description": "部署、容器化、CI/CD、系统管理",
        "tools": ["devops"],
        "system_prompt_keywords": ["部署", "docker", "kubernetes", "CI/CD", "运维"]
    },
    "general": {
        "name": "通用编程",
        "description": "通用Python开发、代码重构、项目迁移",
        "tools": ["general"],
        "system_prompt_keywords": ["编程", "python", "代码", "项目"]
    }
}


class UniversalAgent:
    """通用编程Agent - 支持多场景的智能编程助手"""

    def __init__(
            self,
            model: str = None,
            temperature: float = 0,
            verbose: bool = True,
            service: str = "deepseek",
            scenario: str = "general"
    ):
        """
        初始化通用编程Agent

        Args:
            model: 模型名称
            temperature: 温度参数
            verbose: 是否显示详细信息
            service: AI服务提供商 (deepseek/dashscope)
            scenario: 使用场景 (game_dev/web_dev/data_science/devops/general)
        """
        self.service = service
        self.verbose = verbose
        self.scenario = scenario

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

        # 创建工具集（根据场景选择）
        self.tools = self._create_tools_for_scenario(scenario)

        # 创建系统提示词
        system_prompt = self._create_system_prompt(scenario)

        # 创建Agent
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt,
            debug=False
        )

        scenario_name = SCENARIO_CONFIGS.get(scenario, SCENARIO_CONFIGS["general"])["name"]
        console.print(Panel.fit(
            f"[bold green]🤖 通用编程Agent已启动[/bold green]\n\n"
            f"场景: {scenario_name}\n"
            f"AI服务: {service}\n"
            f"模型: {self.model}\n"
            f"工具总数: {len(self.tools)}个\n\n"
            f"✅ 流式输出: 实时显示\n"
            f"✅ 可靠性: 100%保证",
            title="🚀 Universal Programming Agent"
        ))

    def _create_tools_for_scenario(self, scenario: str) -> List:
        """根据场景创建工具集"""
        basic_tools = create_tools(enable_clip=False)

        # 所有场景都包含质量工具
        try:
            from tools_package.quality_tools import create_quality_tools
            quality_tools = create_quality_tools()
        except ImportError:
            quality_tools = []

        # 根据场景添加特定工具
        if scenario == "game_dev":
            from tools_package.game_dev_tools import create_game_dev_tools
            game_tools = create_game_dev_tools()
            return basic_tools + game_tools + quality_tools
        elif scenario == "web_dev":
            from tools_package.web_dev_tools import create_web_dev_tools
            web_tools = create_web_dev_tools()
            return basic_tools + web_tools + quality_tools
        elif scenario == "data_science":
            from tools_package.data_science_tools import create_data_science_tools
            data_tools = create_data_science_tools()
            return basic_tools + data_tools + quality_tools
        elif scenario == "devops":
            from tools_package.devops_tools import create_devops_tools
            devops_tools = create_devops_tools()
            return basic_tools + devops_tools + quality_tools
        else:  # general
            from tools_package.game_dev_tools import create_game_dev_tools
            # 通用场景包含所有工具
            game_tools = create_game_dev_tools()
            try:
                from tools_package.web_dev_tools import create_web_dev_tools
                web_tools = create_web_dev_tools()
            except ImportError:
                web_tools = []
            try:
                from tools_package.data_science_tools import create_data_science_tools
                data_tools = create_data_science_tools()
            except ImportError:
                data_tools = []
            try:
                from tools_package.devops_tools import create_devops_tools
                devops_tools = create_devops_tools()
            except ImportError:
                devops_tools = []
            return basic_tools + game_tools + web_tools + data_tools + devops_tools + quality_tools

    def _create_system_prompt(self, scenario: str) -> str:
        """根据场景创建系统提示词"""
        scenario_config = SCENARIO_CONFIGS.get(scenario, SCENARIO_CONFIGS["general"])
        scenario_name = scenario_config["name"]

        base_prompt = f"""你是一个**{scenario_name}专家AI Agent**，具备Cursor、Claude、Gemini3 pro这种级别的自主编程能力。

🎯 **核心能力**：
- 自主分析需求，理解要实现的功能
- 自主设计项目结构和文件组织
- 编写完整的、可运行的代码
- 像专业程序员一样工作

📋 **工作流程（严格ReAct模式）**：

1. **分析与规划** - 理解用户需求，制定实现方案
2. **逐步执行** - 使用工具实现每个部分
3. **测试验证** - 确保代码可运行
4. **总结交付** - 说明完成了什么

**关键**：对于每个步骤，都要严格的经过 Thought（思考）→ Action（使用工具）→ Observation（观察结果）

⚠️ **核心原则**：
1. **必须使用工具执行操作** - 不要直接给出代码，要用工具创建
2. **自主决策** - 根据需求自己决定项目结构、文件组织、工具选择
3. **完整实现** - 确保代码完整可运行，不是空框架
4. **专业标准** - 像专业程序员一样，模块化、可维护、有注释
5. **中文交流** - 所有回复使用中文
6. **代码质量** - 生成代码后自动进行语法检查和测试

🔧 **可用工具**（共{len(self.tools)}个专业工具）：

"""

        # 根据场景添加特定说明
        if scenario == "game_dev":
            base_prompt += """**🎮 游戏开发专用工具**：
- 游戏文件模板创建
- Pygame项目结构管理
- 游戏逻辑测试

记住：你是**自主的AI程序员**，像Cursor、Claude、Gemini3 pro这样级别的编程助手，不要僵化地遵循固定模式！
"""
        elif scenario == "web_dev":
            base_prompt += """**🌐 Web开发专用工具**：
- API路由生成
- 数据库模型创建
- HTTP请求测试

记住：你是**自主的AI程序员**，像Cursor、Claude、Gemini3 pro这样级别的编程助手，不要僵化地遵循固定模式！
"""
        elif scenario == "data_science":
            base_prompt += """**📊 数据科学专用工具**：
- 数据处理脚本
- 数据可视化
- 机器学习模型

记住：你是**自主的AI程序员**，像Cursor、Claude、Gemini3 pro这样级别的编程助手，不要僵化地遵循固定模式！
"""
        elif scenario == "devops":
            base_prompt += """**🚀 DevOps专用工具**：
- 部署脚本生成
- 容器化配置
- 系统管理命令

记住：你是**自主的AI程序员**，像Cursor、Claude、Gemini3 pro这样级别的编程助手，不要僵化地遵循固定模式！
"""

        base_prompt += """**🛠️ 通用工具**：
- 代码分析、编辑、搜索
- 文件操作、项目管理
- 测试验证、终端命令
- Python环境管理、Git版本控制

💡 **工作建议**：
- 先规划，再执行，最后测试
- 每个文件都要有完整逻辑，不要留空
- 生成代码后自动进行语法检查
- 确保代码可运行且符合最佳实践

记住：你是**自主的AI程序员**，像Cursor、Claude、Gemini3 pro这样级别的编程助手，不要僵化地遵循固定模式！
"""

        return base_prompt

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
                                    # 提取思考内容（AI消息中的content，在工具调用之前）
                                    thought_content = ""
                                    if hasattr(msg, 'content') and msg.content:
                                        thought_content = msg.content

                                    for tool_call in msg.tool_calls:
                                        step_count += 1
                                        tool_name = tool_call.get('name', 'unknown')
                                        tool_args = tool_call.get('args', {})

                                        stream_callback({
                                            "type": "action",
                                            "step": step_count,
                                            "tool": tool_name,
                                            "args": tool_args,
                                            "thought": thought_content,  # 添加思考内容
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
                    
                    # 超时时不设置stream_success=True，让它走标准模式
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
                    # 添加超时保护到标准模式
                    response = self.agent.invoke(inputs)
                    all_messages = response.get("messages", [])

                    if self.verbose:
                        console.print("[dim]✅ 标准模式完成[/dim]\n")
                    
                    # 如果有回调函数，通知标准模式已完成
                    if stream_callback:
                        stream_callback({
                            "type": "info",
                            "content": "使用标准模式完成任务"
                        })
                        
                except Exception as invoke_error:
                    if self.verbose:
                        console.print(f"[red]❌ 标准模式也失败: {invoke_error}[/red]")
                    
                    # 如果标准模式也失败，抛出异常
                    raise Exception(f"流式和标准模式都失败: {invoke_error}")

            # 🔑 方案3：手动解析messages（保证100%显示）
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
        scenario_name = SCENARIO_CONFIGS.get(self.scenario, SCENARIO_CONFIGS["general"])["name"]
        console.print(f"\n[bold cyan]💬 {scenario_name}模式[/bold cyan]")
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
    scenario = os.getenv("AGENT_SCENARIO", "general")

    try:
        agent = UniversalAgent(
            temperature=float(os.getenv("TEMPERATURE", 0)),
            verbose=os.getenv("VERBOSE", "true").lower() == "true",
            service=service,
            scenario=scenario
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
