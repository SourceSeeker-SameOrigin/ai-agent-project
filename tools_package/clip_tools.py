"""
CLIP图像分析工具
为Agent添加视觉理解能力
"""

import os
from typing import List, Dict, Optional
from PIL import Image


class CLIPTools:
    """CLIP图像分析工具类"""
    
    def __init__(self):
        """初始化CLIP模型（延迟加载）"""
        self.model = None
        self.preprocess = None
        self.device = None
        self._initialized = False
    
    def _initialize(self):
        """延迟初始化模型（只在第一次使用时加载）"""
        if self._initialized:
            return True
        
        try:
            import torch
            import clip
            
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"🔄 正在加载CLIP模型 (设备: {self.device})...")
            
            self.model, self.preprocess = clip.load("ViT-L/14@336px", device=self.device)
            self._initialized = True
            
            print("✅ CLIP模型加载成功")
            return True
            
        except ImportError:
            print("❌ CLIP库未安装")
            print("💡 安装方法: pip install git+https://github.com/openai/CLIP.git")
            return False
        except Exception as e:
            print(f"❌ CLIP初始化失败: {e}")
            return False
    
    def classify_image(self, image_and_labels: str) -> str:
        """
        对图像进行分类
        
        参数格式: "图片路径|||标签1,标签2,标签3"
        例如: "photo.jpg|||猫,狗,鸟,鱼"
        
        返回: 每个标签的概率
        """
        try:
            # 初始化模型
            if not self._initialize():
                return "错误: CLIP模型未能初始化，请先安装CLIP库"
            
            # 解析参数
            parts = image_and_labels.split("|||")
            if len(parts) != 2:
                return "错误: 参数格式应为 '图片路径|||标签1,标签2,标签3'"
            
            image_path = parts[0].strip()
            labels = [label.strip() for label in parts[1].split(",")]
            
            # 检查文件
            if not os.path.exists(image_path):
                return f"错误: 图片文件 {image_path} 不存在"
            
            # 加载和处理图像
            import torch
            import clip
            
            image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
            text = clip.tokenize(labels).to(self.device)
            
            # 推理
            with torch.no_grad():
                logits_per_image, logits_per_text = self.model(image, text)
                probs = logits_per_image.softmax(dim=-1)
            
            # 格式化结果
            result = f"图像分类结果 ({image_path}):\n\n"
            
            # 按概率排序
            sorted_indices = probs[0].argsort(descending=True)
            
            for idx in sorted_indices:
                label = labels[idx]
                prob = probs[0][idx].item()
                bar = "█" * int(prob * 50)
                result += f"{label:20s} {prob:6.2%} {bar}\n"
            
            return result
            
        except Exception as e:
            return f"图像分类错误: {str(e)}"
    
    def search_images(self, query_and_folder: str) -> str:
        """
        在文件夹中搜索最匹配的图片
        
        参数格式: "搜索文本|||图片文件夹路径"
        例如: "夕阳下的海滩|||./photos"
        
        返回: 按相似度排序的图片列表
        """
        try:
            # 初始化模型
            if not self._initialize():
                return "错误: CLIP模型未能初始化"
            
            # 解析参数
            parts = query_and_folder.split("|||")
            if len(parts) != 2:
                return "错误: 参数格式应为 '搜索文本|||图片文件夹路径'"
            
            query_text = parts[0].strip()
            folder_path = parts[1].strip()
            
            # 检查文件夹
            if not os.path.exists(folder_path):
                return f"错误: 文件夹 {folder_path} 不存在"
            
            # 查找图片文件
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')
            image_files = []
            
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(image_extensions):
                    image_files.append(filename)
            
            if not image_files:
                return f"错误: 文件夹 {folder_path} 中没有找到图片文件"
            
            # 加载所有图片
            import torch
            import clip
            
            images = []
            valid_files = []
            
            for img_file in image_files:
                try:
                    img_path = os.path.join(folder_path, img_file)
                    img = self.preprocess(Image.open(img_path)).unsqueeze(0)
                    images.append(img)
                    valid_files.append(img_file)
                except Exception as e:
                    print(f"跳过 {img_file}: {e}")
            
            if not images:
                return "错误: 没有成功加载任何图片"
            
            images = torch.cat(images).to(self.device)
            text = clip.tokenize([query_text]).to(self.device)
            
            # 计算相似度
            with torch.no_grad():
                image_features = self.model.encode_image(images)
                text_features = self.model.encode_text(text)
                
                # 归一化
                image_features /= image_features.norm(dim=-1, keepdim=True)
                text_features /= text_features.norm(dim=-1, keepdim=True)
                
                # 相似度
                similarity = (image_features @ text_features.T).squeeze(-1)
            
            # 确保similarity是1维的
            if similarity.dim() == 0:
                similarity = similarity.unsqueeze(0)
            
            # 排序结果
            sorted_indices = similarity.argsort(descending=True)
            
            result = f"搜索结果 (查询: '{query_text}'):\n\n"
            result += f"在 {folder_path} 中找到 {len(valid_files)} 张图片\n\n"
            
            # 显示前10个结果
            for i, idx in enumerate(sorted_indices[:10], 1):
                filename = valid_files[idx]
                score = similarity[idx].item()
                bar = "█" * int(score * 50)
                result += f"{i:2d}. {filename:30s} {score:6.3f} {bar}\n"
            
            return result
            
        except Exception as e:
            return f"图像搜索错误: {str(e)}"
    
    def understand_image(self, image_path: str) -> str:
        """
        理解图像内容（分析多个维度）
        
        输入: 图片路径
        
        返回: 场景、时间、天气、情绪等多维度分析
        """
        try:
            # 初始化模型
            if not self._initialize():
                return "错误: CLIP模型未能初始化"
            
            # 检查文件
            if not os.path.exists(image_path):
                return f"错误: 图片文件 {image_path} 不存在"
            
            # 定义多维度问题
            questions = {
                "场景类型": ["室内场景", "户外场景", "城市街道", "自然风景", "建筑物"],
                "时间": ["白天", "夜晚", "黄昏", "清晨", "中午"],
                "天气": ["晴天", "阴天", "雨天", "雪天", "多云"],
                "人物": ["有人物", "无人物", "单人", "多人", "人群"],
                "情绪氛围": ["欢快的", "平静的", "忧郁的", "激动的", "神秘的"]
            }
            
            import torch
            import clip
            
            # 加载图像
            image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
            
            result = f"图像内容分析 ({image_path}):\n\n"
            
            # 逐个维度分析
            for category, options in questions.items():
                text = clip.tokenize(options).to(self.device)
                
                with torch.no_grad():
                    logits_per_image, logits_per_text = self.model(image, text)
                    probs = logits_per_image.softmax(dim=-1)
                
                # 找出最可能的选项
                best_idx = probs[0].argmax().item()
                best_option = options[best_idx]
                best_prob = probs[0][best_idx].item()
                
                result += f"【{category}】: {best_option} (置信度: {best_prob:.1%})\n"
                
                # 显示其他选项
                result += "  其他可能: "
                other_probs = []
                for i, option in enumerate(options):
                    if i != best_idx:
                        other_probs.append(f"{option}({probs[0][i].item():.0%})")
                result += ", ".join(other_probs[:3]) + "\n\n"
            
            return result
            
        except Exception as e:
            return f"图像理解错误: {str(e)}"
    
    def compare_images(self, images_str: str) -> str:
        """
        比较多张图片的相似度
        
        参数格式: "图片1路径,图片2路径,图片3路径,..."
        例如: "cat1.jpg,cat2.jpg,dog.jpg"
        
        返回: 图片之间的相似度矩阵
        """
        try:
            # 初始化模型
            if not self._initialize():
                return "错误: CLIP模型未能初始化"
            
            # 解析参数
            image_paths = [path.strip() for path in images_str.split(",")]
            
            if len(image_paths) < 2:
                return "错误: 至少需要2张图片进行比较"
            
            # 检查文件
            for path in image_paths:
                if not os.path.exists(path):
                    return f"错误: 图片文件 {path} 不存在"
            
            # 加载所有图片
            import torch
            
            images = []
            for img_path in image_paths:
                img = self.preprocess(Image.open(img_path)).unsqueeze(0)
                images.append(img)
            
            images = torch.cat(images).to(self.device)
            
            # 计算特征
            with torch.no_grad():
                features = self.model.encode_image(images)
                features /= features.norm(dim=-1, keepdim=True)
                
                # 计算相似度矩阵
                similarity_matrix = features @ features.T
            
            # 格式化结果
            result = "图片相似度分析:\n\n"
            
            # 显示文件名（简化）
            short_names = [os.path.basename(path)[:20] for path in image_paths]
            
            # 表头
            result += "      "
            for name in short_names:
                result += f"{name:22s}"
            result += "\n" + "-" * (6 + 22 * len(short_names)) + "\n"
            
            # 相似度矩阵
            for i, name1 in enumerate(short_names):
                result += f"{name1:20s}  "
                for j in range(len(short_names)):
                    sim = similarity_matrix[i][j].item()
                    result += f"{sim:5.2f}  "
                    result += "█" * int(sim * 10) + "  "
                result += "\n"
            
            # 找出最相似的图片对
            result += "\n最相似的图片对:\n"
            max_sim = 0
            max_pair = (0, 0)
            
            for i in range(len(image_paths)):
                for j in range(i + 1, len(image_paths)):
                    sim = similarity_matrix[i][j].item()
                    if sim > max_sim:
                        max_sim = sim
                        max_pair = (i, j)
            
            result += f"  {short_names[max_pair[0]]} ↔ {short_names[max_pair[1]]}\n"
            result += f"  相似度: {max_sim:.2%}\n"
            
            return result
            
        except Exception as e:
            return f"图片比较错误: {str(e)}"


