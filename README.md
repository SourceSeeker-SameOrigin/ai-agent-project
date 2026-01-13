# 🤖 通用编程AI Agent

基于 LangChain 的智能编程助手系统，具备 **Cursor、Claude、Gemini3 pro** 级别的自主编程能力。支持多场景切换，从游戏开发到Web开发、数据科学、DevOps，一应俱全。

## ✨ 核心特性

- 🎯 **多场景支持**: 游戏开发、Web开发、数据科学、DevOps、通用编程
- 🧠 **ReAct模式**: 推理-行动-观察循环，自主规划与执行
- 🛠️ **丰富工具集**: 40+专业工具，覆盖代码分析、编辑、测试、质量检查
- 🌊 **流式输出**: 实时显示执行计划和步骤，体验流畅
- 🛡️ **代码质量**: 自动语法检查、测试运行、文件备份
- 🌐 **多AI服务**: 支持DeepSeek、通义千问、OpenAI等

## 📁 项目结构

```
ai_agent_project/
├── agents/                          # AI Agent 模块
│   ├── agent.py                     # 基础 Agent（OpenAI）
│   ├── agent_china.py               # 中国版 Agent（国内AI服务）
│   ├── agent_game.py                # 游戏开发专用 Agent（保留）
│   └── agent_universal.py           # ⭐ 通用编程 Agent（新增）
│
├── web_ui/                          # Web 界面模块
│   ├── web_ui_china.py              # 中国版 Web 界面
│   ├── web_ui_game.py               # 游戏开发 Web 界面
│   ├── web_ui_universal.py          # ⭐ 通用编程 Web 界面（新增）
│   └── web_react.py                 # ReAct 演示界面
│
├── tools_package/                   # 工具集模块
│   ├── tools.py                     # 基础工具（文件、网络、系统等）
│   ├── game_dev_tools.py            # 游戏开发工具
│   ├── web_dev_tools.py             # ⭐ Web开发工具（新增）
│   ├── data_science_tools.py        # ⭐ 数据科学工具（新增）
│   ├── devops_tools.py              # ⭐ DevOps工具（新增）
│   ├── quality_tools.py             # ⭐ 代码质量工具（新增）
│   └── clip_tools.py                # CLIP 图像分析工具
│
├── games/                           # 游戏项目示例
│   ├── airplane_shooter/            # 飞机大战
│   ├── plane_war/                   # 飞机战争
│   ├── snake/                       # 贪吃蛇
│   └── tetris/                      # 俄罗斯方块
│
├── docs/                            # 文档
│   ├── Agentic_AI_适应机制.md
│   ├── ReAct模式说明.md
│   └── 使用示例.md                  # ⭐ 使用示例（新增）
│
└── scripts/                         # 脚本文件
    ├── install/                     # 安装脚本
    └── launch/                      # 启动脚本
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API 密钥

创建 `.env` 文件并添加您的 API 密钥：

```bash
# 国内AI服务（推荐）
DEEPSEEK_API_KEY=your_deepseek_key_here      # DeepSeek
DASHSCOPE_API_KEY=your_dashscope_key_here    # 阿里通义千问

# 或使用OpenAI（国际版）
OPENAI_API_KEY=your_openai_key_here
```

### 3. 启动应用

#### 方式一：通用编程界面（推荐）⭐

```bash
streamlit run web_ui/web_ui_universal.py
```

支持场景切换，功能最全面！

#### 方式二：使用启动脚本

```bash
# 启动通用编程界面
./scripts/launch/启动Web界面.sh

