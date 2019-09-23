# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:04:46 2019
此文件添加了logging，从而可以生成日志以随时跟踪工作完成情况
@author: flora_fkx
"""

# -*- coding: utf-8 -*-
import os
import cv2    
import sys
import time
import logging
from datetime import datetime

def getlogger(name):
  logger = logging.getLogger(name)
  if not logger.handlers:#To prevent printing the same log again
      formatter = logging.Formatter('%(asctime)s %(levelname)-5s: %(message)s')
      console_handler = logging.FileHandler('logger.log')
      console_handler.setFormatter(formatter)
      logger.addHandler(console_handler)
      logger.setLevel(logging.INFO)
  return logger


def video2frames(logger,num,pathIn='',
                 pathOut='', 
                 output_video_info = False,
                 extract_time_points = None, 
                 initial_extract_time = 0,
                 end_extract_time = None,
                 extract_time_interval = -1, 
                 output_prefix = 'frame',
                 jpg_quality = 100,
                 isColor = True):
    '''
    pathIn：the path to the video, import as an arguement
    pathOut：the directory to store img captured from video
    only_output_video_info：if it's true, then just output the information (duration,number of frames,frames per second) about the video
    extract_time_points：just capture video at the specific seconds, type is tuple
    initial_extract_time：time to start capturing, default time is 0s
    end_extract_time：time to end capturing, default time is the end of the video
    extract_time_interval：to set the time interval for capturing video, use the frames per second,default is -1 which means all frames
    output_prefix：frame_000001.jpg、frame_000002.jpg、frame_000003.jpg......(set the prefix of the img's name, default is 'frame'
    jpg_quality：set the quality of the imgs, default is 1000
    isColor：if it's false, then save the pictures as black and white pics
    '''
    try:
        cap = cv2.VideoCapture(pathIn)  #open the video file
    except:
        logger.warning("There is an error when open the file {}，please check if you have already saved the file：{}".format(num,os.path.basename(pathIn)))
    else:
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  #total frames of the video
        fps = cap.get(cv2.CAP_PROP_FPS)  #frames per video
        dur = n_frames/fps  #duration of the video

        output_video_info=false #You can decide if you just want the information of the video
        if output_video_info:
            print('output the video information (without extract frames)::::::')
            print("Duration of the video: {} seconds".format(dur))
            print("Number of frames: {}".format(n_frames))
            print("Frames per second (FPS): {}".format(fps))
        #code for just capture video at the specific seconds, type is tuple
        elif extract_time_points is not None:
            if max(extract_time_points) > dur:   
                logger.warning('the max time point is larger than the video duration....')
            try:
                os.makedirs(os.path.join(pathOut,output_prefix))
            except OSError:
                pass
            success = True
            count = 0
            time_start = time.time()
            while success and count < len(extract_time_points):
                cap.set(cv2.CAP_PROP_POS_MSEC, (1000*extract_time_points[count]))
                success,image = cap.read()
                if success:
                    if not isColor:
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                      cv2.imwrite(os.path.join(os.path.join(pathOut,output_prefix), "{}_{}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                    count = count + 1
            time_end = time.time()
            logger.info("The video file {},id is {}，per {}s one pic，totally {} pics，used {:.3f}s".format(output_prefix,num,extract_time_interval,count,time_end-time_start))

        else:
            if initial_extract_time > dur:
                logger.warning('initial extract time is larger than the video duration....')
            if end_extract_time is not None:
                if end_extract_time > dur:
                    logger.warning('end extract time is larger than the video duration....')
                if initial_extract_time > end_extract_time:
                    logger.warning('end extract time is less than the initial extract time....')

            if extract_time_interval == -1:
                if initial_extract_time > 0:
                    cap.set(cv2.CAP_PROP_POS_MSEC, (1000*initial_extract_time))
                try:
                    os.makedirs(os.path.join(pathOut,output_prefix))
                except OSError:
                    pass
                if end_extract_time is not None:
                    N = (end_extract_time - initial_extract_time)*fps + 1
                    success = True
                    count = 0
                    time_start = time.time()
                    while success and count < N:
                        success,image = cap.read()
                        if success:
                            if not isColor:
                                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                            cv2.imwrite(os.path.join(os.path.join(pathOut,output_prefix), "{}_{}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                            count =  count + 1
                    time_end = time.time()
                    logger.info("The video file {},id is {}，per {}s one pic，totally {} pics，used {:.3f}s".format(output_prefix,num,extract_time_interval,count,time_end-time_start))
                else:
                    success = True
                    count = 0
                    time_start = time.time()
                    while success:
                        success,image = cap.read()
                        if success:
                            if not isColor:
                                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                            cv2.imwrite(os.path.join(os.path.join(pathOut,output_prefix), "{}_{}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                            count =  count + 1
                    time_end = time.time()
                    logger.info("The video file {},id is {}，per {}s one pic，totally {} pics，used {:.3f}s".format(output_prefix,num,extract_time_interval,count,time_end-time_start))
            elif extract_time_interval > 0 and extract_time_interval < (1/fps):
                logger.warning('extract_time_interval is less than the frame time interval....')
            elif extract_time_interval > (n_frames/fps):
                logger.warning('extract_time_interval is larger than the duration of the video....')

            #code for capturing video after every certain time interval
            else:
                try:
                    os.makedirs(os.path.join(pathOut,output_prefix))
                except OSError:
                    pass
                if end_extract_time is not None:
                    N = (end_extract_time - initial_extract_time)/extract_time_interval + 1
                    success = True
                    count = 0
                    time_start = time.time()
                    while success and count < N:
                        cap.set(cv2.CAP_PROP_POS_MSEC, (1000*initial_extract_time+count*1000*extract_time_interval))
                        success,image = cap.read()
                        if success:
                            if not isColor:
                                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                            cv2.imwrite(os.path.join(os.path.join(pathOut,output_prefix), "{}_{}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                            count = count + 1
                    time_end = time.time()
                    logger.info("The video file {},id is {}，per {}s one pic，totally {} pics，used {:.3f}s".format(output_prefix,num,extract_time_interval,count,time_end-time_start))
                else:
                    success = True
                    count = 0
                    time_start = time.time()
                    while success:
                        cap.set(cv2.CAP_PROP_POS_MSEC, (1000*initial_extract_time+count*1000*extract_time_interval))
                        success,image = cap.read()
                        if success:
                            if not isColor:
                                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                            cv2.imwrite(os.path.join(os.path.join(pathOut,output_prefix), "{}_{}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                            count = count + 1
                    time_end = time.time()
                    logger.info("The video file {},id is {}，per {}s one pic，totally {} pics，used {:.3f}s".format(output_prefix,num,extract_time_interval,count,time_end-time_start))
  

if __name__=="__main__":
    dirname = sys.argv[1]#the directory name where video is saved
    pathOfDir = os.getcwd()
    pathToFile=os.path.join(pathOfDir,dirname)
    b=os.path.join(pathOfDir,sys.argv[2])#the directory name for saving the imgs
    list = []# to put all the path to the list
    name = 'videoToImg'#set the logger file's name
    for root,dirs,names in os.walk(pathToFile):#sort the path of the imgs 
       for namef in names:
           ext=os.path.splitext(namef)[1]
           if ext=='.mp4':
              p = os.path.join(root,namef)
              list.append(p)
    list.sort()
    n = 0 #You can change this number to reset the video to capture, default is the first one video
    while n < len(list):
          c = eval(sys.argv[3])
          logger = getlogger(name)
          pref = os.path.splitext(os.path.basename(list[n]))[0]
          video2frames(logger,n,pathIn=list[n],pathOut=b,extract_time_interval=c, initial_extract_time = 60,end_extract_time = 180,output_prefix =pref)
          n = n+1

        
