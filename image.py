import os
import cv2
import argparse
from deepsort import DeepSort
from glob import glob
import numpy as np
font = cv2.FONT_HERSHEY_SIMPLEX
def main(args, address, threshold):
    global people
    deepsort = DeepSort(
        det_model_dir=args.det_model_dir, 
        emb_model_dir=args.emb_model_dir, 
        use_gpu=True,
        run_mode='fluid', 
        threshold=threshold,
        max_cosine_distance=args.max_cosine_distance, 
        nn_budget=args.nn_budget, 
        max_iou_distance=args.max_iou_distance, 
        max_age=args.max_age, 
        n_init=args.n_init
    )

    i = 0
    for j in range(3):
        img = cv2.imread(address)
        outputs = deepsort.update(img)
        if outputs is not None:
            count = 0
            for output in outputs:
                cv2.rectangle(img, (output[0], output[1]), (output[2], output[3]), (0,0,255), 2)
                cv2.putText(img, str(output[-1]), (output[0], output[1]), font, 1.2, (255, 255, 255), 2)
                count += 1
            people = count
        print(count)
        cv2.imwrite("./frame/" + str(i).zfill(5) + '.jpg',
                    img)  # str(n).zfill(5)设置保存图片文件名格式（5位）00001~    by XTX


def people_num1():
    global people
    return str(people)

def start_image(address, threshold):
    parser = argparse.ArgumentParser(
        usage='''you can set the video_path or camera_id to start the program, 
            and also can set the display or save_dir to display the results or save the output video.''',
        description="this is the help of this script."
    )

    parser.add_argument("--det_model_dir", type=str, default='model/detection', help="the detection model dir.")
    parser.add_argument("--emb_model_dir", type=str, default='model/embedding', help="the embedding model dir.")
    parser.add_argument("--run_mode", type=str, default='fluid', help="the run mode of detection model.")
    parser.add_argument("--use_gpu", default='True', help="do you want to use gpu.")
    #parser.add_argument("--threshold", type=float, default=0.5, help="the threshold of detection model.")
    parser.add_argument("--max_cosine_distance", type=float, default=0.2, help="the max cosine distance.")
    parser.add_argument("--nn_budget", type=int, default=100, help="the nn budget.")
    parser.add_argument("--max_iou_distance", type=float, default=0.7, help="the max iou distance.")
    parser.add_argument("--max_age", type=int, default=70, help="the max age.")
    parser.add_argument("--n_init", type=int, default=3, help="the number of init.")

    #parser.add_argument("--img_path", type=str, default='./image/1.jpg', help="the input video path or the camera id.")
    parser.add_argument("--save_dir", type=str, default='./output', help="the save dir for the output video.")

    args = parser.parse_args()
    main(args, address, threshold)

if __name__ == '__main__':

    start_image('./image/1.jpg', 0.5)

