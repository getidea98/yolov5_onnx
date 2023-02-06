import datetime
import os

import cv2



current_date = datetime.datetime.now().strftime('%Y%m%d')

video_path = r'C:\Users\miaoyimin\Videos\Radeon ReLive\地下城与勇士 Dungeon & Fighter\\'
# 图片存放的路径
img_path = r'C:\Users\miaoyimin\Desktop\yolo\origin\\' + current_date + '\\'

if not os.path.exists(img_path):
    os.mkdir(img_path)

index = 0
for video in os.listdir(video_path):
    if not video.endswith('.mp4'):
        continue
    # 使用opencv按一定间隔截取视频帧，并保存为图片
    vc = cv2.VideoCapture(os.path.join(video_path, video))  # 读取视频文件
    c = 0
    timeF = 180  # 视频帧计数间隔频率,每五百帧截图一次

    if vc.isOpened():  # 判断是否正常打开
        print("yes")
        rval, frame = vc.read()
    else:
        rval = False
        print("false")
    while rval:  # 循环读取视频帧
        rval, frame = vc.read()
        if c % timeF == 0:  # 每隔timeF帧进行存储操作
            cv2.imwrite(img_path  + current_date + '_%06d' % int(index) + '.jpg',
                        frame)  # 存储为图像
            index = index + 1
            print('视频：', video, '正在截图：', index)
        c = c + 1

    print('视频读取完成', video)
print("success!")
cv2.waitKey(1)
vc.release()
