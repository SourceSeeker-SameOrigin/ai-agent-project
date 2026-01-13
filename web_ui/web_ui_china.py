"""
Streamlit Web界面 - 中国版
支持阿里通义千问、百度文心一言等国内 AI 服务
"""

import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from agents.agent_china import AIAgentChina

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(
    page_title="AI Agent 🇨🇳",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .service-badge {
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_agent(service, api_key, model, temperature, max_iterations, show_thinking, enable_clip=False):
    """初始化 Agent"""
    try:
        # 根据服务类型设置环境变量
        if service == "阿里通义千问":
            os.environ["AI_SERVICE"] = "dashscope"
            os.environ["DASHSCOPE_API_KEY"] = api_key
            if model:
                os.environ["DASHSCOPE_MODEL"] = model
            service_key = "dashscope"
            
        elif service == "百度文心一言":
            os.environ["AI_SERVICE"] = "wenxin"
            os.environ["WENXIN_API_KEY"] = api_key
            if model:
                os.environ["WENXIN_MODEL"] = model
            service_key = "wenxin"
            
        elif service == "智谱ChatGLM":
            os.environ["AI_SERVICE"] = "zhipu"
            os.environ["ZHIPU_API_KEY"] = api_key
            if model:
                os.environ["ZHIPU_MODEL"] = model
            service_key = "zhipu"
            
        elif service == "DeepSeek":
            os.environ["AI_SERVICE"] = "deepseek"
            os.environ["DEEPSEEK_API_KEY"] = api_key
            if model:
                os.environ["DEEPSEEK_MODEL"] = model
            service_key = "deepseek"
        else:
            return None, "未知的服务类型"
        
        # 创建 Agent（verbose 控制是否显示思考过程）
        agent = AIAgentChina(
            model=model if model else None,
            temperature=temperature,
            max_iterations=max_iterations,
            verbose=show_thinking,  # 使用参数控制
            service=service_key,
            enable_clip=enable_clip  # 添加CLIP支持
        )
        
        return agent, None
        
    except ValueError as e:
        return None, str(e)
    except Exception as e:
        return None, f"初始化失败: {str(e)}"


def main():
    # 标题
    st.markdown("<h1 class='main-header'>🤖 AI Agent 🇨🇳</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>基于 LangChain 的智能代理系统 | 支持国内主流 AI 服务</p>", unsafe_allow_html=True)
    
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 配置")
        
        # 服务选择
        service = st.selectbox(
            "🌐 AI 服务",
            ["阿里通义千问", "百度文心一言", "智谱ChatGLM", "DeepSeek"],
            index=0,
            help="选择要使用的国内 AI 服务"
        )
        
        # 显示服务信息
        service_info = {
            "阿里通义千问": {
                "icon": "🔵",
                "desc": "免费额度充足，响应快速",
                "register": "https://dashscope.aliyun.com/",
                "models": ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-longcontext"],
                "default_model": "qwen-turbo"
            },
            "百度文心一言": {
                "icon": "🔴",
                "desc": "中文理解能力强",
                "register": "https://console.bce.baidu.com/qianfan/",
                "models": ["ERNIE-Bot-turbo", "ERNIE-Bot", "ERNIE-Bot-4"],
                "default_model": "ERNIE-Bot-turbo"
            },
            "智谱ChatGLM": {
                "icon": "🟢",
                "desc": "免费额度最多",
                "register": "https://open.bigmodel.cn/",
                "models": ["glm-4", "glm-4-plus", "glm-3-turbo"],
                "default_model": "glm-4"
            },
            "DeepSeek": {
                "icon": "🟣",
                "desc": "价格超低，性能不错",
                "register": "https://platform.deepseek.com/",
                "models": ["deepseek-chat", "deepseek-coder"],
                "default_model": "deepseek-chat"
            }
        }
        
        info = service_info[service]
        st.info(f"{info['icon']} {info['desc']}")
        
        # API 密钥输入
        api_key_label = f"{service} API Key"
        
        # 尝试从环境变量读取
        env_key_map = {
            "阿里通义千问": "DASHSCOPE_API_KEY",
            "百度文心一言": "WENXIN_API_KEY",
            "智谱ChatGLM": "ZHIPU_API_KEY",
            "DeepSeek": "DEEPSEEK_API_KEY"
        }
        
        default_key = os.getenv(env_key_map[service], "")
        
        api_key = st.text_input(
            api_key_label,
            value=default_key,
            type="password",
            help=f"输入你的 {service} API 密钥"
        )
        
        if not api_key:
            st.warning("⚠️ 请输入 API 密钥")
            st.info(f"💡 获取密钥: [{service} 官网]({info['register']})")
        
        st.divider()
        
        # 模型选择
        model = st.selectbox(
            "🎯 模型",
            info["models"],
            index=0,
            help="选择要使用的模型（turbo 版本最便宜）"
        )
        
        # 温度参数
        temperature = st.slider(
            "🌡️ 温度 (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="控制输出随机性：0=确定性，1=创造性"
        )
        
        # 默认无限制迭代，默认显示思考过程
        max_iterations = None
        show_thinking = True
        
        st.divider()
        
        # 🆕 CLIP视觉功能开关
        enable_clip = st.checkbox(
            "🎨 启用 CLIP 图像分析",
            value=False,
            help="启用后可以分析图像、搜索图片等（需要先安装CLIP库）"
        )
        
        if enable_clip:
            st.info("💡 CLIP功能已启用！可以使用图像分析功能")
            st.caption("如未安装CLIP，运行: ./install_clip.sh")
        
        st.divider()
        
        # 工具列表
        st.header("🔧 可用工具")
        
        # 基础工具
        basic_tools = [
            "📄 读取文件",
            "✍️ 写入文件",
            "📁 列出目录",
            "🧮 计算器",
            "🔍 网络搜索",
            "🌐 获取网页",
            "⏰ 获取时间",
            "📊 分析JSON"
        ]
        
        # CLIP工具
        clip_tools = [
            "🖼️ 图像分类",
            "🔍 搜索图片",
            "👁️ 理解图像",
            "📊 比较图片"
        ]
        
        st.markdown("**基础工具:**")
        for tool in basic_tools:
            st.markdown(f"- {tool}")
        
        if enable_clip:
            st.markdown("**🎨 CLIP视觉工具:**")
            for tool in clip_tools:
                st.markdown(f"- {tool}")
        
        st.divider()
        
        # 使用统计
        if "chat_count" in st.session_state:
            st.header("📊 使用统计")
            st.metric("对话次数", st.session_state.chat_count)
    
    # 检查 API 密钥
    if not api_key:
        st.warning("⚠️ 请在侧边栏配置 API 密钥")
        
        # 显示获取指南
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            ### 📝 获取 {service} API 密钥
            
            1. 访问 [{service} 官网]({info['register']})
            2. 注册/登录账号
            3. 进入 API 密钥管理页面
            4. 创建新的 API 密钥
            5. 复制密钥并粘贴到左侧输入框
            """)
        
        with col2:
            st.markdown("""
            ### 💡 为什么选择国内服务？
            
            - ✅ **无需翻墙**：访问稳定快速
            - ✅ **免费额度**：新用户有充足免费额度
            - ✅ **支付便捷**：支持支付宝/微信
            - ✅ **中文优化**：中文理解能力更强
            - ✅ **价格便宜**：比 OpenAI 便宜 80-90%
            """)
        
        return
    
    # 初始化 Agent
    if "agent" not in st.session_state or st.session_state.get("last_service") != service or st.session_state.get("last_show_thinking") != show_thinking or st.session_state.get("last_enable_clip") != enable_clip:
        with st.spinner(f"正在初始化 {service}..."):
            agent, error = initialize_agent(service, api_key, model, temperature, max_iterations, show_thinking, enable_clip)
            
            if error:
                st.error(f"❌ {error}")
                return
            
            st.session_state.agent = agent
            st.session_state.last_service = service
            st.session_state.last_show_thinking = show_thinking
            st.session_state.last_enable_clip = enable_clip
            st.session_state.initialized = True
            
            success_msg = f"✅ {service} 已成功连接！"
            if enable_clip:
                success_msg += " 🎨 CLIP视觉功能已启用"
            st.success(success_msg)
    
    # 主界面 - 使用标签页
    tab1, tab2, tab3 = st.tabs(["💬 对话", "📝 示例", "ℹ️ 帮助"])
    
    with tab1:
        # 对话界面
        st.header(f"与 {service} 对话")
        
        # 初始化聊天历史
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.chat_count = 0
        
        # 显示聊天历史
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                # 如果是 assistant 消息，显示 ReAct 过程
                if message["role"] == "assistant":
                    # 显示任务规划
                    if "plan" in message and message["plan"]:
                        with st.expander("📋 任务规划", expanded=False):
                            st.markdown(message["plan"])
                    
                    # 显示 ReAct 步骤
                    if "react_steps" in message and message["react_steps"]:
                        with st.expander("🧠 ReAct 执行过程", expanded=False):
                            import json
                            for step_data in message["react_steps"]:
                                step = step_data.get("step", 0)
                                tool = step_data.get("tool", "unknown")
                                args = step_data.get("args", {})
                                observation = step_data.get("observation", "")
                                
                                st.markdown(f"### 🔄 步骤 {step}: {tool}")
                                
                                st.markdown("**💭 Thought (思考)**")
                                st.info(f"我需要使用 `{tool}` 工具来完成这个步骤")
                                
                                st.markdown("**🎬 Action (行动)**")
                                st.code(json.dumps(args, ensure_ascii=False, indent=2), language='json')
                                
                                if observation:
                                    st.markdown("**👁️ Observation (观察)**")
                                    st.success(observation if len(observation) < 500 else observation[:500] + "...")
                                
                                st.divider()
                
                st.markdown(message["content"])
        
        # 用户输入
        if prompt := st.chat_input("输入你的问题..."):
            # 添加用户消息
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # 获取AI响应
            with st.chat_message("assistant"):
                # 使用占位符
                plan_placeholder = st.empty()
                steps_placeholder = st.empty()
                result_placeholder = st.empty()
                
                # 显示加载状态
                with plan_placeholder.container():
                    st.info("🔄 正在分析任务并执行...")
                
                try:
                    # 执行任务
                    result = st.session_state.agent.run(prompt, stream_callback=None)
                    
                    response = result.get("output", "")
                    messages = result.get("messages", [])
                    
                    # 解析消息，提取步骤和计划
                    plan_text = ""
                    react_steps = []
                    step_num = 0
                    
                    # 第一遍：查找计划
                    for msg in messages:
                        if hasattr(msg, 'content') and msg.content:
                            msg_type = type(msg).__name__
                            if 'AI' in msg_type:
                                content = msg.content
                                # 即使有 tool_calls，如果内容包含规划关键词，也认为是计划
                                if any(keyword in content for keyword in ["步骤", "计划", "首先", "然后", "接下来", "使用"]):
                                    if not plan_text or len(content) > len(plan_text):
                                        plan_text = content
                    
                    # 第二遍：提取步骤
                    for i, msg in enumerate(messages):
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
                                for j in range(i+1, len(messages)):
                                    next_msg = messages[j]
                                    if hasattr(next_msg, 'tool_call_id') and next_msg.tool_call_id == tool_call.get('id'):
                                        content = next_msg.content if hasattr(next_msg, 'content') else str(next_msg)
                                        step_data["observation"] = content
                                        break
                                
                                react_steps.append(step_data)
                    
                    # 提取最终答案
                    final_answer = response if response and response != "未能获取响应" else ""
                    
                    if not final_answer:
                        # 从消息中提取
                        for msg in reversed(messages):
                            if hasattr(msg, 'content') and msg.content:
                                msg_type = type(msg).__name__
                                if 'AI' in msg_type:
                                    if not hasattr(msg, 'tool_calls') or not msg.tool_calls:
                                        # 排除计划文本，避免重复
                                        if msg.content != plan_text:
                                            final_answer = msg.content
                                            break
                    
                    if not final_answer:
                        final_answer = "任务已执行完成。请查看上方的执行步骤了解详情。"
                    
                    # 更新显示内容
                    # 1. 显示任务规划
                    if plan_text and show_thinking:
                        with plan_placeholder.container():
                            with st.expander("📋 任务规划", expanded=True):
                                st.markdown(plan_text)
                    else:
                        plan_placeholder.empty()
                    
                    # 2. 显示 ReAct 步骤
                    if react_steps and show_thinking:
                        with steps_placeholder.container():
                            with st.expander("🧠 ReAct 执行过程", expanded=True):
                                import json
                                for step_data in react_steps:
                                    step = step_data.get("step", 0)
                                    tool = step_data.get("tool", "unknown")
                                    args = step_data.get("args", {})
                                    observation = step_data.get("observation", "")
                                    
                                    st.markdown(f"### 🔄 步骤 {step}: {tool}")
                                    
                                    st.markdown("**💭 Thought (思考)**")
                                    st.info(f"我需要使用 `{tool}` 工具来完成这个步骤")
                                    
                                    st.markdown("**🎬 Action (行动)**")
                                    try:
                                        args_str = json.dumps(args, ensure_ascii=False, indent=2)
                                    except:
                                        args_str = str(args)
                                    st.code(args_str, language='json')
                                    
                                    if observation:
                                        st.markdown("**👁️ Observation (观察)**")
                                        display_obs = observation if len(observation) < 500 else observation[:500] + "..."
                                        st.success(display_obs)
                                    
                                    st.divider()
                    else:
                        steps_placeholder.empty()
                    
                    # 3. 显示最终答案
                    with result_placeholder.container():
                        st.markdown("---")
                        st.markdown("### ✅ 最终答案")
                        st.markdown(final_answer)
                    
                    # 添加AI响应到历史（包含 ReAct 数据）
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": final_answer,
                        "react_steps": react_steps if show_thinking else [],
                        "plan": plan_text if show_thinking else ""
                    })
                    
                    st.session_state.chat_count += 1
                    
                except Exception as e:
                    import traceback
                    error_msg = f"错误: {str(e)}"
                    error_detail = traceback.format_exc()
                    
                    plan_placeholder.empty()
                    steps_placeholder.empty()
                    
                    with result_placeholder.container():
                        st.error(error_msg)
                        with st.expander("查看详细错误"):
                            st.code(error_detail)
                        st.info("💡 **建议**: 检查 API 密钥、网络连接，或尝试更简单的任务")
                    
                    # 在终端打印详细错误
                    print(f"\n错误详情:\n{error_detail}")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
        
        # 清除历史按钮
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("🗑️ 清除对话"):
                st.session_state.messages = []
                st.rerun()
        with col2:
            if st.button("🔄 重新连接"):
                if "agent" in st.session_state:
                    del st.session_state.agent
                st.rerun()
    
    with tab2:
        # 示例任务
        st.header("示例任务")
        st.markdown("点击下面的按钮快速尝试示例任务")
        
        # 基础示例
        examples = [
            ("🧮 数学计算", "计算 (125 + 375) * 2 的值"),
            ("⏰ 获取时间", "现在几点了？今天星期几？"),
            ("📁 文件操作", "列出当前目录的所有文件和文件夹"),
            ("🔍 网络搜索", "搜索2024年最新的AI技术趋势"),
            ("📝 创建文件", "创建一个名为hello.py的Python文件，内容是打印Hello World"),
            ("📊 数据分析", '分析这个JSON: {"name": "test", "value": 100}'),
        ]
        
        # CLIP示例（如果启用了CLIP）
        if enable_clip:
            clip_examples = [
                ("🖼️ 图像分类", "分析photo.jpg，告诉我这是什么"),
                ("🔍 搜索图片", "在photos文件夹中找出所有猫的照片"),
                ("👁️ 理解图像", "理解scene.jpg的场景、时间和天气"),
                ("📊 比较图片", "比较cat1.jpg和cat2.jpg的相似度"),
            ]
            st.markdown("### 🎨 CLIP视觉示例")
            st.info("💡 请确保图片文件存在，或修改路径")
            
            cols = st.columns(2)
            for i, (title, task) in enumerate(clip_examples):
                with cols[i % 2]:
                    if st.button(title, key=f"clip_example_{i}"):
                        st.session_state.messages.append({"role": "user", "content": task})
                        
                        with st.spinner("执行中..."):
                            try:
                                result = st.session_state.agent.run(task)
                                response = result.get("output", "处理失败")
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": response
                                })
                                st.session_state.chat_count += 1
                                st.success("✅ 执行完成！切换到对话标签查看结果")
                            except Exception as e:
                                st.error(f"❌ 执行失败: {e}")
            
            st.divider()
            st.markdown("### 📋 基础工具示例")
        
        cols = st.columns(2)
        for i, (title, task) in enumerate(examples):
            with cols[i % 2]:
                if st.button(title, key=f"example_{i}"):
                    # 执行示例任务
                    st.session_state.messages.append({"role": "user", "content": task})
                    
                    with st.spinner("执行中..."):
                        try:
                            result = st.session_state.agent.run(task)
                            response = result.get("output", "处理失败")
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": response
                            })
                            st.session_state.chat_count += 1
                            st.success("✅ 执行完成！切换到对话标签查看结果")
                        except Exception as e:
                            st.error(f"❌ 执行失败: {e}")
    
    with tab3:
        # 帮助信息
        st.header("使用帮助")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 快速开始
            
            1. **选择服务**: 在侧边栏选择 AI 服务
            2. **输入密钥**: 粘贴你的 API 密钥
            3. **开始对话**: 在对话框输入问题
            4. **查看结果**: Agent 会自动使用工具完成任务
            
            ### 💡 使用技巧
            
            - **明确描述**: 清晰地描述你的需求
            - **分步执行**: 复杂任务可以分解
            - **利用工具**: Agent 会自动选择工具
            - **试试示例**: 从示例任务开始
            
            ### 📚 示例问题
            
            **文件操作：**
            - "创建一个待办事项文件"
            - "读取 README.md"
            - "列出 Python 文件"
            
            **数据处理：**
            - "计算 1 到 100 的和"
            - "分析这段 JSON 数据"
            
            **信息查询：**
            - "搜索 Python 最新版本"
            - "现在几点了？"
            """)
        
        with col2:
            st.markdown(f"""
            ### 🌐 关于 {service}
            
            **{info['desc']}**
            
            **可用模型：**
            """)
            for m in info["models"]:
                st.markdown(f"- `{m}`")
            
            st.markdown(f"""
            **获取 API 密钥：**
            
            访问 [{service} 官网]({info['register']})
            
            ### 💰 费用说明
            
            - **免费额度**: 新用户通常有大量免费额度
            - **按量计费**: 用完免费额度后按使用量计费
            - **价格实惠**: 比国外服务便宜 80-90%
            - **支付方便**: 支持支付宝/微信支付
            
            ### ⚠️ 注意事项
            
            - API 密钥请妥善保管
            - 文件操作限于项目目录
            - 网络搜索需要稳定连接
            - 合理使用，避免浪费额度
            
            ### 📞 技术支持
            
            如遇问题：
            1. 检查 API 密钥是否正确
            2. 确认网络连接正常
            3. 查看服务商控制台
            4. 参考项目文档
            """)
        
        st.divider()
        
        # 服务对比
        st.markdown("### 📊 国内 AI 服务对比")
        
        comparison_data = {
            "服务": ["阿里通义千问", "百度文心一言", "智谱ChatGLM", "DeepSeek"],
            "免费额度": ["100万tokens", "大量免费", "1000万tokens", "有免费额度"],
            "中文能力": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐"],
            "响应速度": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
            "性价比": ["⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
        }
        
        st.table(comparison_data)


if __name__ == "__main__":
    main()

