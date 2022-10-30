#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from encodings import utf_8
import os
import sys
import subprocess
import glob

for mp4file in glob.glob(r'Z:\test\**\*.mp4',recursive=True):
    hevcfile = mp4file.rpartition('.')[0] + ".hevc.mp4"
    command1 = "ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 %s" %(mp4file)
    res = subprocess.Popen(command1,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
    result = res.stdout.read().decode()

    if 'h264' in result:
        command2="ffmpeg -hwaccel_output_format qsv -c:v h264_qsv -i %s -c:v hevc_qsv -preset veryslow -global_quality 25 -look_ahead 1 %s -y" %(mp4file,hevcfile)
        if subprocess.run(command2,shell=True).returncode==0:
            os.remove(mp4file)
