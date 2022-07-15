import cv2


def crop(img, height, width):
    print("Shape of the image", img.shape)

    height_lower_bound = int((img.shape[0]-height)/2)
    height_upper_bound = int(img.shape[0]-((img.shape[0]-height)/2))
    width_lower_bound = int((img.shape[1]-width)/2)
    width_upper_bound = int(img.shape[1]-((img.shape[1]-width)/2))

    crop = img[height_lower_bound:height_upper_bound,
               width_lower_bound: width_upper_bound]

    return crop
    # cv2.imwrite(output_path, crop)
    # print("Shape of the crop", crop.shape)
    # cv2.destroyAllWindows()
