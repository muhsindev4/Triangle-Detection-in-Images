import cv2
import numpy as np

# Function to check if a contour is a triangle
def is_triangle(contour):
    # Approximate contour using Douglas-Peucker algorithm
    epsilon = 0.03 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # Check if the contour has 3 vertices
    if len(approx) == 3:
        return True
    else:
        return False

# Function to check if a triangle is upward or downward
def triangle_orientation(contour):
    # Get the vertices of the triangle
    vertices = np.squeeze(contour)

    # Calculate the slopes of the sides of the triangle
    slope1 = (vertices[1][1] - vertices[0][1]) / (vertices[1][0] - vertices[0][0])
    slope2 = (vertices[2][1] - vertices[1][1]) / (vertices[2][0] - vertices[1][0])
    slope3 = (vertices[2][1] - vertices[0][1]) / (vertices[2][0] - vertices[0][0])

    # Determine the orientation based on the slopes
    if slope1 > 0 and slope2 > 0 and slope3 < 0:
        return "Upward"
    elif slope1 < 0 and slope2 < 0 and slope3 > 0:
        return "Downward"
    else:
        return "Unknown"

# Load the image
image = cv2.imread('image.png')  # replace the image

if image is None:
    print('Error: Could not load image')
else:
    # Preprocessing
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours in the image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check each contour for triangles
    for contour in contours:
        if is_triangle(contour):
            orientation = triangle_orientation(contour)
            print(f'Triangle found! Orientation: {orientation}')
            # You can further process the triangle contour here
            # For example, draw it on the image
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

    # Display the image with detected triangles
    cv2.imshow('Image with Triangles', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
