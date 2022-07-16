import cv2
import os


def video_to_images(path, output_path):
    video = cv2.VideoCapture(path)
    fps = video.get(cv2.CAP_PROP_FPS)
    isTrue, frame = video.read()
    frame_count = 0

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    while isTrue:
        cv2.imwrite(f'{output_path}/{frame_count}.jpg', frame)
        isTrue, frame = video.read()
        frame_count += 1
    return fps


def images_to_video(frames, output_path, video_name, fps):

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    height, width, _ = frames[0].shape
    video = cv2.VideoWriter(
        f"{output_path}/{video_name}", fourcc=cv2.VideoWriter_fourcc(*"mp4v"), fps=fps, frameSize=(width, height))
    for frame in frames:
        video.write(frame)
    cv2.destroyAllWindows()
    video.release()


def flush_image_folder(image_folder):
    for file in os.listdir(image_folder):
        os.remove(os.path.join(image_folder, file))
    os.rmdir(image_folder)
    print("Flushed image folder")
    return True


def get_output_fps(fps):
    return 2 * fps - 1
