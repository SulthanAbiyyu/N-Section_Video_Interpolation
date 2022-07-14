from config.config_handler import load_config
from utils.video_image import video_to_images, images_to_video

PATH = load_config()['tests']['video'] + "dog.mp4"
video_to_images(PATH, "./output_images")
images_to_video("./output_images", "./output_video", "dog_reconstruct.mp4")
