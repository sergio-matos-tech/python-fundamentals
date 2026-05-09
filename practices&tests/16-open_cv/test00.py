import cv2
import random
import os

path = 'assets/logo.jpg'

if not os.path.exists(path):
    raise FileNotFoundError(f"File not found: {path}")

image = cv2.imread(path, -1)

if image is None:
    raise ValueError("Failed to load image.")

print(type(image))
print(image.shape)

for i in range(min(100, image.shape[0])):
    for j in range(image.shape[1]):
        image[i, j] = [
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        ]

cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

