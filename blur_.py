# import cv2
# import numpy as np

# # Load the image
# image = cv2.imread("/home/nivetheni/combined_pipeline/cid_ref_full.jpg")

# # Define the bounding box
# x, y, w, h = 100, 100, 200, 200

# # Create a mask for the bounding box
# mask = np.zeros(image.shape[:2], dtype=np.uint8)
# cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

# # Apply Gaussian blur to the remaining areas
# blur = cv2.GaussianBlur(image, (51, 51), 0, mask=255-mask)

# # Show the result
# cv2.imshow("Original Image", image)
# cv2.imshow("Blurred Image", blur)
# cv2.waitKey(0)


import cv2
original = cv2.imread("/home/nivetheni/combined_pipeline/cid_ref_full.jpg", 3)
blurred = cv2.GaussianBlur(original, (25,25), 0)

original[0:500, 0:500] = blurred[0:360, 0:500]
cv2.imwrite('cvBlurredOutput.jpg', original)