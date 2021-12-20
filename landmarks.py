import cv2
import dlib
import numpy as np

class FaceClassifier():
    def __init__(self, shape = "shape_predictor_68_face_landmarks.dat"):
        """Can create the 68Landmarks classifier

        Parameters
        ----------
        scaleFactor : double
            Describes the scaling factor for the method detctMultiscaleGray of OpenCV
        minNeighbors : int
            Describes the numbers of minimum Neighbours for the method detectMultiscaleGray of OpenCV
        """

        self.shape = shape
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.shape)

    def detector(self):
        """Returns the classifer

        Returns
        -------
        Dlib frontal face detector
            Returns detector
        """
        return self.detector

    def predictor(self):
        """Returns the classifer

        Returns
        -------
        Dlib shape predictor
            Returns predictor
        """
        return self.predictor

    def shape_to_np(self, dlib_shape, dtype="int"):
        """Converts dlib shape object to numpy array"""

        # Initialize the list of (x,y) coordinates
        coordinates = np.zeros((dlib_shape.num_parts, 2), dtype=dtype)

        # Loop over all facial landmarks and convert them to a tuple with (x,y) coordinates:
        for i in range(0, dlib_shape.num_parts):
            coordinates[i] = (dlib_shape.part(i).x, dlib_shape.part(i).y)

        # Return the list of (x,y) coordinates:
        return coordinates
        
    
    def calc_lm_ls_for_img(self, img, flag_shape = True ):
        """Creates the bounding box list for an img. 

        Parameters
        ----------
        img : np.ndarray
            The image on which the classifier should be applied.
        flag_shape : bool, optional
            [description], by default True

        Returns
        -------
        [[int, int, int, int],...]
            Returns a list of bounding boxes which were recognized by the classifier. However, an empty list can also be returned if nothing was detected.
        """
        grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = self.detector(grey_img, 0)

        shape = []
        for (i, rect) in enumerate(rects):
              shape.append(self.shape_to_np(self.predictor(grey_img, rect)))
        if(flag_shape):
            return shape
        else: 
            return rects
        
if __name__ == "__main__":
    x= cv2.CascadeClassifier(cv2.data.haarcascades + '/haarcascade_frontalface_default.xml')
    print(type(x))