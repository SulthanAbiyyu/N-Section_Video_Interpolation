import cv2
import os


def video_to_images(path, output_path):
    video = cv2.VideoCapture(path)
    isTrue, frame = video.read()
    frame_count = 0

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    while isTrue:
        cv2.imwrite(f'{output_path}/{frame_count}.jpg', frame)
        isTrue, frame = video.read()
        frame_count += 1


def images_to_video(path, output_path, video_name):

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    images = [img for img in os.listdir(path) if img.endswith(".jpg")]
    images.sort(key=lambda x: int(x.split('.')[0]))
    frames = [cv2.imread(os.path.join(path, img)) for img in images]

    height, width, layers = frames[0].shape
    video = cv2.VideoWriter(
        f"{output_path}/{video_name}", fourcc=cv2.VideoWriter_fourcc(*"mp4v"), fps=29.97, frameSize=(width, height))
    for image, frame in zip(images, frames):
        print(image)
        video.write(frame)
    cv2.destroyAllWindows()
    video.release()


def flush_image_folder(image_folder):
    for file in os.listdir(image_folder):
        os.remove(os.path.join(image_folder, file))
    os.rmdir(image_folder)
    print("Flushed image folder")
    return True
