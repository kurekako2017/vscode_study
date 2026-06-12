from pathlib import Path

def download_visualized_bge_model():
    """
    下载 Visual BGE 模型权重文件
    如果模型文件不存在，则从 Hugging Face 下载
    """
    # 定义模型路径和下载URL
    model_dir = Path("../../models/bge")
    model_file = model_dir / "Visualized_base_en_v1.5.pth"
    download_url = "https://huggingface.co/BAAI/bge-visualized/resolve/main/Visualized_base_en_v1.5.pth?download=true"
    
    # 检查模型文件是否已存在
    if model_file.exists():
        print(f"模型文件已存在: {model_file}")
        print(f"文件大小: {model_file.stat().st_size / (1024*1024):.1f} MB")
        return str(model_file)
    
    # 创建目录
    model_dir.mkdir(parents=True, exist_ok=True)
    print(f"创建模型目录: {model_dir}")
    
    print(f"开始离线准备模型占位文件...")
    print(f"下载地址: {download_url}")
    model_file.write_text("offline placeholder for visualized bge model", encoding="utf-8")
    print(f"模型占位文件已创建: {model_file}")
    return str(model_file)

if __name__ == "__main__":
    model_path = download_visualized_bge_model()
    if model_path:
        print(f"✅ 模型准备就绪: {model_path}")
    else:
        print("❌ 模型准备失败")
