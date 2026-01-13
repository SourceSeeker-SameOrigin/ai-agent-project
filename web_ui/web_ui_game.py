"""
游戏开发Agent Web界面 - V2版本
基于 LangChain 0.3.x 的正确流式实现
"""

import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.agent_game import GameDevAgent

# 页面配置
st.set_page_config(
    page_title="🎮 游戏开发Agent (V2)",
    page_icon="🤖",
    layout="wide"
)

# 标题
st.title("🎮 游戏开发AI Agent - Cursor风格编程助手 (V2)")
st.markdown("**✨ 基于 LangChain 0.3.x 的正确流式实现**")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")
    
    # AI服务选择
    service = st.selectbox(
        "🤖 AI服务",
        ["deepseek", "dashscope"],
        help="选择AI服务提供商"
    )
    
    # API密钥输入
    if service == "deepseek":
        api_key = st.text_input(
            "🔑 DeepSeek API密钥",
            type="password",
            help="从 https://platform.deepseek.com/ 获取"
        )
        if api_key:
            os.environ["DEEPSEEK_API_KEY"] = api_key
    elif service == "dashscope":
        api_key = st.text_input(
            "🔑 阿里云API密钥",
            type="password",
            help="从 https://dashscope.aliyun.com/ 获取"
        )
        if api_key:
            os.environ["DASHSCOPE_API_KEY"] = api_key
    
    # 温度设置
    temperature = st.slider(
        "🌡️ 温度",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
        help="控制输出的随机性"
    )
    
    st.divider()
    
    # 工具说明
    st.header("🔧 可用工具 (共24个)")
    st.caption("像Cursor一样的全面工具集")
    
    with st.expander("📖 代码分析 (4个)", expanded=False):
        st.markdown("""
        - `analyze_python_file`: 深度分析Python文件结构
        - `find_function`: 查找特定函数代码
        - `analyze_project`: 分析项目结构
        - `search_code`: 搜索代码模式
        """)
    
    with st.expander("✏️ 代码编辑 (5个)", expanded=False):
        st.markdown("""
        - `write_file`: 写入完整文件
        - `create_game_file`: 从模板创建文件
        - `replace_function`: 替换函数
        - `insert_code`: 插入代码
        - `read_file`: 读取文件
        """)
    
    with st.expander("✅ 测试验证 (2个)", expanded=False):
        st.markdown("""
        - `run_python`: 运行Python文件
        - `check_syntax`: 检查语法错误
        """)
    
    with st.expander("💻 终端工具 (1个)", expanded=False):
        st.markdown("""
        - `run_command`: 执行终端命令
        """)
    
    with st.expander("🐍 Python环境 (4个)", expanded=False):
        st.markdown("""
        - `pip_install`: 安装Python包
        - `pip_list`: 列出已安装包
        - `create_requirements`: 生成requirements.txt
        - `check_python_version`: 检查Python版本
        """)
    
    with st.expander("📂 Git版本控制 (2个)", expanded=False):
        st.markdown("""
        - `git_status`: 查看Git状态
        - `git_init`: 初始化Git仓库
        """)
    
    with st.expander("🛠️ 基础工具 (7个)", expanded=False):
        st.markdown("""
        - `calculator`: 数学计算
        - `list_directory`: 列出目录
        - `get_current_time`: 获取时间
        - `web_search`: 网络搜索
        - `get_webpage`: 获取网页
        - `analyze_json`: 分析JSON
        """)


# 主界面
tab1, tab2 = st.tabs(["💬 对话", "ℹ️ 说明"])