# 或启动游戏开发界面
./scripts/launch/启动游戏开发Agent.sh
```

## 🎯 使用场景

### 🎮 游戏开发

```
任务: 创建一个贪吃蛇游戏，包含游戏逻辑、食物生成、碰撞检测
```

**Agent会自动**:
1. 分析需求，规划项目结构
2. 创建游戏主文件、蛇类、食物类
3. 实现游戏逻辑和碰撞检测
4. 运行测试，确保游戏可运行

### 🌐 Web开发

```
任务: 创建一个Flask REST API，包含用户管理功能（增删改查）
```

**Agent会自动**:
1. 创建Flask应用结构
2. 实现用户模型和API路由
3. 创建requirements.txt
4. 测试API端点

### 📊 数据科学

```
任务: 创建一个数据分析脚本，读取CSV文件，进行统计分析并生成可视化图表
```

**Agent会自动**:
1. 创建数据分析脚本
2. 实现数据读取和统计分析
3. 生成可视化图表
4. 保存结果

### 🚀 DevOps

```
任务: 为Python应用创建Dockerfile和docker-compose.yml
```

**Agent会自动**:
1. 分析应用依赖
2. 创建Dockerfile
3. 创建docker-compose.yml
4. 测试容器构建

### 🔧 通用编程

```
任务: 重构现有代码，应用设计模式，提高代码质量
```

**Agent会自动**:
1. 分析现有代码结构
2. 识别重构点
3. 应用设计模式
4. 代码质量检查
5. 运行测试确保功能正常

## 🛠️ 工具集

### 基础工具 (7个)
- 文件操作：读取、写入、列表、搜索
- 网络功能：搜索、获取网页内容
- 系统工具：获取时间、系统信息
- 计算器：数学计算、JSON解析

### 代码分析工具 (4个)
- `analyze_python_file`: 深度分析Python文件结构
- `find_function`: 查找特定函数代码
- `analyze_project`: 分析整个项目结构
- `search_code`: 在项目中搜索代码模式

### 代码编辑工具 (4个)
- `write_file`: 写入完整文件
- `replace_function`: 替换指定函数
- `insert_code`: 在指定位置插入代码
- `read_file`: 读取文件内容

### 测试验证工具 (2个)
- `run_python`: 运行Python文件
- `check_syntax`: 检查语法错误

### 代码质量工具 (6个) ⭐
- `check_code_quality`: 代码质量检查（语法、风格、类型）
- `run_tests`: 运行测试
- `backup_file`: 备份文件
- `restore_backup`: 恢复备份
- `create_test_file`: 创建测试文件模板
- `install_quality_tools`: 安装代码质量工具

### Web开发工具 (5个) ⭐
- `create_flask_app`: 创建Flask应用模板
- `create_fastapi_app`: 创建FastAPI应用模板
- `create_api_route`: 创建API路由
- `test_http_endpoint`: 测试HTTP端点
- `create_requirements_web`: 创建Web项目requirements.txt

### 数据科学工具 (4个) ⭐
- `create_data_analysis_script`: 创建数据分析脚本
- `create_ml_model`: 创建机器学习模型模板
- `create_visualization`: 创建数据可视化脚本
- `install_data_science_packages`: 安装数据科学包

### DevOps工具 (5个) ⭐
- `create_dockerfile`: 创建Dockerfile
- `create_docker_compose`: 创建docker-compose.yml
- `create_github_actions`: 创建GitHub Actions工作流
- `run_docker_command`: 执行Docker命令（安全限制）
- `check_system_resources`: 检查系统资源

### 终端与Python环境 (5个)
- `run_command`: 执行终端命令
- `pip_install`: 安装Python包
- `pip_list`: 列出已安装包
- `create_requirements`: 生成requirements.txt
- `check_python_version`: 检查Python版本

### Git版本控制 (2个)
- `git_status`: 查看Git状态
- `git_init`: 初始化Git仓库

**总计: 40+ 专业工具**

## 🎨 交互与体验

### 场景切换
在Web界面中可以选择不同场景：
- 🎮 游戏开发
- 🌐 Web开发
- 📊 数据科学
- 🚀 DevOps
- 🔧 通用编程

每个场景会动态加载对应的工具集和优化后的提示词。

### 计划可视化
Agent会先展示执行计划，然后逐步执行：
1. 📋 **执行计划**: 清晰的任务分解
2. 🔄 **执行步骤**: 实时显示每个工具调用
3. ✅ **观察结果**: 每个步骤的执行结果
4. 📊 **最终总结**: 任务完成情况

### 流式输出
支持实时流式输出，体验流畅：
- 实时显示执行计划
- 逐步展示工具调用
- 即时反馈执行结果

## 🛡️ 代码质量与可靠性

### 自动代码检查
- ✅ **语法检查**: 自动检查Python语法错误
- ✅ **代码风格**: 集成ruff进行代码风格检查（可选）
- ✅ **类型检查**: 集成mypy进行类型检查（可选）

### 测试支持
- ✅ **测试运行**: 自动运行pytest测试
- ✅ **测试模板**: 自动生成测试文件模板
- ✅ **测试验证**: 确保代码可运行

### 文件备份
- ✅ **自动备份**: 修改文件前自动备份
- ✅ **时间戳**: 备份文件带时间戳
- ✅ **恢复功能**: 支持从备份恢复文件

## 📚 文档与示例

### 使用示例
查看 `docs/使用示例.md` 获取详细的使用示例：
- 游戏开发示例
- Web开发示例
- 数据科学示例
- DevOps示例
- 通用编程示例

### 最佳实践
1. **明确任务描述**: 提供清晰的任务描述
2. **分步骤执行**: 复杂任务可以分步骤执行
3. **利用质量工具**: 要求Agent进行代码质量检查
4. **场景选择**: 根据任务类型选择合适的场景

## 🤖 Agent 功能

### 通用编程 Agent (`agents/agent_universal.py`) ⭐
- 支持多场景切换
- 动态工具加载
- 流式输出支持
- 代码质量保证

### 游戏开发 Agent (`agents/agent_game_dev_hybrid.py`)
- 专为游戏开发优化
- Pygame游戏开发工具集
- 保留用于游戏开发场景

### 中国版 Agent (`agents/agent_china.py`)
- 支持国内AI服务
- 完全适配国内网络环境

## 🔧 开发指南

### 添加新场景

1. 在 `SCENARIO_CONFIGS` 中添加场景配置
2. 创建对应的工具集文件
3. 在 `_create_tools_for_scenario` 中注册工具

### 添加新工具

在对应的工具文件中添加工具函数：

```python
@staticmethod
def my_new_tool(params: str) -> str:
    """工具描述"""
    # 实现工具逻辑
    return result
