import cv2
def cropImg(x,y):
    img = cv2.imread("./Stitching.jpg")
    print(type(img))

    # Shape of the image
    print("Shape of the image", img.shape)

    # [rows, columns]
    crop = img[int((img.shape[0]-x)/2) : int(img.shape[0]-((img.shape[0]-x)/2)), int((img.shape[1]-y)/2) : int(img.shape[1]-((img.shape[1]-y)/2))]

    cv2.imshow('original', img)
    cv2.imshow('cropped', crop)
    cv2.imwrite('cropped.jpg',crop)
    print("Shape of the crop", crop.shape)
    cv2.waitKey(0)
    cv2.destroyAllWindows()