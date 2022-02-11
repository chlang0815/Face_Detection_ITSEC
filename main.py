from pickle import TRUE
from alive_progress import alive_bar
import file_reader
import haar_cascade
import landmarks
import time
import drawer
import result_writer
import cv2

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

def create_video_dic(data_set_path):
    ref_data = "./data-rescaled/celeb-synthesis-720p"
    fr = file_reader.FileReader(data_set_path,ref_data)
    return fr.read_all_frames_for_all_videos()

class HaarCascade():
    def __init__(self, rel_path_to_write,data_set_path, path_to_video ="data-rescaled\\celeb-real-144p\\id2_0008_144p.mp4", scaleFactor = 1.3, minNeighbors = 5, number_of_videos = 10) -> None:
        self.data_set_path = data_set_path
        self.rel_path_to_write = rel_path_to_write
        self.scaleFactor = scaleFactor
        self.HaarCascadeTimeDic={}
        self.minNeighbors = minNeighbors
        self.number_of_videos = number_of_videos
        # self.fr = file_reader.FileReader(data_set_path)
        self.haar_cascade_classifier = haar_cascade.FaceClassifier(scaleFactor,minNeighbors)
        # self.vl_dic = self.create_video_dic()
        self.haar_cascade_classifier_result_dic = {}
        self.haar_cascade_classifier_time_result_dic = {}
        self.path_to_video = path_to_video


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

    def perform_haar_cascade_on_videos(self, video_dic, without_frame_time =TRUE):
        video_results={}
        video_time_results ={}
        if self.number_of_videos > 0:
            dic_keys = list(video_dic.keys())[:self.number_of_videos]
        else:
            dic_keys = [self.path_to_video]
        if not without_frame_time:
            for video in dic_keys:
                video_results[video],video_time_results[video] = self.perform_haar_cascade_for_gen(video_dic[video])
        else:
            with alive_bar(self.number_of_videos) as bar:
                for video in dic_keys:
                    video_results[video],video_time_results[video] = self.perform_haar_cascade_for_gen_without_frame_time(video_dic[video])
                    bar()

        return video_results, video_time_results
    
    def run_haar_cascade(self,video_dic):
        self.haar_cascade_classifier_result_dic, self.haar_cascade_classifier_time_result_dic= self.perform_haar_cascade_on_videos(video_dic)

    def write_the_results(self):
        rw = result_writer.ResultWriter(self.rel_path_to_write)
        rw.write_results_to_path(self.haar_cascade_classifier_result_dic)
        rw.write_down_the_time_dic(self.haar_cascade_classifier_time_result_dic)



class Landmarks():
    def __init__(self, rel_path_to_write, data_set_path, path_to_video ="data-rescaled\\celeb-real-144p\\id2_0008_144p.mp4", number_of_videos = 1, path_to_predictor= "shape_predictor_68_face_landmarks.dat" ,flag_shape = True ) -> None:
        self.data_set_path = data_set_path
        self.rel_path_to_write = rel_path_to_write
        self.number_of_videos = number_of_videos
        self.flag_shape = flag_shape
        self.path_to_predictor = path_to_predictor
        # self.fr = file_reader.FileReader(data_set_path)
        self.landmarks_classifier = landmarks.FaceClassifier(path_to_predictor)
        # self.vl_dic = self.create_video_dic()
        self.landmarks_classifier_result_dic = {}
        self.landmarks_classifier_time_result_dic = {}
        self.path_to_video = path_to_video
    

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

    def perform_landmark_on_videos(self, video_dic, without_time_frame = TRUE):
        video_results={}
        video_time_results ={}
        if self.number_of_videos > 0:
            dic_keys = list(video_dic.keys())[:self.number_of_videos]
        else:
            dic_keys = [self.path_to_video]
        
        if not without_time_frame:
            for video in dic_keys:
                video_results[video],video_time_results[video]  = self.perform_landmark_for_gen(video_dic[video])
        else:
            with alive_bar(self.number_of_videos) as bar:
                for video in dic_keys:
                    video_results[video],video_time_results[video]  = self.perform_landmark_for_gen_without_time_frame(video_dic[video])
                    bar()
        return video_results, video_time_results

    def run_landmark(self, video_dic):
        self.landmarks_classifier_result_dic, self.landmarks_classifier_time_result_dic = self.perform_landmark_on_videos(video_dic)

    def write_the_results(self):
        rw = result_writer.ResultWriter(self.rel_path_to_write)
        rw.write_results_to_path(self.landmarks_classifier_result_dic)
        rw.write_down_the_time_dic(self.landmarks_classifier_time_result_dic)

