from pickle import TRUE
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
    def __init__(self, rel_path_to_write,data_set_path, scaleFactor = 1.3, minNeighbors = 5, number_of_videos = 10) -> None:
        self.data_set_path = data_set_path
        self.rel_path_to_write = rel_path_to_write
        self.scaleFactor = scaleFactor
        self.HaarCascadeTimeDic={}
        self.minNeighbors = minNeighbors
        self.number_of_videos = number_of_videos
        self.fr = file_reader.FileReader(data_set_path)
        self.haar_cascade_classifier = haar_cascade.FaceClassifier(scaleFactor,minNeighbors)
        self.vl_dic = self.create_video_dic()
        self.haar_cascade_classifier_result_dic, self.haar_cascade_classifier_time_result_dic= self.perform_haar_cascade_on_videos()

    def create_video_dic(self):
        return self.fr.read_all_frames_for_all_videos()

    def perform_haar_cascade_for_gen(self,frame_gen):
        frame_dic = {}
        frame_time_dic ={}
        frame_i = 0
        start_video_time = time.time()
        for frame in frame_gen:
            start_frame_time = time.time()
            frame_dic[frame_i] = self.perfrom_haar_cascade_for_img(frame)
            end_frame_time = time.time()
            finish_frame_time = end_frame_time - start_frame_time
            frame_time_dic[frame_i] =  finish_frame_time
            frame_i += 1
        end_video_time = time.time()
        finish_video_time = end_video_time - start_video_time
        frame_time_dic['finish_video_time'] = finish_video_time
        return frame_dic,frame_time_dic
    def perform_haar_cascade_for_gen_without_frame_time(self,frame_gen):
        frame_dic = {}
        frame_time_dic ={}
        frame_i = 0
        start_video_time = time.time()
        for frame in frame_gen:
            frame_dic[frame_i] = self.perfrom_haar_cascade_for_img(frame)
            frame_i += 1
        end_video_time = time.time()
        finish_video_time = end_video_time - start_video_time
        frame_time_dic['finish_video_time'] = finish_video_time
        return frame_dic,frame_time_dic
    def perfrom_haar_cascade_for_img(self,img):
        return self.haar_cascade_classifier.calc_bb_ls_for_img(img)

    def perform_haar_cascade_on_videos(self, without_frame_time =TRUE):
        video_results={}
        video_time_results ={}
        dic_keys = list(self.vl_dic.keys())[:self.number_of_videos]
        if not without_frame_time:
            for video in dic_keys:
                video_results[video],video_time_results[video] = self.perform_haar_cascade_for_gen(self.vl_dic[video])
        else:
            for video in dic_keys:
                video_results[video],video_time_results[video] = self.perform_haar_cascade_for_gen_without_frame_time(self.vl_dic[video])

        return video_results, video_time_results
      
    def write_the_results(self):
        rw = result_writer.ResultWriter(self.rel_path_to_write)
        rw.write_results_to_path(self.haar_cascade_classifier_result_dic)
        rw.write_down_the_time_dic(self.haar_cascade_classifier_time_result_dic)



