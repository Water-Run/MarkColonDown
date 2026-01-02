# ai_remove_bg.py
# pip install rembg pillow

from rembg import remove
from PIL import Image
import io
from pathlib import Path


def ai_remove_background(
    input_path: str | Path,
    output_prefix: str = "Logo",
):
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(input_path)

    print(f"[AI] Removing background: {input_path.name}")

    # 1. 读取原图（二进制，避免任何颜色空间变换）
    with open(input_path, "rb") as f:
        input_bytes = f.read()

    # 2. AI 去背景（U²-Net / IS-Net）
    output_bytes = remove(
        input_bytes,
        alpha_matting=True,          # 关键：启用高质量 alpha
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10,
    )

    # 3. 用 Pillow 打开（RGBA）
    img = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    # 4. 保存原尺寸
    img.save(f"{output_prefix}_4MP.png")

    # 5. 多分辨率导出（高质量缩放）
    img.resize((1024, 1024), Image.Resampling.LANCZOS)\
       .save(f"{output_prefix}_1MP.png")

    img.resize((512, 512), Image.Resampling.LANCZOS)\
       .save(f"{output_prefix}_0.3MP.png")

    img.resize((256, 256), Image.Resampling.LANCZOS)\
       .save(f"{output_prefix}_0.06MP.png")

    print("[OK] Generated:")
    print(" - Logo_4MP.png")
    print(" - Logo_1MP.png")
    print(" - Logo_0.3MP.png")
    print(" - Logo_0.06MP.png")


if __name__ == "__main__":
    ai_remove_background("Logo.png")
