import cv2
import glob
import time
from pathlib import Path
from collections import Counter


class FileReader:
    def __init__(self, data_set_dir) -> None:
        """Class that has the task to read images that are located in the specified folder path.

        Parameters
        ----------
        data_set_dir : str
            Relative path which specifies where the image folder is located.
        """
        self.data_set_dir = data_set_dir
        self.video_ls = self.read_all_video_files_for_data_set_dir()

    def get_video_name_from_relative_path(self, relative_path_to_video):

        """Returns the video name from the relative path.Returns the video name from the relative path.
        For relative_path_to_video="./data/Celeb-real/id0_0002.mp4" the video_name would be =id0_0002.

        Parameters
        ----------
        relative_path_to_video : str
            The relative path to a video

        Returns
        -------
        str
            The video name
        """
        return relative_path_to_video.split("/")[-1].split(".")[0]

    def get_dataset_name_from_relative_path(self, relative_path_to_video):

        """Returns the dataset from the relative path.
        For relative_path_to_video="./data/Celeb-real/id0_0002.mp4" the data_set_name would be = Celeb-real.

        Parameters
        ----------
        relative_path_to_video : str
            The relative path to a video

        Returns
        -------
        str
            The data set name
        """
        return relative_path_to_video.split("/")[-2]

    def create_img_path_from_data_set_name(self, data_set_name):

        """Adds a prefix to the data set name and returns it.

        Parameters
        ----------
        data_set_name : str
            The data set name

        Returns
        -------
        str
            The new dat set name
        """

        return "IMG_" + data_set_name

    def create_folder_if_not_exist(self, rel_path):
        """Creates a folder if no folder exists at rel_path.

        Parameters
        ----------
        rel_path : str
            The folder path
        """
        if not Path.is_dir(rel_path):
            Path.mkdir(rel_path)

    def save_all_frames_for_one_video(self, relative_path_to_video):

        """Saves all frames for a video under a specific path that can be created.

        Parameters
        ----------
        relative_path_to_video : str
            The relative path to the video
        """
        video_name = self.get_video_name_from_relative_path(relative_path_to_video)

        # print(f"video_name = {video_name}")
        data_set_name = self.get_dataset_name_from_relative_path(relative_path_to_video)
        folder_name = self.create_img_path_from_data_set_name(data_set_name)
        rel_data_set_path = Path.joinpath(Path("data"), Path(folder_name))
        self.create_folder_if_not_exist(rel_data_set_path)
        rel_path_dir = Path.joinpath(Path(rel_data_set_path), video_name)
        # print(f"rel_path_dir = {rel_path_dir}")

        self.create_folder_if_not_exist(rel_path_dir)
        # Keep iterating break
        cap = cv2.VideoCapture(relative_path_to_video)
        i = 0
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:

                path_to_file = Path.joinpath(Path(rel_path_dir), str(i) + ".jpg")
                cv2.imwrite(
                    str(path_to_file), frame
                )  # Write frame to JPEG file (1.jpg, 2.jpg, ...)
                cv2.imshow("frame", frame)  # Display frame for testing
                i += 1  # Advance file counter

            else:
                # Break the interal loop when res status is False.
                break

            # cv2.waitKey(100) #Wait 100msec (for debugging)

        cap.release()  # Release must be inside the outer loop

    def read_all_frames_for_one_video(self, relative_path_to_video):

        """Read all frames of a video under a specific path that can be created.

        Parameters
        ----------
        relative_path_to_video : str
            The relative path to the video

        Yields
        -------
        np.ndarray
            Yields frame images for a specific video
        """
        cap = cv2.VideoCapture(relative_path_to_video)

        # Check if camera opened successfully
        if cap.isOpened() == False:
            print("Error opening video stream or file")

        # Read until video is completed
        while True:

            ret, frame = cap.read()  # Read frame from first video
            if ret:
                yield frame
            # Break the loop
            else:
                break
            # cv2.waitKey(100) #Wait 100msec (for debugging)

        cap.release()  # Release must be inside the outer loop

    def read_all_video_files_for_data_set_dir(self):
        """Returns a possibly empty list of the paths of the images for the given data_set_dir.

        Returns
        -------
        [str,...]
            A list of relative paths to the mp4 videos
        """
        path = Path.joinpath(Path(self.data_set_dir), ("*.mp4"))
        videos_ls = glob.glob(str(path))
        return videos_ls

    def read_all_frames_for_all_videos(self):
        """Reads all videos and their frames and returns a dictonary with them

        Returns
        -------
        {str : [gen], ...}
            A dictonary containing the videos as keys and a generator as values
        """
        v_ls = self.video_ls
        v_f_dic = {video: self.read_all_frames_for_one_video(video) for video in v_ls}

        return v_f_dic

    def get_resolution(self, relative_path_to_video):
        cap = cv2.VideoCapture(relative_path_to_video)
        if cap.isOpened():
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`

        return width, height

    def get_resolution_list(self, min, max):
        """Reads all videos and returns videos with a aspect ratio between a set range."

        Parameters
        ----------
        min : int
            Minimum aspect ratio
        max : int
            Maximum aspect ratio

        Returns
        -------
        list :
            A list of resolution objects, which contain the resolution, the aspect ratio and the number of videos with this resolution.,

        """

        v_ls = self.video_ls

        resolutions = [self.get_resolution(video) for video in v_ls]
        counted_resolutions = Counter((tuple(tup)) for tup in resolutions)

        resolution_list = []
        counter = 0

        for res, num in counted_resolutions.items():
            aspect_ratio = res[0] / res[1]

            if aspect_ratio > min and aspect_ratio < max:
                counter = counter + num
                """ resolution_list.append(
                    {
                        "resolution": str(res),
                        "aspect ratio": aspect_ratio,
                        "number of videos": num,
                    }
                ) """

        """ resolution_list = sorted(
            resolution_list, key=lambda res: res["number of videos"], reverse=True
        ) """

        return counter

    def rescale_video(self, cap, dim, crop_value, name):

        if cap.isOpened():
            ret, frame = cap.read()
            rescaled_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            croped_frame = rescaled_frame[
                crop_value[1] : (dim[1] - crop_value[1]),
                crop_value[0] : (dim[0] - crop_value[0]),
            ]
            (h, w) = croped_frame.shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter('data-rescaled//celeb-synthesis-720p//'+str(name)+'_720p.mp4',
                                    fourcc, 30.0,
                                    (w, h), True)

        # Check if camera opened successfully
        if cap.isOpened() == False:
            print("Error opening video stream or file")

        # Read until video is completed
        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:

                # Resize and crop frame
                rescaled_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                croped_frame = rescaled_frame[
                    crop_value[1] : (dim[1] - crop_value[1]),
                    crop_value[0] : (dim[0] - crop_value[0]),
                ]
                writer.write(croped_frame)
                # cv2.imshow("cropped", croped_frame)
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

    def rescaled_videos_list(self, min, max):

        video_ls = self.video_ls

        real_aspect_ratio = 1280 / 720
        video_rescale_dic = {}

        for video in video_ls:
            cap = cv2.VideoCapture(video)
            if cap.isOpened():
                video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
                video_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`

            video_ar = video_width / video_height

            dim = (int( video_width), int(video_height))
            crop_value = (0, 0)  # tuple with width, height for crop

            if video_ar > min and video_ar < max:
                name = video.split("\\")[-1].split(".")[0]
                print("video_aspect_ratio: ", video_ar)
                if real_aspect_ratio <= video_ar:
                    # change height to 720p and rescale & crop width
                    height = 720
                    width =  video_width * height / video_height
                    dim = (int(width), int(height))
                    crop_value = (int((width - 1280) / 2), 0)
                    print("Rescaled width: ", width - (crop_value[0] * 2), height)
                else:
                    # change width to 1280p and rescale & crop height
                    width = 1280
                    height = video_height * width / video_width
                    dim = (int(width), int(height))
                    crop_value = (0, int((height - 720) / 2))
                    print(crop_value)
                    print("Rescaled height: ", width, height - (crop_value[1] * 2))
                video_rescale_dic[video] = self.rescale_video(cap, dim, crop_value, name)
        return video_rescale_dic


if __name__ == "__main__":
    rel_path_video = "./data/Celeb-real/id0_0002.mp4"
    data_set_celb_real_dir = "./data/Celeb-synthesis"

    # extract_multiple_videos(rel_path_video)
    # save_all_frames_for_one_video(rel_path_video)
    # raffov = read_all_frames_for_one_video(rel_path_video)
    # print(next(raffov))
    fr = FileReader(data_set_celb_real_dir)
    # test = fr.read_all_frames_for_all_videos()

    print("Number of videos that get resized: ", fr.get_resolution_list(1.75, 1.85))
    aspect_ratio = fr.rescaled_videos_list(1.75, 1.85)

    video_0 = list(aspect_ratio.keys())[0]

    [x for x in aspect_ratio[video_0]]
