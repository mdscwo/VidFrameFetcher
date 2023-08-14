import os
import subprocess
import sys
from tqdm import tqdm

def get_video_duration(video_path):
    cmd = ["ffmpeg", "-i", video_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in result.stderr.split("\n"):
        if "Duration" in line:
            time_parts = line.split(",")[0].split("Duration:")[1].strip().split(":")
            hours, minutes, seconds = time_parts
            total_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
            return total_seconds
    return None

def main():
    video_file = input("Enter the path to the video file: ").strip('\"')
    output_dir = input("Enter the location where you'd like to save the screenshots: ").strip('\"')
    interval = int(input("Enter the interval (in seconds) between screenshots: "))

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get video duration
    video_duration = get_video_duration(video_file)
    if video_duration is None:
        print("Couldn't determine video duration. Exiting.")
        sys.exit(1)

    # Calculate the number of screenshots to be taken
    num_screenshots = int(video_duration) // interval

    # Take screenshots
    for i in tqdm(range(num_screenshots), desc="Extracting frames"):
        timestamp = i * interval
        output_file = os.path.join(output_dir, f"frame_{i:03d}.jpg")
        cmd = ["ffmpeg", "-ss", str(timestamp), "-i", video_file, "-vf", f"scale=-1:1080", "-vframes", "1", "-c:v", "mjpeg", "-an", output_file]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error on extracting frame {i}:")
            print(result.stderr)
            continue  # Continue to the next frame

if __name__ == "__main__":
    main()
