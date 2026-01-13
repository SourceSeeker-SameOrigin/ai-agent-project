#!/bin/bash

echo "=========================================="
echo "安装CLIP库和相关依赖"
echo "=========================================="

# 激活虚拟环境
if [ -d "venv" ]; then
    echo "✓ 激活虚拟环境..."
    source venv/bin/activate
fi

echo ""
echo "1️⃣ 安装PyTorch相关依赖..."
echo "----------------------------------------"
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo ""
echo "2️⃣ 安装CLIP依赖..."
echo "----------------------------------------"
pip install ftfy regex tqdm pillow requests

echo ""
echo "3️⃣ 安装CLIP库..."
echo "----------------------------------------"
pip install git+https://github.com/openai/CLIP.git

echo ""
echo "=========================================="
echo "✅ 安装完成！"
echo "=========================================="
echo ""
echo "验证安装:"
echo "  python test_clip.py"
echo ""

