import os
import argparse

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

from color_print import *


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
    # See if the file already exists
    tmp_filename = f"tmp/{name}_tmp.mp4"
    if os.path.exists(tmp_filename):
        print_colored(f"Tmp file already exists for {tmp_filename}", "cyan")
        return tmp_filename

    # Load the video clip
    video_clip = VideoFileClip(
        movie_path,
        audio=False,
        target_resolution=(gif_height, gif_width),
    )

    # Get the subtitles
    subtitles = get_subtitles(subtitle_path)

    # Export the video
    final = CompositeVideoClip([video_clip, subtitles])
    final.write_videofile(
        filename=tmp_filename,
        fps=video_clip.fps,
    )

    # Close the video_clip
    video_clip.close()

    # Return the filename
    return tmp_filename


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
    output_gifs_no_subs = f"output/gifs/{name}/"
    output_gifs_with_subs = f"output/gifs_subs/{name}/"

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
        # Adjust the FPS as needed
        # video_with_subs.write_gif()
        # Try different programs here ^ to see if one is faster
        segment.write_gif(gif_path, fps=10)

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


def show_pre_process_report():
    # Open the video file for getting duration
    video = VideoFileClip(movie_path)
    print_colored(f"Processing the file '{movie_path}'", "green")
    print_colored(
        f"\tDuration: {int(video.duration/60)}min {int(video.duration%60)}sec", "green"
    )
    print_colored(f"\tThe gifs will be named '{name}_000.gif'", "green")

    print()

    print_colored(f"Interval is {interval_gif} seconds", "blue")

    print()

    print_colored(
        f"This will make about \t {int(video.duration / interval_gif)} gifs!", "yellow"
    )
    print_colored(f"The gifs will be {gif_width}w X {gif_height}h", "yellow")

    print()

    # Don't forget to close the video file
    video.close()
    cont = input("Do you wish to continue? (y/n) ")
    if cont.lower() != "y":
        print_colored("Exiting.", "red")
        exit()
    else:
        print_colored("\nContinuing with gifs...\n", "green")


if __name__ == "__main__":
    parse_args()
    show_pre_process_report()
    process_video(name, movie_path, subtitle_path)
