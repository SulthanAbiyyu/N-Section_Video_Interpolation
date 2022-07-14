import cv2
import os


def video_to_images(path):
    video = cv2.VideoCapture(path)
    isTrue, frame = video.read()
    frame_count = 0
    while isTrue:
        cv2.imwrite(f'{frame_count}.jpg', frame)
        isTrue, frame = video.read()
        frame_count += 1


def images_to_video(path, video_name):
    images = [img for img in os.listdir(path) if img.endswith(".jpg")]
    frames = [cv2.imread(os.path.join(path, img)) for img in images]

    height, width, layers = frames[0].shape
    video = cv2.VideoWriter(
        video_name, 0, 1, (width, height))
    for frame in frames:
        video.write(frame)
    cv2.destroyAllWindows()
    video.release()
