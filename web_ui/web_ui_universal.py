"""
通用编程Agent Web界面
支持多场景切换的智能编程助手
"""

import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.agent_universal import UniversalAgent, SCENARIO_CONFIGS

# 页面配置
st.set_page_config(
    page_title="🤖 通用编程Agent",
    page_icon="🤖",
    layout="wide"
)

# 标题
st.title("🤖 通用编程AI Agent - Cursor风格编程助手")
st.markdown("**✨ 支持多场景的智能编程助手，具备自主编程能力**")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")
    
    # 场景选择
    scenario = st.selectbox(
        "🎯 使用场景",
        options=list(SCENARIO_CONFIGS.keys()),
        format_func=lambda x: f"{SCENARIO_CONFIGS[x]['name']} - {SCENARIO_CONFIGS[x]['description']}",
        help="选择编程场景，Agent会根据场景调整工具和提示词"
    )
    
    # AI服务选择
    service = st.selectbox(
        "🤖 AI服务",
        ["deepseek", "通义千问"],
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
    elif service == "通义千问":
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
    
    # 场景说明
    scenario_info = SCENARIO_CONFIGS[scenario]
    st.header(f"📋 {scenario_info['name']}场景")
    st.caption(scenario_info['description'])
    
    # 工具说明
    st.header("🔧 可用工具")
    st.caption("根据场景动态加载工具集")
    
    with st.expander("📖 代码分析", expanded=False):
        st.markdown("""
        - `analyze_python_file`: 深度分析Python文件结构
        - `find_function`: 查找特定函数代码
        - `analyze_project`: 分析项目结构
        - `search_code`: 搜索代码模式
        """)
    
    with st.expander("✏️ 代码编辑", expanded=False):
        st.markdown("""
        - `write_file`: 写入完整文件
        - `replace_function`: 替换函数
        - `insert_code`: 插入代码
        - `read_file`: 读取文件
        """)
    
    with st.expander("✅ 测试验证", expanded=False):
        st.markdown("""
        - `run_python`: 运行Python文件
        - `check_syntax`: 检查语法错误
        - `check_code_quality`: 代码质量检查
        - `run_tests`: 运行测试
        """)
    
    with st.expander("🛡️ 代码质量", expanded=False):
        st.markdown("""
        - `backup_file`: 备份文件
        - `restore_backup`: 恢复备份
        - `create_test_file`: 创建测试文件
        """)
    
    # 场景特定工具
    if scenario == "web_dev":
        with st.expander("🌐 Web开发工具", expanded=False):
            st.markdown("""
            - `create_flask_app`: 创建Flask应用
            - `create_fastapi_app`: 创建FastAPI应用
            - `create_api_route`: 创建API路由
            - `test_http_endpoint`: 测试HTTP端点
            """)
    elif scenario == "data_science":
        with st.expander("📊 数据科学工具", expanded=False):
            st.markdown("""
            - `create_data_analysis_script`: 创建数据分析脚本
            - `create_ml_model`: 创建机器学习模型
            - `create_visualization`: 创建可视化脚本
            """)
    elif scenario == "devops":
        with st.expander("🚀 DevOps工具", expanded=False):
            st.markdown("""
            - `create_dockerfile`: 创建Dockerfile
            - `create_docker_compose`: 创建docker-compose.yml
            - `create_github_actions`: 创建GitHub Actions
            - `run_docker_command`: 执行Docker命令
            """)

# 初始化Agent
@st.cache_resource
def init_agent(service, scenario, temperature):
    """初始化Agent（带缓存）"""
    try:
        # 转换服务名称：UI显示"通义千问"，但Agent期望"dashscope"
        agent_service = "dashscope" if service == "通义千问" else service
        agent = UniversalAgent(
            service=agent_service,
            scenario=scenario,
            temperature=temperature,
            verbose=False
        )
        return agent, None
    except Exception as e:
        return None, str(e)

# 主界面
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            # 显示任务规划
            if "plan" in message and message["plan"]:
                with st.expander("📋 任务规划", expanded=False):
                    st.info(message["plan"])
            
            # 显示ReAct执行过程
            if "react_steps" in message and message["react_steps"]:
                is_latest = (message == st.session_state.messages[-1])
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
if prompt := st.chat_input("输入你的编程任务..."):
    # 检查API密钥
    if service == "deepseek" and not os.getenv("DEEPSEEK_API_KEY"):
        st.error("❌ 请先在侧边栏输入DeepSeek API密钥")
    elif service == "通义千问" and not os.getenv("DASHSCOPE_API_KEY"):
        st.error("❌ 请先在侧边栏输入阿里云API密钥")
    else:
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 添加到历史
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
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
                # 初始化Agent
                agent, error = init_agent(service, scenario, temperature)
                if error:
                    st.error(f"❌ Agent初始化失败: {error}")
                    st.stop()
                
                # Agent创建成功后，更新状态
                scenario_name = SCENARIO_CONFIGS[scenario]['name']
                with status_container:
                    st.success(f"✅ Agent初始化完成 ({scenario_name}场景 | {service} | {len(agent.tools)}个工具)")
                
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
                    
                    elif msg_type == "final":
                        # 在标准模式下，final回调会包含所有步骤信息
                        final_plan = data.get("plan", "")
                        final_steps = data.get("steps", [])
                        
                        if final_plan and not realtime_state["plan"]:
                            realtime_state["plan"] = final_plan
                            with plan_container:
                                st.markdown("### 📋 任务规划")
                                st.info(final_plan)
                                st.divider()
                        
                        # 如果流式模式失败，显示所有步骤
                        if final_steps and not realtime_state["steps"]:
                            for step_data in final_steps:
                                step = step_data.get("step", 0)
                                tool = step_data.get("tool", "unknown")
                                args = step_data.get("args", {})
                                observation = step_data.get("observation", "")
                                
                                with steps_container:
                                    step_status = st.status(
                                        f"✅ 步骤 {step}: {tool} - 已完成", 
                                        state="complete", 
                                        expanded=False
                                    )
                                    
                                    with step_status:
                                        st.markdown("#### 💭 Thought (思考)")
                                        st.info(f"我需要使用 `{tool}` 工具来完成这一步")
                                        
                                        st.markdown("#### 🎬 Action (行动)")
                                        import json
                                        if args:
                                            st.code(json.dumps(args, ensure_ascii=False, indent=2), language='json')
                                        else:
                                            st.code("无参数", language='text')
                                        
                                        if observation:
                                            st.markdown("#### 👁️ Observation (观察)")
                                            st.success(observation)
                                
                                realtime_state["steps"].append(step_data)
                
                # 🚀 执行任务（传入回调函数）
                result = agent.run(prompt, stream_callback=realtime_callback)
                
                # 获取结果
                response = result.get("output", "")
                
                # 如果流式模式失败，从result中获取步骤信息
                if not realtime_state["steps"] and result.get("react_steps"):
                    realtime_state["steps"] = result.get("react_steps", [])
                if not realtime_state["plan"] and result.get("plan"):
                    realtime_state["plan"] = result.get("plan", "")
                    with plan_container:
                        st.markdown("### 📋 任务规划")
                        st.info(realtime_state["plan"])
                        st.divider()
                
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
                st.session_state.messages.append({
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

# 底部说明
st.divider()
st.caption("💡 **提示**: 选择不同的场景可以获得针对性的工具和提示词，提高任务执行效率")