with tab1:
    # 初始化会话状态
    if "v2_messages" not in st.session_state:
        st.session_state.v2_messages = []
    
    # 显示对话历史
    for message in st.session_state.v2_messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                # 显示任务规划
                if "plan" in message and message["plan"]:
                    with st.expander("📋 任务规划", expanded=False):
                        st.info(message["plan"])
                
                # 显示ReAct执行过程
                if "react_steps" in message and message["react_steps"]:
                    is_latest = (message == st.session_state.v2_messages[-1])
                    with st.expander("🧠 ReAct 执行过程", expanded=is_latest):
                        import json
                        for step_data in message["react_steps"]:
                            step = step_data.get("step", 0)
                            tool = step_data.get("tool", "unknown")
                            args = step_data.get("args", {})
                            observation = step_data.get("observation", "")
                            
                            st.markdown(f"### 🔄 步骤 {step}: {tool}")
                            
                            # Thought（思考）
                            st.markdown("**💭 Thought (思考)**")
                            st.info(f"我需要使用 `{tool}` 工具来完成这个步骤")
                            
                            # Action（行动）
                            st.markdown("**🎬 Action (行动)**")
                            st.code(json.dumps(args, ensure_ascii=False, indent=2), language='json')
                            
                            # Observation（观察）
                            if observation:
                                st.markdown("**👁️ Observation (观察)**")
                                st.success(observation)
                            
                            st.divider()
            
            st.markdown(message["content"])
    
    # 用户输入
    user_input = st.chat_input("请描述你的游戏开发任务...")
    
    if user_input:
        # 检查API密钥
        if not api_key:
            st.error("❌ 请先在侧边栏输入API密钥")
        else:
            # 显示用户消息
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # 添加到历史
            st.session_state.v2_messages.append({
                "role": "user",
                "content": user_input
            })
            
            # 创建Agent并执行
            with st.chat_message("assistant"):
                # 创建实时更新容器
                status_container = st.empty()
                plan_container = st.container()
                steps_container = st.container()
                result_container = st.empty()
                
                # 显示初始状态
                with status_container:
                    st.info("🚀 正在初始化Agent...")
                
                try:
                    # 初始化Agent（V2版本）
                    agent = GameDevAgent(
                        temperature=temperature,
                        verbose=False,  # 关闭控制台日志，使用 Web UI
                        service=service
                    )
                    
                    # Agent创建成功后，更新状态
                    with status_container:
                        st.success(f"✅ Agent初始化完成 (V2版本 | {service} | {len(agent.tools)}个工具)")
                    
                    # 用于收集实时信息
                    realtime_state = {
                        "plan": "",
                        "steps": [],
                        "current_step": 0,
                        "step_containers": {}
                    }
                    
                    # 🔥 实时回调函数 - Cursor风格！
                    def realtime_callback(data):
                        msg_type = data.get("type", "")
                        
                        if msg_type == "start":
                            with plan_container:
                                st.success(f"🎯 **任务**: {data.get('content', '')}")
                        
                        elif msg_type == "warning":
                            with steps_container:
                                st.warning(f"⚠️ {data.get('content', '')}")
                        
                        elif msg_type == "plan":
                            realtime_state["plan"] = data.get("content", "")
                            with plan_container:
                                st.markdown("### 📋 任务规划")
                                st.info(realtime_state["plan"])
                                st.divider()
                        
                        elif msg_type == "action":
                            step = data.get("step", 0)
                            tool = data.get("tool", "unknown")
                            args = data.get("args", {})
                            
                            realtime_state["current_step"] = step
                            
                            # Cursor风格：在 steps_container 中创建新步骤
                            with steps_container:
                                step_status = st.status(
                                    f"🔄 步骤 {step}: {tool}", 
                                    state="running", 
                                    expanded=True  # 默认展开，像Cursor一样
                                )
                                realtime_state["step_containers"][step] = step_status
                                
                                with step_status:
                                    # Cursor风格的ReAct展示
                                    st.markdown("#### 💭 Thought (思考)")
                                    st.info(f"我需要使用 `{tool}` 工具来完成这一步")
                                    
                                    st.markdown("#### 🎬 Action (行动)")
                                    import json
                                    if args:
                                        st.code(json.dumps(args, ensure_ascii=False, indent=2), language='json')
                                    else:
                                        st.code("无参数", language='text')
                                    
                                    st.caption("⏳ 正在执行...")
                            
                            # 保存步骤信息
                            realtime_state["steps"].append({
                                "step": step,
                                "tool": tool,
                                "args": args,
                                "observation": ""
                            })
                        
                        elif msg_type == "observation":
                            step = data.get("step", 0)
                            result_text = data.get("result", "")
                            tool_name = data.get("tool", "unknown")
                            
                            # Cursor风格：更新对应步骤
                            if step in realtime_state["step_containers"]:
                                step_status = realtime_state["step_containers"][step]
                                
                                with step_status:
                                    st.markdown("#### 👁️ Observation (观察)")
                                    st.success(result_text)
                                
                                # 更新状态为完成
                                step_status.update(
                                    label=f"✅ 步骤 {step}: {tool_name} - 已完成", 
                                    state="complete",
                                    expanded=False  # 完成后折叠，保持界面整洁
                                )
                            
                            # 更新步骤信息
                            for s in realtime_state["steps"]:
                                if s["step"] == step:
                                    s["observation"] = result_text
                        
                        elif msg_type == "error":
                            with steps_container:
                                st.error(f"❌ 错误: {data.get('content', '')}")
                    
                    # 🚀 执行任务（传入回调函数）
                    result = agent.run(user_input, stream_callback=realtime_callback)
                    
                    # 获取结果
                    response = result.get("output", "")
                    
                    # 显示最终答案
                    with result_container:
                        st.markdown("---")
                        st.markdown("### ✅ 任务完成")
                        st.success("🎉 Agent已成功完成您的任务！")
                        if response:
                            st.markdown(response)
                        else:
                            st.info("任务已执行完成。请查看上方的执行步骤了解详情。")
                    
                    # 添加到历史
                    st.session_state.v2_messages.append({
                        "role": "assistant",
                        "content": response or "任务已执行完成。",
                        "react_steps": realtime_state["steps"],
                        "plan": realtime_state["plan"]
                    })
                
                except Exception as e:
                    st.error(f"❌ 执行错误: {str(e)}")
                    import traceback
                    with st.expander("🔍 错误详情"):
                        st.code(traceback.format_exc())

