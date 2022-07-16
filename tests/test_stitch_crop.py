from ninterpolation.utils.stitching import stitch
from ninterpolation.utils.crop_img import crop


def test_stitch():
    path = "./data/images/0.jpg"
    path2 = "./data/images/50.jpg"
    original_height, original_width = 720, 1280

    stitched = stitch(path, path2)
    assert stitched.shape[0] > original_height
    assert stitched.shape[1] > original_width


def test_crop():
    path = "./data/images/0.jpg"
    path2 = "./data/images/50.jpg"
    original_height, original_width = 720, 1280

    stitched = stitch(path, path2)
    cropped = crop(stitched, original_height, original_width)
    assert cropped.shape[0] == original_height
    assert cropped.shape[1] == original_width
