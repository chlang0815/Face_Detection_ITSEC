import cv2
import numpy as np
from pathlib import Path
class Drawer():
    """Class for drawing the specified result dictonary. 
    """
    def __init__(self,fr ,result_dic, color) -> None:
        """Initilizes the file reader, the result dictonary, and the color.

        Parameters
        ----------
        fr : obj
            The file reader object.
        result_dic :  {str : dic
            A dictonary that contains the videos as keys and a generator as values. A generator contains a dictonary. This diconary has the videos as keys and the frames as values. Each frame contains a list of results.  
        color : (int, int, int)
            The color value. Each integer should be in the range of 0 to 255.
        """
        self.fr = fr
        self.result_dic = result_dic
        self.color = color

    
    def return_result_for_video_and_frame(self, rel_path_to_video, frame):
        """Returns the result for the specified relative path to the video and frame.

        Parameters
        ----------
        rel_path_to_video : str
            Relative path to the video.
        frame : int
            The frame number.

        Returns
        -------
        [[int, ...], ...]
            Returns the result as a list. The return type depends on the selected method. But it is always a list which should contain a list or multiples list .
        """
        video = self.result_dic[rel_path_to_video]
        return video[frame]
    
    def read_specific_frame_for_video(self, rel_path_to_video, frame):
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
        frame_gen = self.fr.read_all_frames_for_one_video(rel_path_to_video)
        if(f_i == 0):
            return next(frame_gen)
        while(f_i != frame):
            frame = next(frame_gen)
            f_i += 1
            return frame

    def show_img(self, img, txt = "DRAWER"):
        """Shows the img 

        Parameters
        ----------
        img : nd.ndarray
            Coloured image, with three dimensions.
        txt : str, optional
            String for the window sub font, by default "DRAWER"
        """
        cv2.imshow(txt,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

class HaarCascadeDrawer(Drawer):
    
    def __init__(self,fr,result_dic, color = (0,0,255)) -> None:
        """Class for drawing the specified result dictonary. Moreover, special functionality for the Haar cascade drawings.

        Parameters
        ----------
        fr : obj
            The instance of the file reader class
        result_dic : dic
            Result dictonary that should contain videos as key and dictonarys as values. These dictonarys should contain the frame number as the key and the list containing a/multiple list/s of four numbers as the values.
            For example { video: {frame : [[int, int, int, int], ...]}}
        color : tuple, optional
            The color value. Each integer should be in the range of 0 to 255, by default (0,0,255)
        """
        super().__init__(fr,result_dic, color)
        print(result_dic)
        self.fontScale =0.75
        self.font =cv2.FONT_HERSHEY_SIMPLEX
    
    def draw_bounding_box_to_img(self, rel_path_to_video, frame):
        """Draws a bouning to the image and returns it.

        Parameters
        ----------
        rel_path_to_video : str
            The relative path to the video.
        frame : int
            The frame number.

        Returns
        -------
        np.ndarray
            The image
        """
        result_ls = self.return_result_for_video_and_frame(rel_path_to_video, frame)
        img = self.read_specific_frame_for_video(rel_path_to_video, frame)
        bb_img = img
        print("IMG_shape:",img.shape)
        for x, y, w, h in result_ls:
            bb_img = cv2.rectangle(bb_img, (x, y),( x + w, y + h), self.color)
            bb_img = cv2.putText(bb_img,f"[{x},{y},{w},{h}]",org = ((x, y + h + 20)),fontFace=self.font, fontScale =self.fontScale,color = self.color)
        return bb_img
