import os
import time

import cv2
import argparse
from deepsort import DeepSort
from collections import Counter
import numpy as np
import sqlite3
global is_stop, people_num
is_stop = 1
people_num = 0
def main(args, threshold=0.5, address1=None, address2=None, address3=None, address4=None, address5=None, address6=None, address7=None,):
    from ui3 import is_true
    os.system('python database.py')
    deepsort = DeepSort(
        det_model_dir=args.det_model_dir,
        emb_model_dir=args.emb_model_dir,
        use_gpu=is_true(),
        run_mode='fluid',
        threshold=threshold,
        max_cosine_distance=args.max_cosine_distance,
        nn_budget=args.nn_budget,
        max_iou_distance=args.max_iou_distance,
        max_age=args.max_age,
        n_init=args.n_init
    )

    cap2 = None
    cap3 = None
    cap4 = None
    cap5 = None
    cap6 = None
    cap7 = None
    success = False
    success2 = False
    success3 = False
    success4 = False
    success5 = False
    success6 = False
    success7 = False
    # 只有一个视频时
    if address1:
        cap = cv2.VideoCapture(address1)
    else:
        cap = cv2.VideoCapture(0)
    # 2个视频时
    if address2:
        cap = cv2.VideoCapture(address1)
        cap2 = cv2.VideoCapture(address2)
    # 3个视频时
    if address3:
        cap = cv2.VideoCapture(address1)
        cap2 = cv2.VideoCapture(address2)
        cap3 = cv2.VideoCapture(address3)
    # 4个视频时
    if address4:
        cap = cv2.VideoCapture(address1)
        cap2 = cv2.VideoCapture(address2)
        cap3 = cv2.VideoCapture(address3)
        cap4 = cv2.VideoCapture(address4)
    # 5个视频时
    if address5:
        cap = cv2.VideoCapture(address1)
        cap2 = cv2.VideoCapture(address2)
        cap3 = cv2.VideoCapture(address3)
        cap4 = cv2.VideoCapture(address4)
        cap5 = cv2.VideoCapture(address5)
    # 6个视频时
    if address6:
        cap = cv2.VideoCapture(address1)
        cap2 = cv2.VideoCapture(address2)
        cap3 = cv2.VideoCapture(address3)
        cap4 = cv2.VideoCapture(address4)
        cap5 = cv2.VideoCapture(address5)
        cap6 = cv2.VideoCapture(address6)
    # 7个视频时
    if address7:
        cap  = cv2.VideoCapture(address1)
        cap2 = cv2.VideoCapture(address2)
        cap3 = cv2.VideoCapture(address3)
        cap4 = cv2.VideoCapture(address4)
        cap5 = cv2.VideoCapture(address5)
        cap6 = cv2.VideoCapture(address6)
        cap7 = cv2.VideoCapture(address7)

    font = cv2.FONT_HERSHEY_SIMPLEX
    if args.save_dir:
        if not os.path.exists(args.save_dir):
            os.mkdir(args.save_dir)
        fps = cap.get(cv2.CAP_PROP_FPS)
        w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        save_video_path = os.path.join(args.save_dir, 'output.avi')
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        writer = cv2.VideoWriter(save_video_path, fourcc, fps, (int(w), int(h)))

    i = 0
    while True:
        global is_stop
        if is_stop == 1:
            return

        img2 = None
        img3 = None
        img4 = None
        img5 = None
        img6 = None
        img7 = None
        bool2=False
        bool3=False
        bool4=False
        bool5 = False
        bool6 = False
        bool7 = False
        if cap != None:
            success, frame1 = cap.read()
        if cap2 != None:
            success2, frame2 = cap2.read()
        if cap3 != None:
            success3, frame3 = cap3.read()
        if cap4 != None:
            success4, frame4 = cap4.read()
        if cap5 != None:
            success5, frame5 = cap5.read()
        if cap6 != None:
            success6, frame6 = cap6.read()
        if cap7 != None:
            success7, frame7 = cap7.read()

        if success:
            # x1 = frame1.size[0]
            # y1 = frame1.size[1]
            # img1 = cv2.resize(frame1, (x1, y1))
            img1 = cv2.resize(frame1, (1920, 1080))
            frame  = img1
        if success2:
            bool2 = True
            # x2 = frame2.size[0]
            # y2 = frame2.size[1]
            img2 = cv2.resize(frame2, (1920, 1080))
        if success3:
            bool3 = True
            # x3 = frame3.size[0]
            # y3 = frame3.size[1]
            img3 = cv2.resize(frame3, (1920, 1080))
        if success4:
            bool4 = True
            # x4 = frame4.size[0]
            # y4 = frame4.size[1]
            img4 = cv2.resize(frame4, (1920, 1080))
        if success5:
            bool5 = True
            # x4 = frame4.size[0]
            # y4 = frame4.size[1]
            img5 = cv2.resize(frame5, (1920, 1080))
        if success6:
            bool6 = True
            # x4 = frame4.size[0]
            # y4 = frame4.size[1]
            img6 = cv2.resize(frame6, (1920, 1080))
        if success7:
            bool7 = True
            # x4 = frame4.size[0]
            # y4 = frame4.size[1]
            img7 = cv2.resize(frame7, (1920, 1080))
        # 核心拼接代码
        # 两个视频时
        if success2 or bool2:
            if success2 == False:
                img2 = cv2.imread('black.jpg')
            if success == False:
                img1 = cv2.imread('black.jpg')
            frame = np.hstack((img1, img2))
        # 三个视频时
        if success3 or bool3:
            if success2 == False:
                img2 = cv2.imread('black.jpg')
            if success3 == False:
                img3 = cv2.imread('black.jpg')
            if success == False:
                img1 = cv2.imread('black.jpg')
            img555 = cv2.imread('black.jpg')
            img555 = cv2.resize(img555, (1920, 1080))
            frame1 = np.hstack((img1, img2))
            frame2 = np.hstack((img3, img555))
            frame = np.vstack((frame1, frame2))
        # 四个视频时
        if success4 or bool4:
            if success2 == False:
                img2 = cv2.imread('black.jpg')
            if success3 == False:
                img3 = cv2.imread('black.jpg')
            if success == False:
                img1 = cv2.imread('black.jpg')
            if success4 == False:
                img4 = cv2.imread('black.jpg')
            frame1 = np.hstack((img1, img2))
            frame2 = np.hstack((img3, img4))
            frame = np.vstack((frame1, frame2))
        # 5个视频时
        if success5 or bool5:
            if success2 == False:
                img2 = cv2.imread('black.jpg')
            if success3 == False:
                img3 = cv2.imread('black.jpg')
            if success == False:
                img1 = cv2.imread('black.jpg')
            if success4 == False:
                img4 = cv2.imread('black.jpg')
            if success5 == False:
                img5 = cv2.imread('black.jpg')
            img666 = cv2.imread('black.jpg')
            img666 = cv2.resize(img666, (1920, 1080))
            frame1 = np.hstack((img1, img2))
            frame2 = np.hstack((img3, img4))
            frame3 = np.hstack((img5, img666))
            frame4 = np.vstack((frame1, frame2))
            frame = np.vstack((frame4, frame3))
        # 6个视频时
        if success6 or bool6:
            if success2 == False:
                img2 = cv2.imread('black.jpg')
            if success3 == False:
                img3 = cv2.imread('black.jpg')
            if success == False:
                img1 = cv2.imread('black.jpg')
            if success4 == False:
                img4 = cv2.imread('black.jpg')
            if success5 == False:
                img5 = cv2.imread('black.jpg')
            if success6 == False:
                img5 = cv2.imread('black.jpg')
            frame1 = np.hstack((img1, img2))
            frame2 = np.hstack((img3, img4))
            frame3 = np.hstack((img5, img6))
            frame = np.vstack((frame1, frame2))
            frame = np.vstack((frame, frame3))
        # 7个视频时
        if success7 or bool7:
            if success2 == False:
                img2 = cv2.imread('black.jpg')
            if success3 == False:
                img3 = cv2.imread('black.jpg')
            if success == False:
                img1 = cv2.imread('black.jpg')
            if success4 == False:
                img4 = cv2.imread('black.jpg')
            if success5 == False:
                img5 = cv2.imread('black.jpg')
            if success6 == False:
                img6 = cv2.imread('black.jpg')
            if success7 == False:
                img7 = cv2.imread('black.jpg')
            img9 = cv2.imread('black.jpg')
            img9 = cv2.resize(img9, (1920, 1080))
            frame0 = np.hstack((img1, img2))
            frame1 = np.hstack((frame0, img3))
            frame3 = np.hstack((img9, img4))
            frame4 = np.hstack((frame3, img9))
            frame5 = np.hstack((img5, img6))
            frame6 = np.hstack((frame5, img7))
            frame7 = np.vstack((frame1, frame4))
            frame = np.vstack((frame7, frame6))
            frame = cv2.resize(frame, (1920, 1080))

        if not success:
            break
        outputs = deepsort.update(frame)
        if outputs is not None:
            count = 0
            for output in outputs:
                if people_num == 0:
                    cv2.rectangle(frame, (output[0], output[1]), (output[2], output[3]), (0, 0, 255), 2)
                    cv2.putText(frame, str(output[-1]), (output[0], output[1]), font, 1.2, (255, 255, 255), 2)
                    count += 1
                elif output[-1] == people_num:
                    cv2.rectangle(frame, (output[0], output[1]), (output[2], output[3]), (0, 0, 255), 2)
                    cv2.putText(frame, str(output[-1]), (output[0], output[1]), font, 1.2, (255, 255, 255), 2)
                    count += 1
                    break
            saveDate(count)
        i = i + 1
        cv2.imwrite("./frame/" + str(i).zfill(5) + '.jpg',
                    frame)  # str(n).zfill(5)设置保存图片文件名格式（5位）00001~    by XTX

        if args.save_dir:
            writer.write(frame)

    if args.save_dir:        
        writer.release()

