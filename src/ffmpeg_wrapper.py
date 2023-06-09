import subprocess as sp
import os

class ffmpeg_wrapper():
    def __init__(self, ffmpeg_path):
        self.__ffmpeg_path = ffmpeg_path
    
    @staticmethod
    def _get_file_name_with_extension(file_path, new_extension):
        file_name_without_extension, _ = os.path.splitext(os.path.basename(file_path))

        return file_name_without_extension + new_extension

    def replace_audio_in_video(self, video_file_path, audio_vocals_file_path, audio_instrumentals_file_path, output_dir):
        output_file_name = ffmpeg_wrapper._get_file_name_with_extension(video_file_path, ".out.mp4")

        output_file_path = os.path.join(output_dir, output_file_name)
        
        args = f"-i \"{video_file_path}\" -i \"{audio_vocals_file_path}\" -i \"{audio_instrumentals_file_path}\" -filter_complex \"[0:a]volume=1.0[a0]; [1:a]volume=0.5[a1]; [2:a]volume=0.5[a2]; [a0][a1][a2]amix=inputs=3:duration=first\" -map 0:v -map \"[out]\" -c:v copy \"{output_file_path}\""
        
        stdout, stderr = self.execute(args)

        return stdout, stderr

    def split_audio_by_intervals(self, audio_file_path, intervals, output_dir):
        split_audio_files_paths = []

        for i, interval in intervals:
            start_time, end_time = interval.split(" ") # expects HH:mm:ss format

            split_audio_file_path = os.path.join(output_dir, f"{i}-{os.path.basename(audio_file_path)}")

            # NOTE originally was -t {(endTime - startTime).TotalSeconds} instead -to
            args = f"-i \"{audio_file_path}\" -ss {start_time} -to {end_time} \"{split_audio_file_path}\""

            self.execute(args)

            split_audio_files_paths.append(split_audio_file_path)

        return split_audio_files_paths

    # def replace_audio_in_video(self, audio_file_path, video_file_path, output_dir):
    #     audio_file_name = os.path.basename(video_file_path)

    #     args = f"-i \"{video_file_path}\" -i \"{audio_file_path}\" -c:v copy -map 0:v:0 -map 1:a:0 {os.path.join(output_dir, audio_file_name)}"
        
    #     stdout, stderr = self.execute(args)

    #     return stdout, stderr

    def extract_audio_from_video(self, input_video_path, output_dir):
        output_file_name = ffmpeg_wrapper._get_file_name_with_extension(input_video_path, ".wav")

        output_audio_path = os.path.join(output_dir, output_file_name)
        
        args = f"-i \"{input_video_path}\" -vn -acodec pcm_s16le -ar 44100 -ac 2 \"{output_audio_path}\""
        
        stdout, stderr = self.execute(args)

        return output_audio_path, stdout, stderr

    def execute(self, args):
        command = f"{self.__ffmpeg_path} {args}"

        process = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        
        stdout, stderr = process.communicate()

        return stdout, stderr
