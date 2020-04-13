# ENPM 809T
# Perception: Lane Detection

# Import packages
import numpy as np
import cv2
import imutils
import time

print("All packages imported properly!")
print(" ------ ")
print(" ")

# Snip/Region-of-Interest dimensions
aa = 300; bb = 250; cc = 50

# Snip region of interest in video frame
def snip_image(img):
    cv2.rectangle(img, (0, img.shape[0] - cc), (img.shape[1], img.shape[0] - aa), (0, 0, 255))
    snip = img[(img.shape[0] - aa):(img.shape[0] - cc), (0):(img.shape[1])]
    return snip

# Create & apply polygon (trapezoid) mask to selected region of interest
def mask_image(img):
    mask = np.zeros((img.shape[0], img.shape[1]), dtype="uint8")
    pts = np.array([[90, img.shape[0]-25], [90, img.shape[0]-35], [img.shape[1]/2-30, 100], [img.shape[1]/2+30, 100],
                    [img.shape[1]-90, img.shape[0]-35], [img.shape[1]-90, img.shape[0]-25]], dtype=np.int32)
    cv2.fillConvexPoly(mask, pts, 255)
    masked = cv2.bitwise_and(img, img, mask=mask)
    return masked

# Mask frame for color of lane lines, convert to grayscale then black/white to binary image
def thres_image(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    whiteLower = np.array([30, 0, 65]); whiteUpper = np.array([255, 255, 150])
    white_mask = cv2.inRange(hsv, whiteLower, whiteUpper)
    frame = cv2.bitwise_or(gray, white_mask)
    thresh = 100
    frame = cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)[1]
    return frame

# Blur image to assist edge detection
def blur_image(img):
    return cv2.GaussianBlur(img, (21, 21), 0)   # (img, kernel size)

# Identify edges & show on screen
def edge_image(img):
    return cv2.Canny(img, 30, 150)  # (img, low thresh, high thres)

# Perform full Hough Transform to identify all possible lane lines
def line_image(img):
    return cv2.HoughLines(img, 1, np.pi / 180, 30)

# plot all lane lines (FOR DEMO PURPOSES ONLY)
def plot_Hough_lines(img, rho, theta):
    a = np.cos(theta); b = np.sin(theta)
    x0 = a * rho; y0 = b * rho
    x1 = int(x0 + 1000 * (-b)); y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b)); y2 = int(y0 - 1000 * (a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
    cv2.line(img, (0, 0), (x0, y0), (0, 255, 255), 1)  # plots perpendicular line
    cv2.circle(img, (x0, y0), 10, (0, 255, 0), -1)
    cv2.circle(img, (x1, y1), 10, (200, 255, 0), -1)
    snipp = cv2.circle(img, (x2, y2), 10, (200, 255, 0), -1)
    return snipp

# Identify left/right lane lines by selecting the median line found in Hough transform
def median(array):
    return np.median(array)

# Plot left lane line (red)
def plot_median_left_line(img, left_rho, left_theta):
    a = np.cos(left_theta); b = np.sin(left_theta)
    x0 = a * left_rho - 70  # 70 = frame.shape[1]/2 - bb   UPDATE THIS MATH!!
    y0 = b * left_rho + 180  # 180 = frame.shape[0] - aa   UPDATE THIS MATH!!
    x1 = int(x0 + 1000 * (-b)) + img.shape[1] / 2 - bb; y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b)) + img.shape[1] / 2 - bb; y2 = int(y0 - 1000 * (a))
    return (x1, y1, x2, y2)

# Plot right lane line (red)
def plot_median_right_line(img, right_rho, right_theta):
    a = np.cos(right_theta); b = np.sin(right_theta)
    x0 = a * right_rho + 0   # 70 = frame.shape[1]/2 - bb
    y0 = b * right_rho + 180  # 180 = frame.shape[0] - aa
    x3 = int(x0 + 1000 * (-b)); y3 = int(y0 + 1000 * (a))
    x4 = int(x0 - 1000 * (-b)); y4 = int(y0 - 1000 * (a))
    return (x3, y3, x4, y4)

