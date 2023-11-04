from huggingface_hub import hf_hub_download
from ultralytics import YOLO
import cv2
import os
from PIL import Image


def process_images_in_folder(input_folder, output_folder):
    # 加载模型
    yolo_path = hf_hub_download("Bingsu/adetailer", "hand_yolov8s.pt")
    model = YOLO(yolo_path)

    # 检查输出目录是否存在，如果不存在则创建
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有图像文件
    for filename in os.listdir(input_folder):
        if not filename.endswith((".png", ".jpg", ".jpeg")):
            continue

        img_path = os.path.join(input_folder, filename)
        image_cv2 = cv2.imread(img_path)
        image = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))
        output = model(image, conf=0.7)

        # 获取检测到的物体的信息
        results = output[0].boxes.xyxy.numpy()

        if results.size == 0:
            continue

        results = results.tolist()

        # 遍历检测到的物体的边界框
        for idx, bbox in enumerate(results):
            x1, y1, x2, y2 = map(int, bbox)

            # 計算增加20% padding後的新座標
            width = x2 - x1
            height = y2 - y1
            padding_x = int(width * 0.4)
            padding_y = int(height * 0.4)
            new_x1 = max(0, x1 - padding_x)
            new_y1 = max(0, y1 - padding_y)
            new_x2 = min(image.width, x2 + padding_x)
            new_y2 = min(image.height, y2 + padding_y)

            # 截取帶有padding的物體
            object_image = image.crop((new_x1, new_y1, new_x2, new_y2))

            # 生成保存路徑
            object_image_path = os.path.join(
                output_folder, f"{filename}_object_{idx}.png")
            object_image.save(object_image_path)