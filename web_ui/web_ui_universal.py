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
        agent = UniversalAgent(
            service=service,
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
if 'plan' not in st.session_state:
    st.session_state.plan = ""
if 'steps' not in st.session_state:
    st.session_state.steps = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 显示执行计划
if st.session_state.plan:
    with st.expander("📋 执行计划", expanded=True):
        st.markdown(st.session_state.plan)

# 显示执行步骤
if st.session_state.steps:
    with st.expander(f"🔄 执行步骤 ({len(st.session_state.steps)}个)", expanded=False):
        for step in st.session_state.steps:
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"**步骤 {step['step']}**")
                with col2:
                    st.markdown(f"**工具**: `{step['tool']}`")
                    if step.get('observation'):
                        st.code(step['observation'][:200] + "..." if len(step.get('observation', '')) > 200 else step.get('observation', ''), language="text")

# 用户输入
if prompt := st.chat_input("输入你的编程任务..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 初始化Agent
    agent, error = init_agent(service, scenario, temperature)
    if error:
        with st.chat_message("assistant"):
            st.error(f"❌ Agent初始化失败: {error}")
        st.stop()
    
    # 流式回调
    def stream_callback(data):
        msg_type = data.get("type")
        
        if msg_type == "plan":
            st.session_state.plan = data.get("content", "")
            with st.chat_message("assistant"):
                with st.expander("📋 执行计划", expanded=True):
                    st.markdown(data.get("content", ""))
        
        elif msg_type == "action":
            step = data.get("step", 0)
            tool = data.get("tool", "")
            if 'steps' not in st.session_state:
                st.session_state.steps = []
            if len(st.session_state.steps) < step:
                st.session_state.steps.append({
                    "step": step,
                    "tool": tool,
                    "args": data.get("args", {}),
                    "observation": ""
                })
        
        elif msg_type == "observation":
            step = data.get("step", 0)
            if step > 0 and len(st.session_state.steps) >= step:
                st.session_state.steps[step - 1]["observation"] = data.get("result", "")
        
        elif msg_type == "final":
            st.session_state.plan = data.get("plan", "")
            st.session_state.steps = data.get("steps", [])
    
    # 执行任务
    with st.chat_message("assistant"):
        with st.spinner("🤔 思考中..."):
            result = agent.run(prompt, stream_callback=stream_callback)
            
            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                st.markdown(result.get("output", "任务完成"))
                
                # 显示执行计划
                if result.get("plan"):
                    with st.expander("📋 执行计划", expanded=True):
                        st.markdown(result["plan"])
                
                # 显示执行步骤
                if result.get("react_steps"):
                    with st.expander(f"🔄 执行步骤 ({len(result['react_steps'])}个)", expanded=False):
                        for step in result["react_steps"]:
                            with st.container():
                                col1, col2 = st.columns([1, 4])
                                with col1:
                                    st.markdown(f"**步骤 {step['step']}**")
                                with col2:
                                    st.markdown(f"**工具**: `{step['tool']}`")
                                    if step.get('observation'):
                                        st.code(step['observation'][:200] + "..." if len(step.get('observation', '')) > 200 else step.get('observation', ''), language="text")
    
    # 添加助手回复
    st.session_state.messages.append({
        "role": "assistant",
        "content": result.get("output", "任务完成")
    })

# 底部说明
st.divider()
st.caption("💡 **提示**: 选择不同的场景可以获得针对性的工具和提示词，提高任务执行效率")

