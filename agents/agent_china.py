"""
AI Agent 主程序 - 中国版
支持国内 AI 服务（阿里通义千问、百度文心一言等）
"""

import os
from typing import Optional
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools_package.tools import create_tools
from rich.console import Console
from rich.panel import Panel

# 加载环境变量
load_dotenv()

console = Console()


class AIAgentChina:
    """AI Agent 类 - 支持国内服务"""
    
    def __init__(
        self,
            model: str = None,
            temperature: float = 0,
            max_iterations: int = None,
            verbose: bool = True,
            service: str = "dashscope",  # dashscope(阿里), wenxin(百度), zhipu(智谱)
            enable_clip: bool = False  # 🆕 是否启用CLIP图像分析功能
    ):
        """
        初始化AI Agent
        
        Args:
            model: 模型名称
            temperature: 温度参数，控制输出随机性（0-1）
            max_iterations: 最大迭代次数（None=无限制）
            verbose: 是否显示详细日志
            service: AI 服务提供商
            enable_clip: 是否启用CLIP图像分析功能
        """
        self.service = service
        
        # 根据服务类型配置
        if service == "dashscope":
            # 阿里通义千问
            api_key = os.getenv("DASHSCOPE_API_KEY")
            if not api_key:
                raise ValueError(
                    "未找到 DASHSCOPE_API_KEY！\n"
                    "请在 .env 文件中添加：\n"
                    "DASHSCOPE_API_KEY=sk-your-api-key\n\n"
                    "获取地址: https://dashscope.aliyun.com/"
                )
            
            self.model = model or os.getenv("DASHSCOPE_MODEL", "qwen-turbo")
            base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
            
        elif service == "wenxin":
            # 百度文心一言
            api_key = os.getenv("WENXIN_API_KEY")
            if not api_key:
                raise ValueError(
                    "未找到 WENXIN_API_KEY！\n"
                    "请在 .env 文件中添加：\n"
                    "WENXIN_API_KEY=your-api-key\n\n"
                    "获取地址: https://console.bce.baidu.com/qianfan/"
                )
            
            self.model = model or os.getenv("WENXIN_MODEL", "ERNIE-Bot-turbo")
            base_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop"
            
        elif service == "zhipu":
            # 智谱 ChatGLM
            api_key = os.getenv("ZHIPU_API_KEY")
            if not api_key:
                raise ValueError(
                    "未找到 ZHIPU_API_KEY！\n"
                    "请在 .env 文件中添加：\n"
                    "ZHIPU_API_KEY=your-api-key\n\n"
                    "获取地址: https://open.bigmodel.cn/"
                )
            
            self.model = model or os.getenv("ZHIPU_MODEL", "glm-4")
            base_url = "https://open.bigmodel.cn/api/paas/v4/"
            
        elif service == "deepseek":
            # DeepSeek
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                raise ValueError(
                    "未找到 DEEPSEEK_API_KEY！\n"
                    "请在 .env 文件中添加：\n"
                    "DEEPSEEK_API_KEY=your-api-key\n\n"
                    "获取地址: https://platform.deepseek.com/"
                )
            
            self.model = model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
            base_url = "https://api.deepseek.com/v1"
            
        else:
            raise ValueError(f"不支持的服务: {service}")
        
        # 初始化 LLM（使用 OpenAI 兼容接口）
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            api_key=api_key,
            base_url=base_url
        )
        
        # 创建工具（根据参数决定是否启用CLIP）
        self.tools = create_tools(enable_clip=enable_clip)
        
        # 创建系统提示
        system_prompt = self._create_system_prompt()
        
        # 使用新的 create_agent API（无迭代次数限制）
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt,
            debug=False  # 关闭调试模式，避免控制台输出 [values]/[updates]
        )
        # 注意：LangChain 的 create_agent 默认就没有迭代限制
        # Agent 会根据任务完成情况自动决定何时停止
        
        self.verbose = verbose
        self.max_iterations = max_iterations if max_iterations else None  # 无限制，由任务完成情况决定
        
        service_names = {
            "dashscope": "阿里通义千问",
            "wenxin": "百度文心一言",
            "zhipu": "智谱ChatGLM",
            "deepseek": "DeepSeek"
        }
        
        console.print(Panel.fit(
            f"[bold green]🤖 AI Agent 已启动 (中国版)[/bold green]\n\n"
            f"AI 服务: {service_names.get(service, service)}\n"
            f"模型: {self.model}\n"
            f"可用工具数: {len(self.tools)}",
            title="系统信息"
        ))
    
    def _create_system_prompt(self) -> str:
        """创建系统提示"""
        return """你是一个强大的 AI Agent，采用 ReAct 模式（Reasoning + Acting）工作。

⚠️ **重要规则**：
- 你**必须使用工具**来完成任务，不能直接给出答案
- 即使任务看起来简单，也要使用相应的工具来执行
- 每个步骤都要明确调用工具，展示完整的 ReAct 过程（思考→行动→观察）

📋 工作流程（必须严格遵循）：

**第一步：任务规划（必须先输出计划）**
收到任务后，你必须首先输出一个清晰的执行计划：
1. 📝 分析任务需求
2. 🎯 列出需要执行的步骤（编号列表）
3. 🔧 说明每一步使用的工具

格式示例：
```
我将按以下步骤完成任务：
1. 使用 calculator 工具计算 100 的平方根
2. 使用 write_file 工具将结果保存到 result.txt 文件

现在开始执行...
```

**第二步：逐步执行（ReAct 循环）**
对于每个步骤：
1. 💭 Thought（思考）：思考当前需要做什么
2. 🎬 Action（行动）：调用相应工具执行操作
3. 👁️ Observation（观察）：分析工具返回的结果
4. 🔄 继续下一步，直到完成所有步骤

**第三步：总结**
- ✅ 汇总所有步骤的结果
- 📝 给出清晰的最终答案

🔧 可用工具：
- calculator: 数学计算（输入：数学表达式，如 "sqrt(100)" 或 "2+2"）
- write_file: 写入文件（输入格式：文件路径|||文件内容，用|||分隔，如 "result.txt|||10"）
- read_file: 读取文件（输入：文件路径）
- list_directory: 列出目录（输入：目录路径，默认 "."）
- get_current_time: 获取当前时间（输入：空字符串或任意文本）
- web_search: 网络搜索（输入：搜索关键词）
- get_webpage: 获取网页内容（输入：URL）
- analyze_json: 分析JSON数据（输入：JSON字符串）

⚠️ 重要规则：
1. **必须先输出计划，再执行步骤**
2. 计划要清晰、具体、可执行
3. 每个步骤只做一件事
4. 如果某步失败，调整策略继续
5. 所有回复使用中文
6. 最后给出友好、清晰的总结

💡 完整示例：

用户：计算 100 的平方根，然后保存到 result.txt 文件

你的完整回应：
"我将按以下步骤完成任务：
1. 使用 calculator 工具计算 sqrt(100)
2. 使用 write_file 工具将结果保存到 result.txt 文件

现在开始执行..."

[然后调用 calculator 工具]
[观察结果: 10.0]
[然后调用 write_file 工具]
[观察结果: 文件已保存]

"任务完成！100 的平方根是 10.0，已成功保存到 result.txt 文件。"
"""
    
    def run(self, task: str, stream_callback=None) -> dict:
        """执行任务"""
        try:
            if self.verbose:
                console.print(f"\n[bold blue]🎯 任务:[/bold blue] {task}\n")
                console.print("[bold cyan]" + "="*80 + "[/bold cyan]")
                console.print("[bold cyan]🔄 开始 ReAct 循环（思考→行动→观察）[/bold cyan]")
                console.print("[bold cyan]" + "="*80 + "[/bold cyan]\n")
            
            # 发送任务开始信号
            if stream_callback:
                stream_callback({
                    "type": "start",
                    "content": task
                })
            
            # 首先让 LLM 分析任务并制定计划（可选，如果需要显示计划）
            if stream_callback:
                # 发送一个简单的计划提示
                # 实际的计划会在 LLM 第一次响应时提取
                stream_callback({
                    "type": "plan",
                    "content": "正在分析任务并制定执行计划..."
                })
            
            # langchain 1.2.x 使用新的消息格式
            inputs = {"messages": [{"role": "user", "content": task}]}
            
            # 使用 stream 方法实现流式输出
            all_messages = []
            step_count = 0
            plan_sent = False  # 标记是否已发送计划
            
            if stream_callback:
                # 流式执行 - 添加错误处理
                try:
                    # 尝试使用 stream 方法
                    for chunk in self.agent.stream(inputs):
                        messages = chunk.get("messages", [])
                        
                        for msg in messages:
                            # 避免重复添加
                            if msg not in all_messages:
                                all_messages.append(msg)
                            
                            # 提取任务规划（从第一个 AIMessage 中）
                            if not plan_sent and hasattr(msg, 'content') and msg.content:
                                msg_type = type(msg).__name__
                                if 'AI' in msg_type:
                                    # 尝试提取规划信息
                                    content = msg.content
                                    # 如果内容包含规划相关的关键词
                                    if any(keyword in content for keyword in ["步骤", "计划", "首先", "然后", "接下来"]):
                                        stream_callback({
                                            "type": "plan",
                                            "content": content
                                        })
                                        plan_sent = True
                                        
                                        if self.verbose:
                                            console.print(Panel(
                                                f"[blue]{content}[/blue]",
                                                border_style="blue",
                                                title="📋 任务规划"
                                            ))
                                            console.print()
                            
                            # 检测工具调用（Action）
                            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                                for tool_call in msg.tool_calls:
                                    step_count += 1
                                    
                                    # 实时发送思考和行动信息
                                    stream_callback({
                                        "type": "action",
                                        "step": step_count,
                                        "tool": tool_call.get('name', 'unknown'),
                                        "args": tool_call.get('args', {}),
                                        "content": f"**第 {step_count} 轮迭代**\n\n"
                                                  f"💭 **Thought**: 需要使用工具来完成任务\n\n"
                                                  f"🎬 **Action**: 调用工具 `{tool_call.get('name', 'unknown')}`\n\n"
                                                  f"```json\n{tool_call.get('args', {})}\n```\n"
                                    })
                                    
                                    if self.verbose:
                                        console.print(f"[bold yellow]▼ 第 {step_count} 轮迭代 ▼[/bold yellow]")
                                        console.print(Panel(
                                            f"[cyan]🎬 Action: 调用 [bold]{tool_call.get('name', 'unknown')}[/bold]\n"
                                            f"📝 输入: {tool_call.get('args', {})}[/cyan]",
                                            border_style="cyan",
                                            title="行动"
                                        ))
                            
                            # 检测工具响应（Observation）
                            elif hasattr(msg, 'name') and msg.name:
                                content = msg.content if hasattr(msg, 'content') else str(msg)
                                display_content = content[:300] + "..." if len(content) > 300 else content
                                
                                # 实时发送观察结果（包含步骤编号）
                                stream_callback({
                                    "type": "observation",
                                    "step": step_count,  # 当前步骤编号
                                    "tool": msg.name,
                                    "result": display_content,
                                    "content": f"👁️ **Observation**: 工具 `{msg.name}` 返回结果\n\n"
                                              f"```\n{display_content}\n```\n\n"
                                })
                                
                                if self.verbose:
                                    console.print(Panel(
                                        f"[green]👁️ Observation: 工具 [bold]{msg.name}[/bold] 返回\n"
                                        f"📊 结果: {display_content}[/green]",
                                        border_style="green",
                                        title="观察"
                                    ))
                                    console.print()
                    
                    response = {"messages": all_messages}
                    
                except Exception as stream_error:
                    # 如果流式执行失败，回退到普通模式
                    if self.verbose:
                        console.print(f"[yellow]⚠️  流式模式失败，切换到普通模式: {stream_error}[/yellow]")
                    
                    # 发送警告信息
                    stream_callback({
                        "type": "info",
                        "content": "⚠️ 流式模式不可用，使用普通模式执行...\n\n"
                    })
                    
                    # 使用普通模式执行
                    response = self.agent.invoke(inputs)
                    all_messages = response.get("messages", [])
                    
                    # 手动解析并发送步骤信息
                    step_count = 0
                    plan_sent = False
                    
                    for msg in all_messages:
                        # 提取任务规划
                        if not plan_sent and hasattr(msg, 'content') and msg.content:
                            msg_type = type(msg).__name__
                            if 'AI' in msg_type:
                                content = msg.content
                                if any(keyword in content for keyword in ["步骤", "计划", "首先", "然后", "接下来"]):
                                    stream_callback({
                                        "type": "plan",
                                        "content": content
                                    })
                                    plan_sent = True
                        
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                step_count += 1
                                stream_callback({
                                    "type": "action",
                                    "step": step_count,
                                    "tool": tool_call.get('name', 'unknown'),
                                    "args": tool_call.get('args', {}),
                                    "content": f"**第 {step_count} 轮迭代**\n\n"
                                              f"💭 **Thought**: 需要使用工具来完成任务\n\n"
                                              f"🎬 **Action**: 调用工具 `{tool_call.get('name', 'unknown')}`\n\n"
                                              f"```json\n{tool_call.get('args', {})}\n```\n"
                                })
                        
                        elif hasattr(msg, 'name') and msg.name:
                            content = msg.content if hasattr(msg, 'content') else str(msg)
                            display_content = content[:300] + "..." if len(content) > 300 else content
                            stream_callback({
                                "type": "observation",
                                "step": step_count,
                                "tool": msg.name,
                                "result": display_content,
                                "content": f"👁️ **Observation**: 工具 `{msg.name}` 返回结果\n\n"
                                          f"```\n{display_content}\n```\n\n"
                            })
            else:
                # 非流式执行（原有逻辑）
                response = self.agent.invoke(inputs)
            
            # 提取消息
            if stream_callback and all_messages:
                messages = all_messages
            else:
                messages = response.get("messages", [])
                
                # 如果启用 verbose 且没有使用流式输出，显示详细的执行过程
                if self.verbose and messages:
                    step_count = 0
                    console.print("[bold magenta]📋 执行步骤详情:[/bold magenta]\n")
                    
                    for i, msg in enumerate(messages):
                        # 检测工具调用（Action）
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                step_count += 1
                                console.print(f"[bold yellow]▼ 第 {step_count} 轮迭代 ▼[/bold yellow]")
                                console.print(Panel(
                                    f"[cyan]💭 Thought: Agent 决定使用工具\n"
                                    f"🎬 Action: 调用 [bold]{tool_call.get('name', 'unknown')}[/bold]\n"
                                    f"📝 输入: {tool_call.get('args', {})}[/cyan]",
                                    border_style="cyan",
                                    title="思考与行动"
                                ))
                        
                        # 检测工具响应（Observation）
                        elif hasattr(msg, 'name') and msg.name:
                            content = msg.content if hasattr(msg, 'content') else str(msg)
                            # 限制显示长度
                            if len(content) > 300:
                                content = content[:300] + "...(已截断)"
                            
                            console.print(Panel(
                                f"[green]👁️  Observation: 工具 [bold]{msg.name}[/bold] 返回结果\n"
                                f"📊 结果: {content}[/green]",
                                border_style="green",
                                title="观察结果"
                            ))
                            console.print()
                    
                    if step_count == 0:
                        console.print("[dim]💡 此任务无需使用工具，直接完成[/dim]\n")
            
            # 提取输出 - 找到最后一个 AIMessage
            output = "未能获取响应"
            if messages:
                # 从后向前找最后一个 AIMessage
                for msg in reversed(messages):
                    if hasattr(msg, 'content') and msg.content:
                        # 检查是否是 AIMessage（不是 ToolMessage）
                        msg_type = type(msg).__name__
                        if 'AI' in msg_type and not hasattr(msg, 'tool_calls'):
                            output = msg.content
                            break
                        elif 'AI' in msg_type and hasattr(msg, 'tool_calls') and not msg.tool_calls:
                            # AIMessage 但没有 tool_calls，说明是最终答案
                            output = msg.content
                            break
                
                # 如果还是没有找到，使用最后一条消息
                if output == "未能获取响应" and messages:
                    last_msg = messages[-1]
                    if hasattr(last_msg, 'content'):
                        output = last_msg.content
            
            if self.verbose:
                console.print("[bold green]" + "="*80 + "[/bold green]")
                console.print("[bold green]✅ 最终答案:[/bold green]")
                console.print(Panel(output, border_style="green", padding=(1, 2)))
            
            # 发送最终答案
            if stream_callback:
                stream_callback({
                    "type": "final",
                    "content": output
                })
            
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
    
    def list_tools(self):
        """列出所有可用工具"""
        console.print("\n[bold cyan]🔧 可用工具列表:[/bold cyan]\n")
        
        for i, tool in enumerate(self.tools, 1):
            console.print(f"[bold]{i}. {tool.name}[/bold]")
            console.print(f"   {tool.description}\n")


def main():
    """主函数"""
    import sys
    
    # 选择服务
    service = os.getenv("AI_SERVICE", "dashscope")
    
    # 创建Agent
    try:
        agent = AIAgentChina(
            temperature=float(os.getenv("TEMPERATURE", 0)),
            max_iterations=int(os.getenv("MAX_ITERATIONS", 10)),
            verbose=os.getenv("VERBOSE", "true").lower() == "true",
            service=service
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
            console.print("  python agent_china.py              # 进入对话模式")
            console.print("  python agent_china.py --tools      # 列出所有工具")
            console.print("  python agent_china.py --task <任务> # 执行单个任务")
    else:
        # 默认进入对话模式
        agent.chat()


if __name__ == "__main__":
    main()

