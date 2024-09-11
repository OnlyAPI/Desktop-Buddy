import os
import shutil
from rembg import remove
from PIL import Image, ImageSequence
import imageio.v2 as imageio
import io
from concurrent.futures import ThreadPoolExecutor

# 去除PNG图像背景的方法
def remove_png_background(input_path: str, output_path: str):
    with open(input_path, "rb") as input_file:
        input_image = input_file.read()
    
    output_image = remove(input_image)

    with open(output_path, "wb") as output_file:
        output_file.write(output_image)
    
    print(f"已处理PNG: {input_path} -> {output_path}")


# 去除GIF图像背景的方法
def remove_gif_background(input_path: str, output_path: str):
    with Image.open(input_path) as gif:
        frames = []
        
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")
            
            with io.BytesIO() as input_bytes:
                frame.save(input_bytes, format="PNG")
                input_bytes.seek(0)
                
                output_bytes = remove(input_bytes.read())
                frame_no_bg = Image.open(io.BytesIO(output_bytes))
                frames.append(frame_no_bg)

        frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0, duration=gif.info['duration'])
    
    print(f"已处理GIF: {input_path} -> {output_path}")


# 处理 input 文件夹中的文件
def process_images():
    input_folder = 'input'
    output_folder = 'output'
    completed_folder = 'completed'

    # 确保输出和已完成文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(completed_folder, exist_ok=True)

    # 获取输入文件夹中的所有文件
    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    
    # 定义任务列表
    tasks = []

    # 使用线程池执行异步处理
    with ThreadPoolExecutor(max_workers=4) as executor:
        for file_name in files:
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)

            # 根据文件扩展名决定处理方式
            if file_name.lower().endswith('.png') or file_name.lower().endswith('.jpg'):
                # 异步处理PNG图像
                task = executor.submit(remove_png_background, input_path, output_path)
                tasks.append(task)
            elif file_name.lower().endswith('.gif'):
                # 异步处理GIF图像
                task = executor.submit(remove_gif_background, input_path, output_path)
                tasks.append(task)
            else:
                print(f"不支持的文件格式: {file_name}")

    # 等待所有任务完成
    for task in tasks:
        task.result()

    # 将已处理的文件移动到 completed 文件夹
    for file_name in files:
        shutil.move(os.path.join(input_folder, file_name), os.path.join(completed_folder, file_name))
    
    print("所有图像处理完成并移动到 'completed' 文件夹。")

if __name__ == "__main__":
    process_images()