def saveDate(count):
    conn = sqlite3.connect("people_num.db")
    cur = conn.cursor()
    sql = '''
        insert into  num(
        num)
        values(%d)'''%count
    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()

def stop():
    global is_stop
    is_stop =1

def re_start():
    global is_stop
    is_stop = 0

def start_video1(threshold,address1):
    global args
    main(args, threshold, address1)

def start_video2(threshold,address1,address2):
    global args
    main(args, threshold, address1, address2)

def start_video3(threshold,address1,address2,address3):
    global args
    main(args, threshold, address1, address2, address3)

def start_video4(threshold,address1,address2,address3,address4):
    global args
    main(args, threshold, address1, address2, address3, address4)

def start_video5(threshold,address1,address2,address3,address4,address5):
    global args
    main(args, threshold, address1, address2, address3, address4, address5)

def start_video6(threshold,address1,address2,address3,address4,address5,address6):
    global args
    main(args, threshold, address1, address2, address3, address4, address5, address6)

def start_video7(threshold,address1,address2,address3,address4,address5,address6,address7):
    global args
    main(args, threshold, address1, address2, address3, address4, address5, address6, address7)


def start_camera():
    global args
    main(args)

def find_one(one_num=0):
    global people_num
    people_num = one_num




global args
parser = argparse.ArgumentParser(
    usage='''you can set the video_path or camera_id to start the program,
       and also can set the display or save_dir to display the results or save the output video.''',
    description="this is the help of this script."
)
parser.add_argument("--det_model_dir", type=str, default='model/detection', help="the detection model dir.")
parser.add_argument("--emb_model_dir", type=str, default='model/embedding', help="the embedding model dir.")
parser.add_argument("--run_mode", type=str, default='fluid', help="the run mode of detection model.")
parser.add_argument("--max_cosine_distance", type=float, default=0.3, help="the max cosine distance.")
parser.add_argument("--nn_budget", type=int, default=150, help="the nn budget.")
parser.add_argument("--max_iou_distance", type=float, default=0.5, help="the max iou distance.")
parser.add_argument("--max_age", type=int, default=70, help="the max age.")
parser.add_argument("--n_init", type=int, default=3, help="the number of init.")
parser.add_argument("--save_dir", type=str, default='output', help="the save dir for the output video.")

args = parser.parse_args()