```

然后在 `create_xxx_tools()` 中注册：

```python
Tool(
    name="my_new_tool",
    func=MyTools.my_new_tool,
    description="工具描述"
)
```

## 📦 依赖管理

主要依赖：
- `langchain` - LLM应用框架
- `streamlit` - Web界面
- `rich` - 终端美化
- `python-dotenv` - 环境变量管理

可选依赖：
- `ruff` - 代码风格检查
- `mypy` - 类型检查
- `pytest` - 测试框架
- `pandas` - 数据分析
- `flask` / `fastapi` - Web框架

## 🐛 故障排除

### 导入错误
确保：
1. 从项目根目录运行
2. 虚拟环境已激活
3. 所有依赖已安装

### API密钥问题
```bash
# 验证API密钥
python scripts/install/verify_api_key.py
```

### 工具未安装
某些工具需要额外安装：
```bash
# 安装代码质量工具
pip install ruff mypy pytest

# 安装数据科学工具
pip install pandas numpy matplotlib

# 安装Web开发工具
pip install flask fastapi uvicorn
```

## 📝 更新日志

### 2026-01-09 - 重大更新 ⭐
- ✨ **定位重构**: 从"游戏开发Agent"升级为"通用编程Agent"
- 🛠️ **工具扩展**: 新增Web开发、数据科学、DevOps工具集
- 🎨 **交互改进**: 新增场景切换、计划可视化功能
- 🛡️ **质量保证**: 新增代码质量检查、测试、备份功能
- 📚 **文档完善**: 新增使用示例和最佳实践指南
- 🌐 **UI升级**: 新增通用编程Web界面，支持场景切换

### 2026-01-09 - 初始版本
- ✨ 重构项目结构，按功能模块组织代码
- 📁 创建 `agents/`、`web_ui/`、`tools_package/`、`games/` 等模块
- 📝 更新所有导入路径
- 🚀 更新启动脚本以适配新结构
- 📚 创建完整的项目文档

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

Copyright (c) 2026 SourceSeeker-SameOrigin

MIT 许可证允许：
- ✅ 商业使用
- ✅ 修改
- ✅ 分发
- ✅ 私人使用

唯一要求：保留版权声明和许可证声明。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

- 如有问题，请通过 Issue 联系。
- 邮箱:1178672658@qq.com
- 个人微信:Lisir-Say-Hi

---

**🎉 享受AI编程的乐趣！**
