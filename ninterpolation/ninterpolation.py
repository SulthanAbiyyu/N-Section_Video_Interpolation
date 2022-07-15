from config.config_handler import load_config
from utils.video_image import video_to_images, images_to_video
from utils.crop_img import crop
from utils.stitching import stitch

import cv2

PATH = load_config()['tests']['video'] + "dog.mp4"
OUTPUT_IMAGE_PATH = load_config()['output']['image']
OUTPUT_VIDEO_PATH = load_config()['output']['video']
# video_to_images(PATH, OUTPUT_IMAGE_PATH)
# images_to_video(OUTPUT_IMAGE_PATH, OUTPUT_VIDEO_PATH, "dog_reconstruct.mp4")

stitched = stitch("./output_images/0.jpg", "./output_images/20.jpg")

crop = crop(stitched, 720, 1280)

print(stitched.shape)
print(crop.shape)
