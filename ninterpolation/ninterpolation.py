from config.config_handler import load_config
from utils.video_image import video_to_images, images_to_video, flush_image_folder, get_output_fps
from utils.crop_img import crop
from utils.stitching import stitch

from tqdm import tqdm
import cv2
import os


def ninterpolation(PATH, OUTPUT_VIDEO_PATH, FILE_NAME):
    OUTPUT_IMAGE_PATH = "./temp_img"
    print(f"""
    Video Path          : {PATH}
    Output Video Path   : {OUTPUT_VIDEO_PATH}
    Output Name         : {FILE_NAME}
    """)
    fps = video_to_images(PATH, OUTPUT_IMAGE_PATH)
    images = [img for img in os.listdir(
        OUTPUT_IMAGE_PATH) if img.endswith(".jpg")]
    images.sort(key=lambda x: int(x.split('.')[0]))

    height, width, _ = cv2.imread(
        os.path.join(OUTPUT_IMAGE_PATH, images[0])).shape
    cropped = []

    print("stitching and cropping..")
    for i in tqdm(range(len(images))):
        if i != (len(images) - 1):
            stitched = stitch(os.path.join(OUTPUT_IMAGE_PATH, images[i]), os.path.join(
                OUTPUT_IMAGE_PATH, images[i + 1]))

            cropped.append(crop(stitched, height, width))

    images_cv2 = [cv2.imread(os.path.join(OUTPUT_IMAGE_PATH, img))
                  for img in images]

    all_images = []
    total_length = len(cropped) + len(images_cv2)

    crop_counter = 0
    ori_counter = 0

    print("merging frames..")
    for i in tqdm(range(1, total_length)):
        if i % 2 != 0:
            all_images.append(images_cv2[ori_counter])
            ori_counter += 1
        else:
            all_images.append(cropped[crop_counter])
            crop_counter += 1

    print("converting images to video..")
    images_to_video(all_images, OUTPUT_VIDEO_PATH,
                    FILE_NAME, get_output_fps(fps))

    print("deleting image folder..")
    flush_image_folder(OUTPUT_IMAGE_PATH)


if __name__ == '__main__':
    PATH = load_config()['tests']['video'] + "scene.mp4"
    OUTPUT_VIDEO_PATH = load_config()['output']['video']
    ninterpolation(PATH, OUTPUT_VIDEO_PATH, "scene_intepolated.mp4")
