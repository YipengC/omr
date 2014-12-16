import cv2

def threshold(img):
	return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,99,2)

# Output image
"""
parsedFilePath = sys.argv[1].split('/')
imageName = parsedFilePath[-1].split('.')[0]
cv2.imwrite('binary_' + imageName + '.png',img)
"""
