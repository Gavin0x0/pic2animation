import imageio
import torch
import time
from tqdm import tqdm
from animate import normalize_kp
from demo import load_checkpoints
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage import img_as_ubyte
from skimage.transform import resize
import cv2
import os
import argparse
import subprocess
import os
from PIL import Image


def video2mp3(file_name):
    """
    将视频转为音频
    :param file_name: 传入视频文件的路径
    :return:
    """
    outfile_name = file_name.split('.')[0] + '.mp3'
    cmd = 'ffmpeg -i ' + file_name + ' -f mp3 ' + outfile_name + ' -y'
    print(cmd)
    subprocess.call(cmd, shell=True)

def video_add_mp3(file_name, mp3_file):
    """
     视频添加音频
    :param file_name: 传入视频文件的路径
    :param mp3_file: 传入音频文件的路径
    :return:
    """
    outfile_name = file_name.split('.')[0] + '-f.mp4'
    subprocess.call('ffmpeg -i ' + file_name
                    + ' -i ' + mp3_file + ' -strict -2 -f mp4 '
                    + outfile_name + ' -y', shell=True)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input_image", required=True,
                help="Path to image to animate")
ap.add_argument("-c", "--checkpoint", required=True, help="Path to checkpoint")
ap.add_argument("-v", "--input_video", required=False,
                help="Path to video input")

args = vars(ap.parse_args())
# 带时间的输出文件名 11_06_20_51_59_output.mp4
nowtime = time.strftime("%m_%d_%H_%M_%S", time.localtime())
# 没有声音的生成视频
filename = nowtime+'_output.mp4'
# 带声音的最终视频
finalname = nowtime+'_output-f.mp4'

print(";python; Loading image and checkpoint...")
source_path = args['input_image']
checkpoint_path = args['checkpoint']
if args['input_video']:
    video_path = args['input_video']
else:
    print(";python; video not exist!")
# 图像压缩
source_image = imageio.imread(source_path)
source_image = resize(source_image, (256, 256))[..., :3]
# 当前文件位置
currPath = os.path.dirname(__file__)
# 当前文件绝对路径
asbPath = os.path.abspath(__file__)

generator, kp_detector = load_checkpoints(
    config_path=currPath+'/config/vox-256.yaml', checkpoint_path=checkpoint_path)
# 检查输出文件夹
if not os.path.exists(currPath+'/output'):
    os.mkdir(currPath+'/output')

relative = True
adapt_movement_scale = True
cpu = False
# 如果存在视频路径就加载视频
if video_path:
    cap = cv2.VideoCapture(video_path)
    print(";python; Loading video...")
else:
    print(";python; video not exist!")

fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

video2mp3(file_name=video_path)

fourcc = cv2.VideoWriter_fourcc('M', 'P', 'E', 'G')
out1 = cv2.VideoWriter(currPath+'/output/'+filename, fourcc, fps, size, True)

cv2_source = cv2.cvtColor(source_image.astype('float32'), cv2.COLOR_BGR2RGB)
with torch.no_grad():
    predictions = []
    source = torch.tensor(source_image[np.newaxis].astype(
        np.float32)).permute(0, 3, 1, 2)
    if not cpu:
        source = source.cuda()
    kp_source = kp_detector(source)
    count = 0
    while(True):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if ret == True:
            frame1 = resize(frame, (256, 256))[..., :3]
            if count == 0:
                source_image1 = frame1
                source1 = torch.tensor(source_image1[np.newaxis].astype(
                    np.float32)).permute(0, 3, 1, 2)
                kp_driving_initial = kp_detector(source1)
            frame_test = torch.tensor(
                frame1[np.newaxis].astype(np.float32)).permute(0, 3, 1, 2)
            driving_frame = frame_test
            if not cpu:
                driving_frame = driving_frame.cuda()
            kp_driving = kp_detector(driving_frame)
            kp_norm = normalize_kp(kp_source=kp_source,
                                   kp_driving=kp_driving,
                                   kp_driving_initial=kp_driving_initial,
                                   use_relative_movement=relative,
                                   use_relative_jacobian=relative,
                                   adapt_movement_scale=adapt_movement_scale)
            out = generator(source, kp_source=kp_source, kp_driving=kp_norm)
            predictions.append(np.transpose(
                out['prediction'].data.cpu().numpy(), [0, 2, 3, 1])[0])
            im = np.transpose(
                out['prediction'].data.cpu().numpy(), [0, 2, 3, 1])[0]
            im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
            out1.write(img_as_ubyte(im))
            count += 1
        else:
            break
    cap.release()
    out1.release()
    cv2.destroyAllWindows()
video_add_mp3(file_name=currPath+'/output/'+filename,
              mp3_file=video_path.split('.')[0] + '.mp3')

if os.path.exists(currPath+'/output/'+finalname):
    if os.path.getsize(currPath+'/output/'+finalname)>1024*100:
        # 成功则回一个视频路径
        print(';finalvideo;'+asbPath+'/../output/'+finalname)
    else:
        print(';python; failed')
else:
    print(';python; failed')
