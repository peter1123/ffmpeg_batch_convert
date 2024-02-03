import os
import subprocess

input_folder = r"Z:\test"
output_folder = r"Z:\mp4"

# 遍历文件夹下的所有文件，包括子文件夹
for root, dirs, files in os.walk(input_folder):
    for file in files:
        # 判断文件格式是否为mp4
        if file.endswith(".mp4"):
            input_path = os.path.join(root, file)
            # 使用ffprobe获取视频流信息
            codec = subprocess.check_output(f'ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "{input_path}"').decode().strip()
            # 判断视频编码是否为hevc
            if codec != "hevc":
                output_path = os.path.join(output_folder, os.path.relpath(input_path, input_folder))
                output_path = os.path.splitext(output_path)[0] + ".mp4"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                # 使用ffmpeg进行格式转换
                cmd = f'ffmpeg -y -hide_banner -stats -init_hw_device qsv:hw,child_device_type=d3d11va -hwaccel_output_format qsv -loglevel info -i "{input_path}" -c:v hevc_qsv -c:a aac -preset veryslow -global_quality 25 -pix_fmt nv12 "{output_path}"'
                if subprocess.run(cmd,shell=True).returncode==0:
                    os.replace(output_path, input_path)
                    print(f"文件 {input_path} 转换成功，已替换源文件")
                else:
                    print(f"文件 {input_path} 转换失败，请检查输出信息")
