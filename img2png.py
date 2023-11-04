from PIL import Image
import os
import uuid
import concurrent.futures


def generate_new_filename(filename):
    base, ext = os.path.splitext(filename)
    return base + "_" + str(uuid.uuid4()) + '.png'


def change_image_to_png(input_folder, output_folder, filename):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    try:
        image = Image.open(input_path)
        image = image.convert("RGBA")  # 轉換為RGBA格式，以確保進一步的處理

        new_filename = generate_new_filename(filename)
        output_path = os.path.join(output_folder, new_filename)
        image.save(output_path, 'PNG')
        image.close()
        print(f"已轉換 '{filename}' 為 '{new_filename}'")
    except Exception as e:
        print(f"無法處理 '{filename}': {str(e)}")


def img2png(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for filename in os.listdir(input_folder):
            if filename.endswith(tuple(supported_formats)):
                executor.submit(change_image_to_png,
                                input_folder, output_folder, filename)

    print(f"處理完成，已將轉換後的圖片保存到 '{output_folder}' 資料夾。")
