import os

from ninterpolation.utils.video_image import video_to_images, images_to_video, flush_image_folder


def test_video_image():
    path = "./data/videos/dog.mp4"
    output_image_path = "./tests/test_images"
    output_video_path = "./tests/test_videos"

    fps = video_to_images(path, output_image_path)

    assert os.path.exists(output_image_path)
    assert round(fps, 2) == 29.97
    assert len(os.listdir(output_image_path)) > 300

    images_to_video(output_image_path, output_video_path, "dog_video.mp4", fps)

    assert os.path.exists(output_video_path)
    assert os.path.exists(f"{output_video_path}/dog_video.mp4")

    flush_image_folder(output_image_path)
    assert not os.path.exists(output_image_path)

    os.remove(f"{output_video_path}/dog_video.mp4")
    os.rmdir(output_video_path)
