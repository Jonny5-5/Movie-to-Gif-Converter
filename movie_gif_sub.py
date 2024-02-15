import os
import argparse

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

name = None
movie_path = None
subtitle_path = None
output_dir_no_subs = "output/gifs/"
interval_gif = 3  # seconds
gif_width = 640
gif_height = 360


def parse_args():
    parser = argparse.ArgumentParser(description="Process movie and subtitle paths.")
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        required=True,
        help="Name of the movie.",
    )
    parser.add_argument(
        "-m",
        "--movie_path",
        type=str,
        required=True,
        help="Path to the movie file.",
    )
    parser.add_argument(
        "-s",
        "--subtitle_path",
        type=str,
        required=True,
        help="Path to the subtitle file.",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        required=False,
        help="Interval of time for each GIF clip.",
    )

    # Set the values of the global variables
    global name
    global movie_path
    global subtitle_path

    args = parser.parse_args()

    name = args.name
    movie_path = args.movie_path
    subtitle_path = args.subtitle_path
    if args.interval != None:
        global interval_gif
        interval_gif = args.interval


def get_subtitle_video(movie_path, subtitle_path, name) -> str:
    # Load the video clip
    video_clip = VideoFileClip(movie_path, audio=False)

    # Get the subtitles
    subtitles = get_subtitles(subtitle_path)

    # Export the video
    final = CompositeVideoClip(
        [video_clip, subtitles],
        size=(gif_width, gif_height),
    )
    filename = f"tmp/{name}_tmp.mp4"
    final.write_videofile(
        filename=filename,
        fps=video_clip.fps,
    )

    # Close the video_clip
    video_clip.close()

    # Return the filename
    return filename


def get_subtitles(path: str) -> SubtitlesClip:
    # Load subtitles
    generator = lambda txt: TextClip(
        txt,
        font="Georgia-Regular",
        fontsize=24,
        color="yellow",
    )
    subtitles = SubtitlesClip(path, generator)
    subtitles = subtitles.set_position(("center", "bottom"))
    return subtitles


def video_into_gifs(name, video_path):
    # Output directory for GIFs with subtitles
    output_gifs_no_subs = "output/gifs/"
    output_gifs_with_subs = "output/gifs_subs/"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_gifs_no_subs):
        os.makedirs(output_gifs_no_subs)
    if not os.path.exists(output_gifs_with_subs):
        os.makedirs(output_gifs_with_subs)

    # Load the video clip
    video_with_subs = VideoFileClip(video_path)

    # Initialize the relevant variables
    segment_duration = interval_gif
    start_time = 0
    end_time = start_time + segment_duration
    gif_index = 0

    # Loop through the video
    while end_time < video_with_subs.duration:
        # Capture the segment from start_time to end_time
        segment = video_with_subs.subclip(start_time, end_time)

        # Generate the GIF file path
        gif_path = os.path.join(
            output_gifs_with_subs,
            f"{name}_{gif_index}.gif",
        )

        # Write the segment as a GIF
        segment.write_gif(gif_path, fps=10)  # Adjust the FPS as needed

        # Move to the next segment
        start_time = end_time
        end_time = start_time + segment_duration
        gif_index += 1

    # Close the video clip
    video_with_subs.close()


def process_video(name, movie_path, subtitle_path):
    # Make video with subtitles
    video_path = get_subtitle_video(movie_path, subtitle_path, name)

    # Parse into gifs
    video_into_gifs(name, video_path)


if __name__ == "__main__":
    parse_args()
    process_video(name, movie_path, subtitle_path)
