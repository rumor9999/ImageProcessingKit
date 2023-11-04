import os
import shutil


def copy_image(start_dir, target_dir):
    print(f"遍歷目錄:\n{start_dir}\n並複製到:\n{target_dir}")

    # 若目標資料夾不存在，則建立
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 遍例目錄並深入子資料夾
    for root, dirs, files in os.walk(start_dir):
        for name in files:
            # 只處理 .png, .jpg 和 .jpeg 檔案
            if name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                # 取得檔案的完整路徑
                file_path = os.path.join(root, name)
                # 確保目標資料夾中檔名不重複
                new_name = get_non_conflicting_name(target_dir, name)
                # 將檔案複製到目標資料夾
                shutil.copy2(file_path, os.path.join(target_dir, new_name))

    print(f"複製完畢")


def get_non_conflicting_name(target_folder, filename):
    # 如果檔案不存在，直接回傳原始檔名
    if not os.path.exists(os.path.join(target_folder, filename)):
        return filename

    # 將檔名拆分為基礎名稱和副檔名
    base_name, extension = os.path.splitext(filename)
    counter = 1

    new_name = f"{base_name}_{counter}{extension}"

    # 當檔案存在時，增加編號並檢查
    while os.path.exists(os.path.join(target_folder, new_name)):
        counter += 1
        new_name = f"{base_name}_{counter}{extension}"

        print(f"原檔名{filename}已存在，調整為新檔名:{new_name}")

    # 回傳不重複的檔名
    return new_name