# Plot boundary of lane (green)
def plot_final_lines(img, x1, y1, x2, y2, x3, y3, x4, y4):
    # generate y = m * x + b lines
    slope_left = (y2 - y1) / (float(x2) - float(x1))
    b_left = y2 - slope_left * x2
    x6 = 0; y6 = slope_left * x6 + b_left
    x7 = img.shape[1] / 2 - 100; y7 = slope_left * x7 + b_left
    slope_right = (y4 - y3) / (float(x4) - float(x3))
    b_right = y4 - slope_right * x4
    x8 = img.shape[1] / 2 + 100; y8 = slope_right * x8 + b_right
    x9 = img.shape[1] + 200; y9 = slope_right * x9 + b_right
    #create a copy of the original:
    overlay = img.copy()
    # generate polygon that is the lane itself
    pts = np.array([[x6, y6], [x7, y7], [x8, y8], [x9, y9]], dtype=np.int32)
    cv2.fillConvexPoly(img, pts, (0, 255, 0))
    # blend with the original:
    opacity = 0.6
    cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)
    # draw lane lines on top of lane
    cv2.line(img, (int(x6), int(y6)), (int(x7), int(y7)), (0, 0, 255), 16)
    cv2.line(img, (int(x8), int(y8)), (int(x9), int(y9)), (0, 0, 255), 16)
    opacity = 0.4
    overlay = cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)
    return overlay

def main():
	print("Here we go!")

	# Identify image & make a copy
	frame = cv2.imread('ENPM809Ttestimage.jpg')
	cv2.imshow("Original Frame", frame)
	final_output = frame.copy()

	snip = snip_image(frame)
	#cv2.imshow("Region of Interest", frame)
	#cv2.imshow("Snip", snip)

	masked = mask_image(snip)
	#cv2.imshow("Masked", masked)

	frame = thres_image(masked)
	#cv2.imshow("Thresholded to B/W", frame)

	blurred = blur_image(frame)
	#cv2.imshow("Blurred", blurred)

	edged = edge_image(blurred)
	#cv2.imshow("Edged", edged)

	lines = line_image(edged)

	# initialize arrays for left and right lanes
	rho_left = []; theta_left = []; rho_right = []; theta_right = []

	# ensure cv2.HoughLines found at least one line
	if lines is not None:

		# loop through all of the lines found by cv2.HoughLines
		for i in range(0, len(lines)):

			# evaluate each row of cv2.HoughLines output 'lines'
			for rho, theta in lines[i]:

				# collect LEFT lanes
				if theta < np.pi * 0.4 and theta > np.pi * 0.2:
				# if rho > 0:
					rho_left.append(rho); theta_left.append(theta)
					#snipp = plot_Hough_lines(snip, rho, theta)
					#cv2.imshow("Left Hough Lines!", snipp)

				# collect RIGHT lanes
				if theta > np.pi * 0.6 and theta < np.pi * 0.8:
				# if rho < 0:
					rho_right.append(rho); theta_right.append(theta)
					#snipp = plot_Hough_lines(snip, rho, theta)
					#cv2.imshow("Right Hough Lines!", snipp)

	# statistics to identify median lane dimensions
	left_rho = median(rho_left); left_theta = median(theta_left)
	right_rho = median(rho_right); right_theta = median(theta_right)

	# plot median lanes on top of scene snip
	if left_theta < np.pi * 0.4 and left_theta > np.pi * 0.2:
	# if left_theta > np.pi / 4:
		(x1, y1, x2, y2) = plot_median_left_line(snip, left_rho, left_theta)

	if right_theta > np.pi * 0.6 and right_theta < np.pi * 0.8:
		(x3, y3, x4, y4) = plot_median_right_line(snip, right_rho, right_theta)

	# identify location of lane lines and lane boundary & plot on top of original frame
	final = plot_final_lines(final_output, x1, y1, x2, y2, x3, y3, x4, y4)
	#cv2.imshow("Original Video + Lanes Detected", final)

	# press any key to end the script
	cv2.waitKey(0)

	print("Thanks for playing!")

if __name__ == '__main__':
	main()
