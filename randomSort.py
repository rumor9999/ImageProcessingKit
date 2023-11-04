import os
import uuid

def rename_files_in_directory(start_dir, output_dir):
    supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    
    # 檢查輸出目錄是否存在，如果不存在就建立它
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 取得目前工作目錄
    path = os.path.abspath(start_dir)

    # 建立一個list，將符合條件的檔案名稱存入
    files = [f for f in os.listdir(path) if f.endswith(tuple(supported_formats))]

    # 開始重新命名檔案
    for file_name in files:
        # 取得舊的檔案路徑
        old_path = os.path.join(path, file_name)

        # 使用UUID作為新檔名
        new_name = str(uuid.uuid4()) + os.path.splitext(file_name)[1]

        # 檔案的新路徑
        new_path = os.path.join(output_dir, new_name)

        # 重新命名檔案
        os.rename(old_path, new_path)
        
    # 再次列出輸出目錄下的檔案
    files = [f for f in os.listdir(output_dir) if f.endswith(tuple(supported_formats))]

    # 開始重新命名檔案
    for i, file_name in enumerate(files):
        # 取得舊的檔案路徑
        old_path = os.path.join(output_dir, file_name)

        # 檔名的新名稱
        new_name = str(i + 1) + os.path.splitext(file_name)[1]

        # 檔案的新路徑
        new_path = os.path.join(output_dir, new_name)

        # 重新命名檔案
        os.rename(old_path, new_path)

if __name__ == '__main__':
    # 取得目前工作目錄
    old_path = os.getcwd()

    new_path = os.path.join(old_path, "sorted")

    rename_files_in_directory(old_path, new_path)
