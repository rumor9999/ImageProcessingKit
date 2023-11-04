import argparse
import os
import toml
from copy_image import copy_image
from dataAugmentation import dataSetAug
from randomSort import rename_files_in_directory
from png_set_whitebackground import png_set_whitebackground
from img2png import img2png
from resize_image import resize_images

# 调用函数处理图像
# process_images_in_folder(input_folder, output_folder)

if __name__ == '__main__':
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description='Read TOML configuration file.')

    # 添加命令行参数，指定配置文件路径
    parser.add_argument('config_file',
                        type=str,
                        nargs='?',
                        help='Path to TOML configuration file',
                        default="config.toml")

    # 解析命令行参数
    args = parser.parse_args()

    # 读取TOML配置文件
    config_path = args.config_file

    with open(config_path, "r", encoding="utf-8") as toml_file:
        config = toml.load(toml_file)

    # 获取配置中的路径变量
    input_dataset_path = config["input_dataset_path"]
    output_dataset_path = config["output_dataset_path"]

    # 创建目的地文件夹（如果不存在）
    if not os.path.exists(output_dataset_path):
        os.makedirs(output_dataset_path)

    output_dataset_path_base = input_dataset_path

    # 遍歷來原資料夾，複製到同一個資料夾
    output_dataset_path_original = os.path.join(
        output_dataset_path, "original")
    copy_image(output_dataset_path_base, output_dataset_path_original)
    output_dataset_path_base = output_dataset_path_original

    # 全部轉成png
    output_dataset_path_png = os.path.join(
        output_dataset_path, "png")
    img2png(output_dataset_path_base, output_dataset_path_png)
    output_dataset_path_base = output_dataset_path_png

    # 限制圖片大小
    if config["input_dataset_path"]:
        output_dataset_path_resized = os.path.join(
            output_dataset_path, "resized")
        resize_images(output_dataset_path_base,
                      output_dataset_path_resized, config["image_max_size"])
        output_dataset_path_base = output_dataset_path_resized

    # 透明背景轉白背景
    png_set_whitebackground(output_dataset_path_base)

    # 圖片增生
    dataAugmentation_config = config["data_augmentation"]
    if dataAugmentation_config["enable_data_augmentation"]:
        output_dataset_path_augmentation = os.path.join(
            output_dataset_path, "augmentation")

        dataSetAug(output_dataset_path_base,
                   output_dataset_path_augmentation,
                   dataAugmentation_config["num_rotations"],
                   dataAugmentation_config["num_crops"],
                   dataAugmentation_config["num_contrasts"],
                   dataAugmentation_config["num_brightnesses"])

        output_dataset_path_base = output_dataset_path_augmentation

    output_dataset_path_final = os.path.join(output_dataset_path, "final")
    if config["rename_and_random_sort"]:
        rename_files_in_directory(
            output_dataset_path_base, output_dataset_path_final)
    else:
        copy_image(output_dataset_path_base, output_dataset_path_final)