# 创建全局实例（延迟初始化）
_clip_tools = CLIPTools()


def create_clip_tools():
    """创建CLIP工具列表（用于集成到Agent）"""
    from langchain_core.tools import Tool
    
    tools = [
        Tool(
            name="classify_image",
            func=_clip_tools.classify_image,
            description="使用CLIP对图像进行分类。输入格式：'图片路径|||标签1,标签2,标签3'。Classify image with CLIP."
        ),
        Tool(
            name="search_images",
            func=_clip_tools.search_images,
            description="在文件夹中搜索最匹配的图片。输入格式：'搜索文本|||文件夹路径'。Search images in folder."
        ),
        Tool(
            name="understand_image",
            func=_clip_tools.understand_image,
            description="理解图像内容，分析场景、时间、天气等。输入：图片路径。Understand image content."
        ),
        Tool(
            name="compare_images",
            func=_clip_tools.compare_images,
            description="比较多张图片的相似度。输入格式：'图片1,图片2,图片3,...'。Compare image similarity."
        ),
    ]
    
    return tools


if __name__ == "__main__":
    """测试CLIP工具"""
    print("=" * 60)
    print("CLIP工具测试")
    print("=" * 60)
    
    clip_tools = CLIPTools()
    
    print("\n1. 测试模型加载:")
    if clip_tools._initialize():
        print("✅ CLIP工具可用")
    else:
        print("❌ CLIP工具不可用，请先安装CLIP库")
        print("   安装命令: pip install git+https://github.com/openai/CLIP.git")

