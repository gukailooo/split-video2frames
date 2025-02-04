import os
import numpy as np
import argparse
import cv2

def main():

    parser = argparse.ArgumentParser(description='Extract frames from a video at a specified interval.')
    parser.add_argument('source', type=str, help='Path to the source video file.')
    parser.add_argument('dest_folder', type=str, help='Path to the destination folder where frames will be saved.')
    parser.add_argument('--frame_interval', type=int, default=1, help='Interval between saved frames (e.g., 2 for every other frame). Defaults to 1 (every frame).')
    parser.add_argument('--prefix', type=str, default='frame', help='Prefix for the saved frame filenames. Defaults to "frame".')
    parser.add_argument('--image_format', type=str, default='jpg', help='Image format to save the frames in (jpg, png, etc.). Defaults to "jpg".')
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.source)
    if not cap.isOpened():
        print(f"Error: Could not open video file: {args.source}")
        return

    dest_folder = os.path.abspath(args.dest_folder)  # Use a better variable name and ensure absolute path
    os.makedirs(dest_folder, exist_ok=True) # Create the destination directory if it doesn't exist

    frame_interval = args.frame_interval
    prefix = args.prefix
    image_format = args.image_format
    
    frame_count = 0
    saved_frame_count = 0  # Keep track of the actual number of frames saved



    while(True):
        ret, frame = cap.read()

        if not ret:
            print("End of video or error reading frame.")
            break

        if frame_count % frame_interval == 0:
            filename = f'{prefix}{saved_frame_count:06d}.{image_format}' # Format the filename with leading zeros
            filepath = os.path.join(dest_folder, filename)

            try:
                cv2.imwrite(filepath, frame)
                print(f'Saved: {filepath}')
                saved_frame_count += 1
            except Exception as e:
                print(f"Error saving frame: {e}")
                break  # Stop the loop if we can't save frames 

        frame_count += 1

    cap.release()
    print(f'Finished. Extracted {saved_frame_count} frames to {dest_folder}')


if __name__ == '__main__':
    main()