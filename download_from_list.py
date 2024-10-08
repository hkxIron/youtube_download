#!/usr/bin/env python
# coding:utf-8
# -*- coding: utf-8 -*-
# author: hkxIron
# 根据视频列表，下载视频文件

import os,sys
import platform
from typing import List
import argparse

"""
安装或升级 yt-dlp:
[安装]
python3 -m pip install -U yt-dlp

[升级]
python3 -m pip install -U yt-dlp

error:"token" parameter not in video info for unknown reason
需要去官网下载最新的bin:
https://github.com/ytdl-org/youtube-dl

由于youtube-dl已不再更新，需要使用yt-dlp, 作为youtube-dl的继承者
https://github.com/yt-dlp/yt-dlp

# 安装依赖
python -m pip install -U yt-dlp
# 示例用法, 视频存在data/目录
python download_from_list.py --link_list_file=links/drl_zhaoshiyu.txt --output_dir=/home/hkx/data/TeachVideo/drl_zhaoshiyu --is_playlist=True
python download_from_list.py --link_list_file=links/compression_for_agi.txt --output_dir=data/
python download_from_list.py --link_list_file=links/drl_wangshusheng.txt --output_dir=/home/hkx/data/TeachVideo/drl

用法示例:
python download_from_list.py --link_list_file=links/nn_from_zero.txt  --output_dir=nn_from_zero/

利用ffmpeg从mkv转为mp4:
ffmpeg -i '01_RL Course by David Silver - Lecture 2 - Markov Decision Process_1920x1080.mkv'  -strict -2 '01_RL Course by David Silver - Lecture 2 - Markov Decision Process_1920x1080.mp4'

或者利用脚本
sh convert_mp4.sh
"""

#downloader=r"D:\public_code\hkx_tf_practice\test_python\youtube_download\youtube-dl.exe "
sysstr = platform.system()
print("system: ", sysstr)
if sysstr  =="Windows":
    #downloader=r"youtube-dl.exe "  # 由于是在当前路径下，所以不需要写全路径
    downloader=r"yt-dlp.exe "  # 由于是在当前路径下，所以不需要写全路径
else: # Linux
    #downloader=r"youtube-dl "
    downloader=r"yt-dlp "

#downloader=r"youtube-dl "  # linux
#proxy = ' --proxy "dev-proxy.oa.com:8080" ' # 在公司，代理很好用
#proxy = ' --proxy "xx.yy.cn:3128" '
proxy = ' --proxy "fq.mioffice.cn:3128" '

format = '%(title)s_%(resolution)s.%(ext)s" '

#option=' --write-auto-sub --verbose  --recode-video mp4 ' # 很多不能转为mp4
option=' --write-auto-sub --verbose --sub-format srt --sub-lang en,zh-Hans'
"""
参数--write-auto-sub 是下载自动生成的字幕，不加 auto 是下载上传者上传的字幕
--skip-download 表示不下载视频

--write-sub                      Write subtitle file
--write-auto-sub                 Write automatic subtitle file (YouTube only)
--all-subs                       Download all the available subtitles of the video
--list-subs                      List all available subtitles for the video
--sub-format FORMAT              Subtitle format, accepts formats preference, for example: "srt" or "ass/srt/best"
--sub-lang LANGS                 Languages of the subtitles to download (optional) separated by commas, use IETF language tags like 'en,pt'
"""

def download_video(link_list:List[str], output_dir:str, skip_count:int, is_playlist:bool=False):
    print(f"begin to download list, output_dir:{output_dir} is_playlist:{is_playlist}")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print("mkdir: ",output_dir)
    num = len(link_list)
    if len(link_list) == 0:
        print("no video need download!")
        return
    print("video num:%d skip_count:%d \nlink_list:%s"%(num, skip_count, "\n".join(link_list)))
    index = skip_count + 1
    failed_list = []
    for link in link_list:
        print("begin to download:", link)
        if is_playlist:
            base_filename = format + option + " --yes-playlist"
        else:
            index_str = str(index).zfill(2)  # 填充为两位
            base_filename = index_str + "_" + format + option
        cmd = downloader + link +" -o "+ os.path.join('"'+output_dir, base_filename)
        if len(proxy) > 0:
            cmd += proxy
        print("shell command: ", cmd)
        success_flag = os.system(cmd)>>8 == 0
        if success_flag:
            print("download video success:", link)
        else:
            failed_list.append(link)
            print("download video failed:", link)
        index += 1
    print("total: %d success:%d failed:%d"%(num, num - len(failed_list), len(failed_list)))

def read_link_list(link_list_file:str):
    link_list = []
    skip_links_count = 0
    with open(link_list_file,"r") as fr:
        for line in fr.readlines():
            # 不读取注释的
            if line.strip().startswith("#") or line.strip().startswith("//") or len(line.strip()) <=5:
                if "http://" in line or "https://" in line:
                    skip_links_count+=1
                continue
            link_list.append(line.rstrip("\n"))
    return link_list, skip_links_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--link_list_file', type=str, default='')
    parser.add_argument('--output_dir', type=str, default='')
    parser.add_argument('--is_playlist', type=bool, default=False, help='是否是播放列表')
    args = parser.parse_args()
    print("args:", args)

    link_list_file = args.link_list_file
    output_dir = args.output_dir
    is_playlist = args.is_playlist

    print(f"link list file: {link_list_file}")
    link_list, skip_count = read_link_list(link_list_file)
    download_video(link_list, output_dir, skip_count, is_playlist)
    print("job down.")

