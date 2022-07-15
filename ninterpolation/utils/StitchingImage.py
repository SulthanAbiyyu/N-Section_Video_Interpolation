from multiprocessing import dummy
import sys
import cv2
import numpy as np
def stitchImg(image1,image2):
  img1 = cv2.imread(image1)
  img2 = cv2.imread(image2)
  img1 = cv2.resize(img1,(0,0),fx=0.4,fy=0.4)
  img2 = cv2.resize(img2,(0,0),fx=0.4,fy=0.4)
  img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
  img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

  cv2.imshow('img1',img1_gray)
  cv2.imshow('img2',img2_gray)


  orb = cv2.ORB_create(nfeatures=2000)

 
  keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
  keypoints2, descriptors2 = orb.detectAndCompute(img2, None)
  cv2.imshow('Keypointorb apalah',cv2.drawKeypoints(img1, keypoints1, None, (255, 0, 255)))
  cv2.imshow('Keypointorb apalah2',cv2.drawKeypoints(img2, keypoints2, None, (255, 0, 255)))


  bf = cv2.BFMatcher_create(cv2.NORM_HAMMING)


  matches = bf.knnMatch(descriptors1, descriptors2,k=2)

  print(keypoints1[0].pt)
  print(keypoints1[0].size)

  print("Descriptor of the first keypoint: ")
  print(descriptors1[0])



  def draw_matches(img1, keypoints1, img2, keypoints2, matches):
    r, c = img1.shape[:2]
    r1, c1 = img2.shape[:2]

 
    output_img = np.zeros((max([r, r1]), c+c1, 3), dtype='uint8')
    output_img[:r, :c, :] = np.dstack([img1, img1, img1])
    output_img[:r1, c:c+c1, :] = np.dstack([img2, img2, img2])


    for match in matches:
      img1_idx = match.queryIdx
      img2_idx = match.trainIdx
      (x1, y1) = keypoints1[img1_idx].pt
      (x2, y2) = keypoints2[img2_idx].pt


      cv2.circle(output_img, (int(x1),int(y1)), 4, (0, 255, 255), 1)
      cv2.circle(output_img, (int(x2)+c,int(y2)), 4, (0, 255, 255), 1)


      cv2.line(output_img, (int(x1),int(y1)), (int(x2)+c,int(y2)), (0, 255, 255), 1)
      
    return output_img

  all_matches = []
  for m, n in matches:
    all_matches.append(m)

  img3 = draw_matches(img1_gray, keypoints1, img2_gray, keypoints2, all_matches[:30])
  cv2.imshow('image Hasil?',img3)

  good = []
  for m, n in matches:
      if m.distance < 0.4 * n.distance:
          good.append(m)

  cv2.imshow('Bagus aja 1',cv2.drawKeypoints(img1, [keypoints1[m.queryIdx] for m in good], None, (255, 0, 255)))
  cv2.imshow('Bagus aja 2',cv2.drawKeypoints(img2, [keypoints2[m.queryIdx] for m in good], None, (255, 0, 255)))

  def warpImages(img1, img2, H):

    rows1, cols1 = img1.shape[:2]
    rows2, cols2 = img2.shape[:2]

    list_of_points_1 = np.float32([[0,0], [0, rows1],[cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2)
    temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2)

    list_of_points_2 = cv2.perspectiveTransform(temp_points, H)

    list_of_points = np.concatenate((list_of_points_1,list_of_points_2), axis=0)

    [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)
    
    translation_dist = [-x_min,-y_min]
    
    H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

    output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min))
    output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:cols1+translation_dist[0]] = img1

    return output_img

  MIN_MATCH_COUNT = 10

  if len(good) > MIN_MATCH_COUNT:

      src_pts = np.float32([ keypoints1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
      dst_pts = np.float32([ keypoints2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

      M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
      
      result = warpImages(img2, img1, M)

      cv2.imshow('Hasilnya mungkin',result)
      cv2.imwrite('Stitching.jpg',result)
  cv2.waitKey(0)