import os
from PIL import Image


def png_set_whitebackground(folder):
    # 獲取文件夾中的所有文件
    files = os.listdir(folder)

    for filename in files:
        if filename.lower().endswith((".png")):
            input_path = os.path.join(folder, filename)

            # 打开图像
            image = Image.open(input_path)

            # 如果图像具有透明通道
            if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
                # 创建一个白色背景的新图像
                new_image = Image.new('RGB', image.size, (255, 255, 255))

                # 将原始图像复制到新图像上，自动处理透明部分
                new_image.paste(image, (0, 0), image)

                # 保存新图像
                new_image.save(input_path)

                print(f"{input_path}已替换透明背景")
            else:
                print("图像没有透明背景，无需替换")
