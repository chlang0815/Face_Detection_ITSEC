import cv2 
import os
import glob
import time
class FileReader():
    def __init__(self, data_set_dir) -> None:
        self.data_set_dir = data_set_dir
    
    def get_video_name_from_relative_path(self,relative_path_to_video):
        return relative_path_to_video.split("/")[-1].split(".")[0]

    def get_dataset_name_from_relative_path(self,relative_path_to_video):
        return relative_path_to_video.split("/")[-2]
    
    def create_img_path_from_data_set_name(self,data_set_name):
        return 'IMG_'+ data_set_name
    
    def create_folder_if_not_exist(self, rel_path):
        if not os.path.isdir(rel_path):
            os.mkdir(rel_path) 
    def save_all_frames_for_one_video(self,relative_path_to_video):
        video_name = self.get_video_name_from_relative_path(relative_path_to_video)
        #print(f"video_name = {video_name}")
        data_set_name = self.get_dataset_name_from_relative_path(relative_path_to_video)
        folder_name = self.create_img_path_from_data_set_name(data_set_name)
        rel_data_set_path = os.path.join('data',folder_name )
        self.create_folder_if_not_exist(rel_data_set_path)
        rel_path_dir = os.path.join(rel_data_set_path,video_name)
        #print(f"rel_path_dir = {rel_path_dir}")
        self.create_folder_if_not_exist(rel_path_dir)
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
    def read_all_frames_for_one_video(self,relative_path_to_video):
        video_name = self.get_video_name_from_relative_path(relative_path_to_video)
        #print(f"video_name = {video_name}")
        data_set_name = self.get_dataset_name_from_relative_path(relative_path_to_video)
        folder_name = self.create_img_path_from_data_set_name(data_set_name)
        rel_data_set_path = os.path.join('data',folder_name )
        self.create_folder_if_not_exist(rel_data_set_path)
        rel_path_dir = os.path.join(rel_data_set_path,video_name)
        #print(f"rel_path_dir = {rel_path_dir}")
        self.create_folder_if_not_exist(rel_path_dir)
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
    
    def read_all_video_files_for_data_set_dir(self):
        path = os.path.join(self.data_set_dir, ("*.mp4"))
        videos_ls = glob.glob(str(path))
        return videos_ls
    
    def read_all_frames_for_all_videos(self):
        v_ls = self.read_all_video_files_for_data_set_dir()
        v_f_dic = {video : self.read_all_frames_for_one_video(video) for video in v_ls}
        return v_f_dic

if __name__ == '__main__':
    rel_path_video = "./data/Celeb-real/id0_0002.mp4"
    data_set_celb_real_dir = "./data/Celeb-real"

    #extract_multiple_videos(rel_path_video)
    #save_all_frames_for_one_video(rel_path_video)
    #raffov = read_all_frames_for_one_video(rel_path_video)
    #print(next(raffov))
    fr = FileReader(data_set_celb_real_dir)
    v_f_dic = fr.read_all_frames_for_all_videos()
    #print(v_f_dic)
    video_0 = list(v_f_dic.keys())[0]

    #print(video_0)
    #print([x for x in v_f_dic[video_0]])

