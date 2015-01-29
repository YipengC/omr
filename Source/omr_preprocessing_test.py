import sys
import cv2
import omr_image_preprocessing

img = cv2.imread(sys.argv[1],0)

img = omr_image_preprocessing.process(img)

parsedFilePath = sys.argv[1].split('/')
imageName = parsedFilePath[-1].split('.')[0]
cv2.imwrite('test_preprocessing_output_' + imageName + '.png',img)