class Landmarks():
    def __init__(self, rel_path_to_write,data_set_path , number_of_videos = 1, path_to_predictor= "shape_predictor_68_face_landmarks.dat" ,flag_shape = True ) -> None:
        self.data_set_path = data_set_path
        self.rel_path_to_write = rel_path_to_write
        self.number_of_videos = number_of_videos
        self.flag_shape = flag_shape
        self.path_to_predictor = path_to_predictor
        self.fr = file_reader.FileReader(data_set_path)
        self.landmarks_classifier = landmarks.FaceClassifier(path_to_predictor)
        self.vl_dic = self.create_video_dic()
        self.landmarks_classifier_result_dic, self.landmarks_classifier_time_result_dic = self.perform_landmark_on_videos()
        

    def create_video_dic(self):
        return self.fr.read_all_frames_for_all_videos()

    def perform_landmark_for_gen(self,frame_gen):
        frame_dic = {}
        frame_time_dic ={}
        frame_i = 0
        start_video_time = time.time()
        for frame in frame_gen:
            start_frame_time = time.time()
            frame_dic[frame_i] = self.perfrom_landmark_for_img(frame)
            end_frame_time = time.time()
            finish_frame_time = end_frame_time - start_frame_time
            frame_time_dic[frame_i] =  finish_frame_time
            frame_i += 1
        
        end_video_time = time.time()
        finish_video_time = end_video_time - start_video_time
        frame_time_dic['finish_video_time'] = finish_video_time
        return frame_dic,frame_time_dic

    def perform_landmark_for_gen_without_time_frame(self,frame_gen):
        frame_dic = {}
        frame_time_dic ={}
        frame_i = 0
        start_video_time = time.time()
        for frame in frame_gen:
            frame_dic[frame_i] = self.perfrom_landmark_for_img(frame)
            frame_i += 1
        end_video_time = time.time()
        finish_video_time = end_video_time - start_video_time
        frame_time_dic['finish_video_time'] = finish_video_time
        return frame_dic,frame_time_dic

    def perfrom_landmark_for_img(self,img):
        return self.landmarks_classifier.calc_lm_ls_for_img(img,self.flag_shape)

    def perform_landmark_on_videos(self, without_time_frame = TRUE):
        video_results={}
        video_time_results ={}
        dic_keys = list(self.vl_dic.keys())[:self.number_of_videos]
        if not without_time_frame:
            for video in dic_keys:
                video_results[video],video_time_results[video]  = self.perform_landmark_for_gen(self.vl_dic[video])
        else:
            for video in dic_keys:
                video_results[video],video_time_results[video]  = self.perform_landmark_for_gen_without_time_frame(self.vl_dic[video])
        return video_results, video_time_results

    def write_the_results(self):
        rw = result_writer.ResultWriter(self.rel_path_to_write)
        rw.write_results_to_path(self.landmarks_classifier_result_dic)
        rw.write_down_the_time_dic(self.landmarks_classifier_time_result_dic)

def run(data_set_name, number_of_videos, bb_bool):
    data_path = f"./data/{data_set_name}"
    rel_path_to_write_5 =f"./results/landmark5/{data_set_name}"
    rel_path_to_write_68 =f"./results/landmark68/{data_set_name}"
    rel_path_to_write_haar_cascade =f"./results/haarcascade/{data_set_name}"
    lr = Landmarks(rel_path_to_write_68,data_path,flag_shape=bb_bool,number_of_videos=number_of_videos)
    lr_5 = Landmarks(rel_path_to_write_5,data_path,path_to_predictor="shape_predictor_5_face_landmarks.dat",flag_shape=bb_bool,number_of_videos=number_of_videos)
    hc = HaarCascade(rel_path_to_write_haar_cascade,data_path,number_of_videos=number_of_videos)
    lr.write_the_results()
    lr_5.write_the_results()
    hc.write_the_results()

if __name__ == '__main__':

    """     rel_path_video = 'data/Celeb-real/id23_0006.mp4'
    data_set_celb_real_dir = "./data/Celeb-real"
    rel_path_to_write ="./results/Celeb-real"
    bb_bool = True """
    NUMBER_OF_VIDEOS = 2
    DATA_SET_NAME = 'Celeb-real'
    BB_BOOL = False
    
    run(DATA_SET_NAME, NUMBER_OF_VIDEOS, BB_BOOL)
    #draw_5 = drawer.LandmarkDrawer(lr_5.landmarks_classifier_result_dic, color=(255,0,0),flag_shape=bb_bool)
    #draw_hc = drawer.HaarCascadeDrawer(hc.haar_cascade_classifier_result_dic, color=(0,0,250))
    #draw = drawer.LandmarkDrawer(lr.landmarks_classifier_result_dic, color=(0,255,100),flag_shape=bb_bool)

    """ print(lr.landmarks_classifier_result_dic.keys())
    img = read_specific_frame_for_video(hc.fr,rel_path_video,frame=0)
    img = draw.draw_bounding_box_to_img(rel_path_video,0, img)
    img = draw_5.draw_bounding_box_to_img(rel_path_video,0, img)
    img = draw_hc.draw_bounding_box_to_img(rel_path_video,0, img) """
    #draw_hc.show_img(img)
    #video_0 = list(hcr.vl_dic.keys())[0]
    #video_0_gen= hcr.vl_dic[video_0]
    #for x in video_0_gen:
    #    print(hcr.perfrom_haar_cascade_for_img(x))




