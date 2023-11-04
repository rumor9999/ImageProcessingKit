import os
from PIL import Image

def resize_images(input_dir, output_dir, max_size):
    # 建立輸出目錄
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得輸入目錄中的所有檔案
    files = os.listdir(input_dir)
    
    for file in files:
        # 確認檔案是圖片檔案
        if file.endswith('.png'):
            # 載入圖片
            image_path = os.path.join(input_dir, file)
            image = Image.open(image_path)
            
            # 計算新的圖片尺寸
            width, height = image.size
            if width > max_size or height > max_size:
                if width > height:
                    new_width = max_size
                    new_height = int(height * (max_size / width))
                else:
                    new_height = max_size
                    new_width = int(width * (max_size / height))
                new_size = (new_width, new_height)
                
                # 縮放圖片
                resized_image = image.resize(new_size, Image.LANCZOS)
                
                # 儲存縮放後的圖片
                output_path = os.path.join(output_dir, file)
                resized_image.save(output_path)
                print(f"Resized {file} to {new_width}x{new_height}")
            else:
                # 如果圖片尺寸已經小於等於最大尺寸，則直接複製到輸出目錄
                output_path = os.path.join(output_dir, file)
                image.save(output_path)
                print(f"Copied {file} to {output_dir}")