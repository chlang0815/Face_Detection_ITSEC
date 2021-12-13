import file_reader
import haar_cascade
import landmarks
import time

class HaarCascade():
    def __init__(self,data_set_path="./data/Celeb-real", scaleFactor = 1.3, minNeighbors = 5, number_of_videos = 1) -> None:
        self.data_set_path = data_set_path
        self.scaleFactor = scaleFactor
        self.minNeighbors = minNeighbors
        self.number_of_videos = number_of_videos
        self.fr = file_reader.FileReader(data_set_path)
        self.haar_cascade_classifier = haar_cascade.FaceClassifier(scaleFactor,minNeighbors)
        self.vl_dic = self.create_video_dic()
        self.haar_cascade_classifier_result_dic= self.perform_haar_cascade_on_videos()

    def create_video_dic(self):
        return self.fr.read_all_frames_for_all_videos()

    def perform_haar_cascade_for_gen(self,frame_gen):
        frame_dic = {}
        frame_i = 0
        for frame in frame_gen:
            frame_dic[frame_i] = self.perfrom_haar_cascade_for_img(frame)
            frame_i += 1
        return frame_dic

    def perfrom_haar_cascade_for_img(self,img):
        return self.haar_cascade_classifier.calc_bb_ls_for_img(img)

    def perform_haar_cascade_on_videos(self):
        video_results={}
        dic_keys = list(self.vl_dic.keys())[:self.number_of_videos]
        for video in dic_keys:
            video_results[video] = self.perform_haar_cascade_for_gen(self.vl_dic[video])
        return video_results


class SixtyEightLandmarks():
    def __init__(self, data_set_path="./data/Celeb-real", number_of_videos = 1) -> None:
        self.data_set_path = data_set_path
        self.number_of_videos = number_of_videos
        self.fr = file_reader.FileReader(data_set_path)
        self.landmarks_classifier = landmarks.FaceClassifier()
        self.vl_dic = self.create_video_dic()
        self.landmarks_classifier_result_dic= self.perform_landmark_on_videos()
        

    def create_video_dic(self):
        return self.fr.read_all_frames_for_all_videos()

    def perform_landmark_for_gen(self,frame_gen):
        frame_dic = {}
        frame_i = 0
        for frame in frame_gen:
            frame_dic[frame_i] = self.perfrom_landmark_for_img(frame)
            frame_i += 1
        return frame_dic

    def perfrom_landmark_for_img(self,img):
        return self.landmarks_classifier.calc_lm_ls_for_img(img)

    def perform_landmark_on_videos(self):
        video_results={}
        dic_keys = list(self.vl_dic.keys())[:self.number_of_videos]
        for video in dic_keys:
            video_results[video] = self.perform_landmark_for_gen(self.vl_dic[video])
        with open('68landmarks.txt', 'w') as f:
            print(video_results, file=f)
        return video_results

if __name__ == '__main__':
    rel_path_video = "./data/Celeb-real/id0_0002.mp4"
    data_set_celb_real_dir = "./data/Celeb-real"
    start = time.time()
    hcr = SixtyEightLandmarks(data_set_celb_real_dir)
    end = time.time()
    
    print("Time HaarCascade: " , end-start)

    
    
    #video_0 = list(hcr.vl_dic.keys())[0]
    #video_0_gen= hcr.vl_dic[video_0]
    #for x in video_0_gen:
    #    print(hcr.perfrom_haar_cascade_for_img(x))




