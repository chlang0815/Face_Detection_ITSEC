import cv2

class FaceClassifier():
    def __init__(self, scaleFactor, minNeighbors):
        """Can create the Haar Cascade classifier

        Parameters
        ----------
        scaleFactor : double
            Describes the scaling factor for the method detctMultiscaleGray of OpenCV
        minNeighbors : int
            Describes the numbers of minimum Neighbours for the method detectMultiscaleGray of OpenCV
        """
        self.classifier = None
        self.scaleFactor = scaleFactor
        self.minNeighbors = minNeighbors
        self.createCascadeClassifier()

    def classifier(self):
        """Returns the classifer

        Returns
        -------
        cv2.CascadeClassifier
            Returns the classifer
        """
        return self.classifier

    def createCascadeClassifier(self):
        """Creates the cascade classifier with the frontalface default of opencv
        """
        self.classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + '/haarcascade_frontalface_default.xml')
    
    def calc_bb_ls_for_img(self, img):
        """Creates the bounding box list for an img. 

        Parameters
        ----------
        img : np.ndarray
            The image on which the classifier should be applied.

        Returns
        -------
        [[int, int, int, int],...]
            Returns a list of bounding boxes which were recognized by the classifier. However, an empty list can also be returned if nothing was detected.
        """
        grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return self.classifier.detectMultiScale(grey_img, self.scaleFactor, self.minNeighbors)
if __name__ == "__main__":
    x= cv2.CascadeClassifier(cv2.data.haarcascades + '/haarcascade_frontalface_default.xml')
    print(type(x))