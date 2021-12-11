import cv2 
import os
import glob
import time
def get_video_name_from_relative_path(relative_path_to_video):
    return relative_path_to_video.split("/")[-1].split(".")[0]
def get_dataset_name_from_relative_path(relative_path_to_video):
    return relative_path_to_video.split("/")[-2]
def create_img_path_from_data_set_name(data_set_name):
    return 'IMG_'+ data_set_name
def create_folder_if_not_exist(rel_path):
    if not os.path.isdir(rel_path):
        os.mkdir(rel_path)

def save_all_frames_for_one_video(relative_path_to_video):
    video_name = get_video_name_from_relative_path(relative_path_to_video)
    #print(f"video_name = {video_name}")
    data_set_name = get_dataset_name_from_relative_path(relative_path_to_video)
    folder_name = create_img_path_from_data_set_name(data_set_name)
    rel_data_set_path = os.path.join('data',folder_name )
    create_folder_if_not_exist(rel_data_set_path)
    rel_path_dir = os.path.join(rel_data_set_path,video_name)
    #print(f"rel_path_dir = {rel_path_dir}")
    create_folder_if_not_exist(rel_path_dir)
    # Keep iterating break
    cap = cv2.VideoCapture(relative_path_to_video)
    i = 0
    while True:
        ret, frame = cap.read()  # Read frame from first video
        if ret:
            path_to_file = os.path.join(rel_path_dir,str(i) + '.jpg' )
            cv2.imwrite(path_to_file , frame)  # Write frame to JPEG file (1.jpg, 2.jpg, ...)
            cv2.imshow('frame', frame)  # Display frame for testing
            i += 1 # Advance file counter
        else:
            # Break the interal loop when res status is False.
            break

        #cv2.waitKey(100) #Wait 100msec (for debugging)

    cap.release() #Release must be inside the outer loop

def read_all_frames_for_one_video(relative_path_to_video):
    video_name = get_video_name_from_relative_path(relative_path_to_video)
    #print(f"video_name = {video_name}")
    data_set_name = get_dataset_name_from_relative_path(relative_path_to_video)
    folder_name = create_img_path_from_data_set_name(data_set_name)
    rel_data_set_path = os.path.join('data',folder_name )
    create_folder_if_not_exist(rel_data_set_path)
    rel_path_dir = os.path.join(rel_data_set_path,video_name)
    #print(f"rel_path_dir = {rel_path_dir}")
    create_folder_if_not_exist(rel_path_dir)
    # Keep iterating break
    cap = cv2.VideoCapture(relative_path_to_video)
    i = 0
    while True:
        ret, frame = cap.read()  # Read frame from first video
        if ret:
            yield frame
        else:
            # Break the interal loop when res status is False.
            break

        #cv2.waitKey(100) #Wait 100msec (for debugging)

    cap.release() #Release must be inside the outer loop


def read_all_video_files_for_data_set_dir(data_set_dir):
    path = os.path.join(data_set_dir, ("*.mp4"))
    videos_ls = glob.glob(str(path))
    return videos_ls

def read_all_frames_for_all_videos(data_set_dir):
    v_ls = read_all_video_files_for_data_set_dir(data_set_dir)
    v_dic_for= {}
    time_v_f_dic_s =  time.time()
    v_f_dic = {video : read_all_frames_for_one_video(video) for video in v_ls}
    time_v_f_dic_e =  time.time()
    for video in v_ls: 
        v_dic_for[video] = read_all_frames_for_one_video(video)
    return v_f_dic

if __name__ == '__main__':
    rel_path_video = "./data/Celeb-real/id0_0002.mp4"
    data_set_celb_real_dir = "./data/Celeb-real"
    data_set_celb_real_dir = "./data/Celeb-real"
    data_set_celb_real_dir = "./data/Celeb-real"
    #extract_multiple_videos(rel_path_video)
    #save_all_frames_for_one_video(rel_path_video)
    #raffov = read_all_frames_for_one_video(rel_path_video)
    #print(next(raffov))
    v_f_dic = read_all_frames_for_all_videos(data_set_celb_real_dir)
    print(v_f_dic)
    keys = list(v_f_dic.keys())
    print(keys)
    vid_name = keys[0]
    #print(vid_name)
    #print([x for x in v_f_dic[vid_name]])


