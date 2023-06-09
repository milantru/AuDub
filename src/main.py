from ffmpeg_wrapper import ffmpeg_wrapper
import os

def cleanup_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.startswith('.') and not file.endswith('.out.mp4'):
                file_path = os.path.join(root, file)
                os.remove(file_path)

def cleanup():
    cleanup_directory('data/output')
    cleanup_directory('data/output/split_audio')

def main():
    file_name_tmp = "rezero_satella_arrival.mp4"

    base_path = "." # root of repo (it is assumed that the program is run from the root of repo)

    ffmpeg_path = os.path.join(base_path, os.path.normpath("src/third_party_sw/ffmpeg/bin/ffmpeg.exe"))
    ffmpeg = ffmpeg_wrapper(ffmpeg_path)

    # Extract audio from video
    input_video_path = os.path.join(base_path, os.path.normpath("data/input/" + file_name_tmp))
    output_dir = os.path.join(base_path, os.path.normpath("data/output"))
    audio_path, _, _ = ffmpeg.extract_audio_from_video(input_video_path, output_dir)

    # Separate background noise (music, sound...) and voices
    # TODO UltimateVocalRemover, use audio_path for the separation
    audio_vocals_file_path, audio_instrumentals_file_path = os.path.abspath(output_dir), os.path.abspath(output_dir)
    print("This is temporary stopping point (until UVR part is implemented) so you can use UVR manually for separating background noise and voices using directories...")
    print("\n...INPUT:\n" + os.path.abspath(audio_path))
    print("\n...OUTPUT (for both vocals and instrumentals):\n" + audio_vocals_file_path)
    input("\n------- PRESS ENTER TO CONTINUE -------\n")
    
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

    # Merge new audio files (that were created by reading the transcript using voice models)
    # TODO ffmpeg
    audio_dub_path = ...

    # Replace audio in video with both background noise and new voices audio
    ffmpeg.replace_audio_in_video(input_video_path, audio_dub_path, audio_instrumentals_file_path, output_dir) 
    """
    input("------- PRESS ENTER TO START CLEAN UP -------")
    cleanup()

if __name__ == "__main__":
    main()
