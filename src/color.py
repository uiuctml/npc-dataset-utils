import cv2
import header
import random
import numpy as np

CRITERIA_MAX_ITER = 100
CRITERIA_EPSILON = 1.0
k = 3
ATTEMPTS = 100
RGB_THRESHOLD = 35

# Dataset-wide approach - corruptColor MUST take average_brightness passed from corrupt.py
def normalizeBrightness(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    local_brightness = np.mean(v)
    ratio = header.corrupt_mean_brightness / local_brightness
    v = np.clip(v * ratio, 0, 255).astype(np.uint8)
    adjusted_hsv = cv2.merge([h, s, v])
    adjusted_image = cv2.cvtColor(adjusted_hsv, cv2.COLOR_HSV2BGR)
    return adjusted_image

def clusterId(label):
    # find the most frequent cluster_id & its frequency
    unique, frequency = np.unique(label, return_counts = True)
    index = np.argmax(frequency)
    cluster_id = unique[index]
    cluster_freq = frequency[index]

    # check the pixel position variance of the cluster
    width, height = label.shape
    center = (width//2, height//2)

    cluster_id_var = []

    for (id, freq) in zip(unique, frequency):
        cluster_var = 0
        for i in range(width):
            for j in range(height):
                if label[i, j] == id:
                    cluster_var += ((abs(i-center[0]) + abs(j-center[1]))**2)**(1/2)
        cluster_var //= freq
        cluster_id_var.append((id, cluster_var))

    cluster_id_var.sort(key=lambda x: x[1])

    # the cluster_id pixel has too large variance
    if cluster_id == cluster_id_var[-1][0]:
        indices = np.argsort(frequency)
        cluster_id = indices[-2]
        cluster_freq = frequency[cluster_id]

    return cluster_id, cluster_freq

def modifyColor(image, cluster_id, cluster_freq, label):
    width, height, channel = image.shape

    # calculate the average RBG value of cluster_id pixels
    average_rgb = np.array([0, 0, 0])
    for i in range(width):
        for j in range(height):
            if label[i, j] == cluster_id:
                average_rgb += image[i, j]
    average_rgb //= cluster_freq

    # find max RGB value and its index
    max_rgb = max(average_rgb)
    max_rgb_index = average_rgb.argmax()

    # R has the max value, swap R with G/B
    if max_rgb_index == 0 and max_rgb - average_rgb[1] > RGB_THRESHOLD and max_rgb - average_rgb[2] > RGB_THRESHOLD:
        rgb_index = random.choice([1, 2])
        for i in range(width):
            for j in range(height):
                if label[i, j] == cluster_id:
                    image[i, j][0], image[i, j][rgb_index] = image[i, j][rgb_index], image[i, j][0]
    # G has the max value, swap G with R/B
    elif max_rgb_index == 1 and max_rgb - average_rgb[0] > RGB_THRESHOLD and max_rgb - average_rgb[2] > RGB_THRESHOLD:
        rgb_index = random.choice([0, 2])
        for i in range(width):
            for j in range(height):
                if label[i, j] == cluster_id:
                    image[i, j][1], image[i, j][rgb_index] = image[i, j][rgb_index], image[i, j][1]
    # B has the max value, swap B with R/G
    elif max_rgb_index == 2 and max_rgb - average_rgb[0] > RGB_THRESHOLD and max_rgb - average_rgb[1] > RGB_THRESHOLD:
        rgb_index = random.choice([0, 1])
        for i in range(width):
            for j in range(height):
                if label[i, j] == cluster_id:
                    image[i, j][2], image[i, j][rgb_index] = image[i, j][rgb_index], image[i, j][2]
    # RGB have roughly same value
    else:
        rgb_indices = random.sample([0, 1, 2], 2)
        for i in range(width):
            for j in range(height):
                if label[i, j] == cluster_id:
                    image[i, j][rgb_indices[0]] = 0
                    image[i, j][rgb_indices[1]] = 0

    return

def corruptColor(image):
    image = np.array(image)
    image_normalized = normalizeBrightness(image)

    # vectorized the image
    vectorized = image_normalized.reshape((-1, 3))
    vectorized = np.float32(vectorized)

    # k-means clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, CRITERIA_MAX_ITER, CRITERIA_EPSILON)
    ret, label, center = cv2.kmeans(vectorized, k, None, criteria, ATTEMPTS, cv2.KMEANS_PP_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]

    # find the cluster_id of background color
    label = label.reshape((image.shape[:2]))
    cluster_id, cluster_freq = clusterId(label)

    # # find the most frequent cluster_id & its frequency (original method)
    # unique, freq = np.unique(label, return_counts=True)
    # index = np.argmax(freq)
    # cluster_id = unique[index]
    # cluster_freq = freq[index]

    # modify the color
    label = label.reshape((image.shape[:2]))
    image_color_shifted = np.copy(image)
    modifyColor(image_color_shifted, cluster_id, cluster_freq, label)

    return image_color_shifted
