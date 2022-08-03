from config.config_handler import load_config
from utils.video_image import video_to_images, images_to_video, flush_image_folder, get_output_fps
from utils.crop_img import crop
from utils.stitching import stitch

from tqdm import tqdm
import cv2
import os


def images_path_gen(total_img, OUTPUT_IMAGE_PATH):
    for i in range(total_img):
        yield f"{OUTPUT_IMAGE_PATH}/{i}.jpg"


def images_cv2_gen(img):
    yield cv2.imread(img)


def ninterpolation(PATH, OUTPUT_VIDEO_PATH, FILE_NAME):
    OUTPUT_IMAGE_PATH = "./temp_img"
    print(f"""
    Video Path          : {PATH}
    Output Video Path   : {OUTPUT_VIDEO_PATH}
    Output Name         : {FILE_NAME}
    """)
    fps = video_to_images(PATH, OUTPUT_IMAGE_PATH)

    images = images_path_gen(
        len(os.listdir(OUTPUT_IMAGE_PATH)), OUTPUT_IMAGE_PATH)
    current_image = next(images)

    height, width, _ = cv2.imread(current_image).shape
    cropped = []

    print("stitching and cropping..")

    next_image = next(images)
    stitched = stitch(current_image, next_image)
    cropped.append(crop(stitched, height, width))
    current_image = next_image

    for next_image in tqdm(images, total=len(os.listdir(OUTPUT_IMAGE_PATH))):
        stitched = stitch(current_image, next_image)
        cropped.append(crop(stitched, height, width))
        current_image = next_image

    images = images_path_gen(
        len(os.listdir(OUTPUT_IMAGE_PATH)), OUTPUT_IMAGE_PATH)

    images_cv2 = images_cv2_gen(next(images))
    current_image_cv2 = next(images_cv2)

    all_images = []
    total_length = len(cropped) + len(os.listdir(OUTPUT_IMAGE_PATH))

    crop_counter = 0

    print("merging frames..")
    for i in tqdm(range(1, total_length)):
        if i % 2 != 0:
            all_images.append(current_image_cv2)
            current_image_cv2 = next(images_cv2_gen(next(images)))

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
    ninterpolation(PATH, OUTPUT_VIDEO_PATH, "scene_intepolated_gen.mp4")
