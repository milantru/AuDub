from ffmpeg_wrapper import ffmpeg_wrapper
from audio_separator import Separator
import os

def clean_up_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.startswith('.') and not file.endswith('.out.mp4'):
                file_path = os.path.join(root, file)
                os.remove(file_path)

def clean_up():
    clean_up_directory('data/output')
    clean_up_directory('data/output/split_audio')

def main():
    print("STAGE 0: Preparation.")
    file_name_tmp = "rezero_satella_arrival.mp4"

    base_path = "." # root of repo (it is assumed that the program is run from the root of repo)

    ffmpeg_path = os.path.join(base_path, os.path.normpath("src/third_party_sw/ffmpeg/bin/ffmpeg.exe"))
    ffmpeg = ffmpeg_wrapper(ffmpeg_path)

    print("STAGE 1: Extraction of audio from video.")
    input_video_path = os.path.join(base_path, os.path.normpath("data/input/" + file_name_tmp))
    output_dir = os.path.join(base_path, os.path.normpath("data/output"))
    audio_path, _, _ = ffmpeg.extract_audio_from_video(input_video_path, output_dir)

    print("STAGE 2: Separation of background noise (music, sound...) and voices.")
    split_audio_dir = os.path.join(os.path.abspath(output_dir), "split_audio")

    separator = Separator(audio_path, output_dir=split_audio_dir)

    audio_instrumentals_filename, audio_vocals_filename = separator.separate()
    
    audio_instrumentals_file_path = os.path.join(split_audio_dir, audio_instrumentals_filename)
    audio_vocals_file_path = os.path.join(split_audio_dir, audio_vocals_filename)

    """
    # Create annotated transcript (containing, apart from text, timestamps and speakers)
    # TODO nlp, use audio_vocals_file_path for creating transcript
    transcript_file_path = ...

    # Split audio to separate audio files by intervals (per speaker talking)
    split_audio_dir = os.path.join(output_dir, "split_audio")

    speakers_and_their_intervals = [
        # TODO from transcript_file_path get real speakers_and_their_intervals
        ["speaker_0", [ "HH:mm:ss", "HH:mm:ss", "HH:mm:ss"]],
        ["speaker_1", [ "HH:mm:ss", "HH:mm:ss"]]
    ]

    speakers_and_their_split_audio_files_paths = []
    for speaker_name, intervals  in speakers_and_their_intervals:
        speaker_dir = os.path.join(split_audio_dir, speaker_name)
        os.mkdir(speaker_dir)
        
        split_audio_files_paths = ffmpeg.split_audio_by_intervals(audio_vocals_file_path, intervals, speaker_dir)

        speakers_and_their_split_audio_files_paths.append([speaker_name, split_audio_files_paths])

    # Create voice model for each speaker
    for speaker_name, split_audio_files_paths in speakers_and_their_split_audio_files_paths:
        # TODO tortoise, create voice model for the speaker
        ...
    
    # Use models to read the transcript
    # TODO tortoise, let the model read the transcript from transcript_file_path

    # Replace audio in video with both background noise and new voices audio
    ffmpeg.replace_audio_in_video(input_video_path, audio_dub_path, audio_instrumentals_file_path, output_dir) 
    """
    input("------- PRESS ENTER TO START CLEAN UP -------")
    print("Starting clean up.")
    clean_up()
    print("Finished clean up.")

if __name__ == "__main__":
    main()
