#!/bin/bash
# 中国用户快速配置脚本

echo "🇨🇳 AI Agent - 中国用户配置向导"
echo "======================================"
echo ""

# 选择服务
echo "请选择要使用的 AI 服务:"
echo "1. 阿里通义千问（最推荐，免费额度多）"
echo "2. 百度文心一言（免费额度多）"
echo "3. 智谱 ChatGLM（免费额度最多）"
echo "4. DeepSeek（最便宜）"
echo ""
read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        SERVICE="dashscope"
        SERVICE_NAME="阿里通义千问"
        API_KEY_VAR="DASHSCOPE_API_KEY"
        MODEL_VAR="DASHSCOPE_MODEL"
        MODEL_DEFAULT="qwen-turbo"
        REGISTER_URL="https://dashscope.aliyun.com/"
        ;;
    2)
        SERVICE="wenxin"
        SERVICE_NAME="百度文心一言"
        API_KEY_VAR="WENXIN_API_KEY"
        MODEL_VAR="WENXIN_MODEL"
        MODEL_DEFAULT="ERNIE-Bot-turbo"
        REGISTER_URL="https://console.bce.baidu.com/qianfan/"
        ;;
    3)
        SERVICE="zhipu"
        SERVICE_NAME="智谱ChatGLM"
        API_KEY_VAR="ZHIPU_API_KEY"
        MODEL_VAR="ZHIPU_MODEL"
        MODEL_DEFAULT="glm-4"
        REGISTER_URL="https://open.bigmodel.cn/"
        ;;
    4)
        SERVICE="deepseek"
        SERVICE_NAME="DeepSeek"
        API_KEY_VAR="DEEPSEEK_API_KEY"
        MODEL_VAR="DEEPSEEK_MODEL"
        MODEL_DEFAULT="deepseek-chat"
        REGISTER_URL="https://platform.deepseek.com/"
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "✅ 已选择: $SERVICE_NAME"
echo ""

# 检查是否已有 API Key
if [ -f .env ]; then
    existing_key=$(grep "^${API_KEY_VAR}=" .env 2>/dev/null | cut -d'=' -f2)
    if [ ! -z "$existing_key" ]; then
        echo "⚠️  检测到已存在的 API Key: ${existing_key:0:10}..."
        read -p "是否要更新？(y/n): " update
        if [ "$update" != "y" ] && [ "$update" != "Y" ]; then
            echo "保持现有配置"
            exit 0
        fi
    fi
fi

# 提示用户获取 API Key
echo "📝 请按以下步骤获取 API Key:"
echo ""
echo "1. 访问: $REGISTER_URL"
echo "2. 注册/登录账号"
echo "3. 找到 API Key 管理页面"
echo "4. 创建新的 API Key"
echo "5. 复制完整的 API Key"
echo ""

read -p "请粘贴你的 API Key: " api_key

if [ -z "$api_key" ]; then
    echo "❌ API Key 不能为空"
    exit 1
fi

# 创建 .env 文件
echo "📝 正在创建配置文件..."
cat > .env << EOF
# ============================================
# 国内 AI 服务配置
# ============================================

# 服务选择
AI_SERVICE=$SERVICE

# $SERVICE_NAME
${API_KEY_VAR}=$api_key
${MODEL_VAR}=$MODEL_DEFAULT

# ============================================
# 通用配置
# ============================================
TEMPERATURE=0
MAX_ITERATIONS=10
VERBOSE=true
EOF

echo "✅ 配置文件已创建"
echo ""

# 测试配置
echo "🧪 正在测试配置..."
echo ""

# 激活虚拟环境并测试
source venv/bin/activate 2>/dev/null || true
python agent_china.py --task "你好" 2>&1 | head -20

echo ""
echo "======================================"
echo "✅ 配置完成！"
echo ""
echo "🚀 使用方法:"
echo "  python agent_china.py              # 对话模式"
echo "  python agent_china.py --tools      # 查看工具"
echo "  python agent_china.py --task <任务> # 执行任务"
echo ""
echo "📚 详细文档: 中国用户配置指南.md"
echo "======================================"