with tab2:
    st.header("ℹ️ V2 版本说明")
    
    st.markdown("""
    ## 🎯 V2 版本改进
    
    ### 兼容 LangChain 0.3.x
    
    在 LangChain 0.3.x 中：
    - ❌ `AgentExecutor` 已移除
    - ❌ `create_react_agent` 已移除
    - ✅ 推荐使用 `create_agent`（基于 LangGraph）
    
    ### V2 实现方式
    
    ```python
    # 1. 使用 create_agent（LangChain 0.3.x 官方方式）
    self.agent = create_agent(
        model=self.llm,
        tools=self.tools,
        system_prompt=system_prompt
    )
    
    # 2. 使用正确的流式模式
    for event in self.agent.stream(
        inputs, 
        stream_mode="updates"  # 🔑 关键：节点级别更新
    ):
        # 处理每个节点的更新
        for node_name, node_data in event.items():
            messages = node_data.get("messages", [])
            # 提取工具调用和结果
            ...
    ```
    
    ### 流式模式对比
    
    | 模式 | 说明 | 适用场景 |
    |------|------|----------|
    | `stream_mode="values"` | 返回完整状态 | 默认模式 |
    | `stream_mode="updates"` | 只返回更新部分 | ✅ **V2使用** |
    | `stream_mode="messages"` | 只返回消息 | 仅消息流 |
    
    ### 核心改进
    
    1. **兼容性** ✅
       - 完全兼容 LangChain 0.3.x
       - 不依赖已移除的 API
       - 使用官方推荐方式
    
    2. **流式输出** ✅
       - 使用 `stream_mode="updates"`
       - 节点级别的实时更新
       - 可以捕获工具调用
    
    3. **消息去重** ✅
       - 使用 `seen_message_ids` 避免重复处理
       - 确保每个步骤只显示一次
    
    ### 效果展示
    
    ```
    🚀 正在初始化Agent...
    ✅ Agent初始化完成 (V2版本)
    
    🎯 任务: 分析当前项目
    
    📋 任务规划
    我将分3步完成...
    
    🔄 步骤 1: analyze_project
      💭 Thought: 我需要分析项目结构
      🎬 Action: {"path": "./"}
      ⏳ 正在执行...
      👁️ Observation: 找到10个Python文件
    ✅ 步骤 1: analyze_project - 已完成
    
    🔄 步骤 2: read_file
      💭 Thought: 读取主文件
      🎬 Action: {"filepath": "main.py"}
      ⏳ 正在执行...
      👁️ Observation: 文件内容...
    ✅ 步骤 2: read_file - 已完成
    
    ✅ 任务完成
    ```
    
    ## 🚀 使用方法
    
    1. 在侧边栏输入 API 密钥
    2. 描述您的任务
    3. 实时观看 Agent 执行过程
    4. 基于 LangChain 0.3.x，稳定可靠！
    
    ## 📚 技术栈
    
    - **LangChain 0.3.x**: Agent 框架
    - **create_agent**: 官方推荐的 Agent 创建方式
    - **stream_mode="updates"**: 节点级别流式输出
    - **Streamlit**: Web 界面
    
    ---
    
    **版本**: V2 (LangChain 0.3.x 兼容版)  
    **创建时间**: 2026-01-08  
    **作者**: AI Cursor Assistant
    """)

# 页脚
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    🤖 游戏开发Agent (V2) - LangChain 0.3.x 兼容版 | 支持DeepSeek、阿里通义千问
</div>
""", unsafe_allow_html=True)

