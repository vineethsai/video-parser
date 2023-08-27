import cv2
import numpy as np
import concurrent.futures

def is_red_color(pixel):
    lower_red = np.array([0, 0, 100])
    upper_red = np.array([100, 100, 255])

    return cv2.inRange(pixel, lower_red, upper_red)

def calculate_average_red_pixels(frame):
    red_mask = is_red_color(frame)
    red_pixel_count = np.count_nonzero(red_mask)
    total_pixels = frame.shape[0] * frame.shape[1]
    average_red_ratio = red_pixel_count / total_pixels
    return average_red_ratio

def process_frame(frame, frame_count):
    if frame_count % 100 == 0:
        average_red_ratio = calculate_average_red_pixels(frame)
        print("here")
        if average_red_ratio > 0.0001:

            screenshot_name = f'./screenshots/screenshot_{frame_count:03d}.png'
            cv2.imwrite(screenshot_name, frame)
            print(f'Saved {screenshot_name}')

def main():
    video_path = '../gcpn_1.mov'
    capture = cv2.VideoCapture(video_path)

    screenshot_counter = 0
    frame_count = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            ret, frame = capture.read()

            if not ret:
                break

            frame_count += 1

            if frame_count % 1000 == 0:
                executor.submit(process_frame(frame, frame_count))

    capture.release()

if __name__ == "__main__":
    main()
