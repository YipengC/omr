import sys
import cv2
import omr_threshold_image
import omr_classes
import omr_staff_line_detection
import omr_staff_line_removal
import omr_recognition
import omr_reconstruction
import omr_bar_line_detection

img = cv2.imread(sys.argv[1],0)

# Threshold
img = omr_threshold_image.threshold(img)

# Copy of thresholded image for recognition output
imgRecognitionOutput = img.copy()
imgRecognitionOutput = cv2.cvtColor(imgRecognitionOutput,cv2.COLOR_GRAY2RGB)

# Get staff line detection data
staffData = omr_staff_line_detection.getStaffData(img)

# Remove staff lines
#img = omr_staff_line_removal.removeStaffLines(img,staffData)

# Test removeStaffLinesSP
img = omr_staff_line_removal.removeStaffLinesSP(img,staffData)
raw_input("Press Enter to continue...")

# Perform recognition
musicalObjects = omr_recognition.performRecognition(img,staffData)

# Save recognition output
for musicalObjectList in musicalObjects.values():
	for musicalObject in musicalObjectList:
		x,y = musicalObject.point
		w,h = musicalObject.dimensions
		cv2.rectangle(imgRecognitionOutput,(x,y),(x+w,y+h),(0,0,255),3)
parsedFilePath = sys.argv[1].split('/')
imageName = parsedFilePath[-1].split('.')[0]
cv2.imwrite('recognition_output_' + imageName + '.png',imgRecognitionOutput)

# Perform reconstruction
omr_reconstruction.performReconstruction(musicalObjects,staffData,imageName)
