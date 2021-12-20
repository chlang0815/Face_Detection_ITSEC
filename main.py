import file_reader
import haar_cascade
import landmarks
import time
import drawer
import result_writer

def read_specific_frame_for_video(file_reader, rel_path_to_video, frame):
    """Returns an img for the specified video and frame.

    Parameters
    ----------
    rel_path_to_video : str
        Relative path to the video.
    frame : int
        The frame number.

    Returns
    -------
    np.ndarray
        Coloured image, with three dimensions.
    """
    f_i = 0
    frame_gen = file_reader.read_all_frames_for_one_video(rel_path_to_video)
    if(f_i == 0):
        return next(frame_gen)
    while(f_i != frame):
        frame = next(frame_gen)
        f_i += 1
        return frame


class HaarCascade():
    def __init__(self,data_set_path="./data/Celeb-real",rel_path_to_write = "./results/Celeb-real", scaleFactor = 1.3, minNeighbors = 5, number_of_videos = 2) -> None:

        self.data_set_path = data_set_path
        self.rel_path_to_write = rel_path_to_write
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
      
    def write_the_results(self):
        rw = result_writer.ResultWriter(self.rel_path_to_write)
        rw.write_results_to_path(self.haar_cascade_classifier_result_dic)



class SixtyEightLandmarks():
    def __init__(self, data_set_path="./data/Celeb-real", rel_path_to_write = "./results/Celeb-real", number_of_videos = 1) -> None:
        self.data_set_path = data_set_path
        self.rel_path_to_write = rel_path_to_write
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
        return video_results

    def write_the_results(self):
        rw = result_writer.ResultWriter(self.rel_path_to_write)
        rw.write_results_to_path(self.landmarks_classifier_result_dic)



if __name__ == '__main__':
    rel_path_video = 'data/Celeb-real/id23_0006.mp4'
    data_set_celb_real_dir = "./data/Celeb-real"
    rel_path_to_write ="./results/Celeb-real"
    lr = SixtyEightLandmarks()
    hc = HaarCascade()
    draw_hc = drawer.HaarCascadeDrawer(hc.haar_cascade_classifier_result_dic, color=(0,0,250))
    draw = drawer.LandmarkDrawer(lr.landmarks_classifier_result_dic, color=(0,255,100))
    #print(lr.landmarks_classifier_result_dic.keys())
    img = read_specific_frame_for_video(hc.fr,rel_path_video,frame=0)
    img = draw.draw_bounding_box_to_img(rel_path_video,0, img)
    img = draw_hc.draw_bounding_box_to_img(rel_path_video,0, img)
    #dic = lr.landmarks_classifier_result_dic
    #lr.write_the_results()
   
    draw_hc.show_img(img)
    """hcr = HaarCascade(data_set_celb_real_dir,rel_path_to_write)
    draw = drawer.HaarCascadeDrawer(hcr.fr,hcr.haar_cascade_classifier_result_dic, color=(255,0,255))
    test_img = draw.draw_bounding_box_to_img(rel_path_video,0)
    draw.show_img(test_img) """
    #video_0 = list(hcr.vl_dic.keys())[0]
    #video_0_gen= hcr.vl_dic[video_0]
    #for x in video_0_gen:
    #    print(hcr.perfrom_haar_cascade_for_img(x))




