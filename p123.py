import cv2
import numpy as np

# Set target size
width, height = 640, 360

# Load image
img = cv2.imread('/home/nivetheni/v2_framewise/QmdKF6j93gLo1Mo81RatCydjYHkCeos1Fyiwu2sZd8HbeV.jpg')

# Get current size
h, w, _ = img.shape

# Calculate padding
top = bottom = (height - h) // 2
left = right = (width - w) // 2

# Add black padding
color = [0, 0, 0] # Black
img_padded = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT,value=color)

# Resize image
img_resized = cv2.resize(img_padded, (width, height))

# Save image
cv2.imwrite('./resized_image2.jpg', img_resized)