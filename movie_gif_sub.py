import os
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip


# Path to the video file
video_path = "supersuit.mp4"

# Subtitles file path (SubRip format)
subtitles_path = "supersuit.srt"

# Path to the ImageMagick binary (convert.exe on Windows)
# Replace 'path_to_convert_binary' with the actual path to the convert binary file
# Example: "C:/Program Files/ImageMagick/convert.exe"
# os.environ["IMAGEMAGICK_BINARY"] = r"D:\ImageMagick"


# Output directory for GIFs with subtitles
output_directory = "output_gifs_with_subtitles/"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Load the video clip
video_clip = VideoFileClip(video_path)

# Load subtitles
generator = lambda txt: TextClip(
    txt,
    font="Georgia-Regular",
    fontsize=24,
    color="yellow",
)
subtitles = SubtitlesClip(subtitles_path, generator)
subtitles = subtitles.set_position(("center", "bottom"))

# export the final video
video_with_subs = "supersuit_subs_bottom_center.mp4"
final = CompositeVideoClip([video_clip, subtitles])
final.write_videofile(filename=video_with_subs, fps=video_clip.fps)

# Close the old video_clip
video_clip.close()

# Load the video clip
video_with_subs = VideoFileClip(video_with_subs)

# Duration of the segment in seconds
segment_duration = 3

# Initialize starting time
start_time = 0

# Initialize end time
end_time = start_time + segment_duration

# Initialize GIF index
gif_index = 0

# Loop through the video
while end_time < video_with_subs.duration:
    # Capture the segment from start_time to end_time
    segment = video_with_subs.subclip(start_time, end_time)

    # Generate the GIF file path
    gif_path = os.path.join(output_directory, f"segment_{gif_index}.gif")

    # Write the segment as a GIF
    segment.write_gif(gif_path, fps=10)  # Adjust the FPS as needed

    # Move to the next segment
    start_time = end_time
    end_time = start_time + segment_duration
    gif_index += 1

# Close the video clip
video_with_subs.close()
