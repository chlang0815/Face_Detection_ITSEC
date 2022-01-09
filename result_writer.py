from os import write
from pathlib import Path
class ResultWriter():
    def __init__(self, rel_path_to_results) -> None:
        """Writes the results to files that are created at the specified relative path.

        Parameters
        ----------
        rel_path_to_results : str
            Relative pathe where the results should be saved
        """
        self.rel_path_to_results = Path(rel_path_to_results)
        
    def create_folder_if_not_exist(self, rel_path):
        """Creates the folder/folders if no folder/folders exists at rel_path.

        Parameters
        ----------
        rel_path : str
            The path to create if the path does not exist
        """
        if not Path.is_dir(rel_path):
            Path.mkdir(rel_path, parents=True)
    
    def write_down_the_dic(self,dictonary):
        """Writes the dictonary to a file named result_dictonary.txt in rel_path_to_results

        Parameters
        ----------
        dictonary : dict
            A dictonary with the form {video:{frame: resultlist},...}
            video: relative path to the image
            frame: the current frame 
            resultlist: the list of the result/s of the current frame
        """
        write_path = Path.joinpath(self.rel_path_to_results,'result_dictonary.txt')
        rdw = open( write_path, "a+")
        for video, frame in dictonary.items():
            rdw.write(f"video={video}\n")
            for frame_number, result_ls in frame.items():
                rdw.write(f"frame_number:{frame_number}\n")
                for result in result_ls:
                    rdw.write(f"{result}\n")
        rdw.close()
    def write_down_the_time_dic(self,time_dictonary):
        write_path = Path.joinpath(self.rel_path_to_results,'result_time_dictonary.txt')
        rdw = open(write_path,"a+")
        for video, frame in time_dictonary.items():
            rdw.write(f"video={video}\n")
            for fr,frame_time in frame.items():
                rdw.write(f"{fr} = {frame_time}\n")

        rdw.close()
       
    def write_down_hit_and_no_hit_file(self,dictonary):
        """Creates the results for the dictonary and writes them to a specific file in rel_path_to_results.
        The specific files are hit_file.txt, no_file.txt, eval.txt, and detailed_eval_file.txt
        hit_file.txt: Contains all the hits ( A hit is defined as the detection of only one result in the frame.)
        no_file.txt: Contains all the misses (A miss is defined iff the detection is not a hit.)
        eval.txt: Counts the number of hits and the number of misses of the whole dictonary
        detailed_eval_file.txt :  Counts the number of hits and the number of misses of each frame and writes them separately for each video.

        Parameters
        ----------
        dictonary : dict
            A dictonary with the form {video:{frame: resultlist},...}
            video: relative path to the image
            frame: the current frame 
            resultlist: the list of the result/s of the current frame
        """
        write_path_hf = Path.joinpath(self.rel_path_to_results,'hit_file.txt')
        write_path_nhf = Path.joinpath(self.rel_path_to_results,'no_hit_file.txt')
        write_path_ef = Path.joinpath(self.rel_path_to_results,'eval_file.txt')
        write_path_devf = Path.joinpath(self.rel_path_to_results,'detailed_eval_file.txt')
        counter_hit = 0
        counter_no_hit = 0
        hf = open( write_path_hf, "a+")
        nhf = open( write_path_nhf, "a+")
        ef = open( write_path_ef, "a+")
        devf = open(write_path_devf, "a+")
        for video, frame in dictonary.items():
            counter_hit_per_video = 0 
            counter_no_hit_per_video = 0
            for frame_number, result_ls in frame.items():
                len_results = len(result_ls)
                if (len_results == 1):
                    hf.write(f"video:{video};frame_number:{frame_number};result:{result_ls[0]}\n")
                    counter_hit += 1
                    counter_hit_per_video += 1 

                else:
                    write_str_no_hit = f"video:{video};frame_number:{frame_number};result:["
                    for result in result_ls:
                        write_str_no_hit +=f"{result},"
                    write_str_no_hit = write_str_no_hit[:-1]
                    write_str_no_hit += "]\n"
                    nhf.write(write_str_no_hit)
                    counter_no_hit += 1
                    counter_no_hit_per_video += 1
            detailed_eval_video_str = f"video:{video};counter_hit_per_video:{counter_hit_per_video};counter_no_hit_per_video:{counter_no_hit_per_video};number_of_frames:{len(frame)}\n"
            devf.write(detailed_eval_video_str)
        ef.write(f"counter_no_hit ={counter_no_hit}, counter_hit = {counter_hit}")
        hf.close()
        nhf.close()
        ef.close()
    def write_results_to_path(self, dictonary):
        """Calls all the write functions.

        Parameters
        ----------
        dictonary : dict
            A dictonary with the form {video:{frame: resultlist},...}
            video: relative path to the image
            frame: the current frame 
            resultlist: the list of the result/s of the current frame
        """
        self.create_folder_if_not_exist(self.rel_path_to_results)
        self.write_down_the_dic(dictonary)
        self.write_down_hit_and_no_hit_file(dictonary)



