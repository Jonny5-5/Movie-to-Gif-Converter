from moviepy.editor import VideoFileClip
import os

# Path to the video file
video_path = "supersuit.mp4"

# Output directory for GIFs
output_directory = "output_gifs/"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Load the video clip
clip = VideoFileClip(video_path)

# Duration of the segment in seconds
segment_duration = 3

# Initialize starting time
start_time = 0

# Initialize end time
end_time = start_time + segment_duration

# Initialize GIF index
gif_index = 0

# Loop through the video
while end_time < clip.duration:
    # Capture the segment from start_time to end_time
    segment = clip.subclip(start_time, end_time)

    # Generate the GIF file path
    gif_path = os.path.join(output_directory, f"segment_{gif_index}.gif")

    # Write the segment as a GIF
    segment.write_gif(gif_path, fps=10)  # Adjust the FPS as needed

    # Move to the next segment
    start_time = end_time
    end_time = start_time + segment_duration
    gif_index += 1

# Close the video clip
clip.close()
