import sys
import cv2
import omr_threshold_image
import omr_classes
import omr_staff_line_detection
import omr_staff_line_removal

img = cv2.imread(sys.argv[1],0)

# Threshold
img = omr_threshold_image.threshold(img)

# Get staff line detection data
staffData = omr_staff_line_detection.getStaffData(img)

# Remove staff lines
img = omr_staff_line_removal.removeStaffLines(img,staffData)


