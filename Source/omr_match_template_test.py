import sys
import cv2
import numpy as np

img = cv2.imread(sys.argv[1],0)
template = cv2.imread(sys.argv[2],0)