def run(data_set_name, number_of_videos, bb_bool):
    data_path = f"./data-rescaled/{data_set_name}"
    rel_path_to_write_5 =f"./results/landmark5/{data_set_name}"
    rel_path_to_write_68 =f"./results/landmark68/{data_set_name}"
    rel_path_to_write_haar_cascade =f"./results/haarcascade/{data_set_name}"

    def show_video(path, drawer, txt = "DRAWER"):
        """Shows the video

        """
        cap = cv2.VideoCapture(path)
        if cap.isOpened():
            ret, frame = cap.read()
            (h, w) = frame.shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(f'data_output//{txt}.mp4',
                                    fourcc, 30.0,
                                    (w, h), True)
            
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # Check if camera opened successfully
        if cap.isOpened() == False:
            print("Error opening video stream or file")

        frame_counter = 0

        # Read until video is completed
        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()

            if frame_counter == length:
                frame_counter = 0

            if ret == True:
                # Resize and crop frame
                for d in drawer:   
                    frame = d.draw_bounding_box_to_img(path, frame_counter, frame)
                frame_counter += 1
                writer.write(frame)
                if frame_counter == int(length/2):
                    cv2.imwrite('frame'+str(frame_counter)+'.jpg',frame)
                cv2.imshow("frame", frame)
                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    exit()
            # Break the loop
            else:
                break

        cap.release()  # Release must be inside the outer loop
        writer.release()
 
        # Closes all the frames
        cv2.destroyAllWindows()
    
    #video_list = ["id19_0009"]
    #for vid in video_list:
    #rel_path_video = f"data-rescaled\\{data_set_name}\\{vid}_144p.mp4"

    """ Run Haar Cascade """

    """ video_dic = create_video_dic(data_path)
    hc = HaarCascade(rel_path_to_write_haar_cascade,data_path, number_of_videos=number_of_videos)
    hc.run_haar_cascade( video_dic)
    hc.write_the_results() """
    #draw_hc = drawer.HaarCascadeDrawer(hc.haar_cascade_classifier_result_dic, color=(0,0,250))

    """ Run 5 Landmark """
    video_dic = create_video_dic(data_path)
    lr_5 = Landmarks(rel_path_to_write_5,data_path,path_to_predictor="shape_predictor_5_face_landmarks.dat",flag_shape=bb_bool,number_of_videos=number_of_videos)
    lr_5.run_landmark( video_dic)
    lr_5.write_the_results()
    #draw_5 = drawer.LandmarkDrawer(lr_5.landmarks_classifier_result_dic, color=(255,255,255),flag_shape=bb_bool)


    """ Run 68 Landmark """
    """ video_dic = create_video_dic(data_path)
    lr = Landmarks(rel_path_to_write_68,data_path,flag_shape=bb_bool,number_of_videos=number_of_videos)
    lr.run_landmark( video_dic)
    lr.write_the_results() """
    #draw_68 = drawer.LandmarkDrawer(lr.landmarks_classifier_result_dic, color=(0,255,0),flag_shape=bb_bool)
        

        # draw_list = [draw_hc, draw_5, draw_68]
        # show_video(rel_path_video, draw_list, txt = vid)

if __name__ == '__main__':

    """ Manually set name of the data set,
        amounts of videos in the data set
        and landmark bool to switch between drawing landmarks or drawing bounding boxes in the Landmark algorithms  """
        
    DATA_SET_NAME = 'celeb-synthesis-144p'
    NUMBER_OF_VIDEOS = 660
    LM_BOOL = True
    
    run(DATA_SET_NAME, NUMBER_OF_VIDEOS, LM_BOOL)



