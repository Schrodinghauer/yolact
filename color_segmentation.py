import numpy as np
import cv2
import os
import pdb

import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt



def make_histogram(cluster):
    """
    Count the number of pixels in each cluster
    :param: KMeans cluster
    :return: numpy histogram
    """
    numLabels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    hist, _ = np.histogram(cluster.labels_, bins=numLabels)
    hist = hist.astype('float32')
    hist /= hist.sum()
    return hist


def make_bar(height, width, color):
    """
    Create an image of a given color
    :param: height of the image
    :param: width of the image
    :param: BGR pixel values of the color
    :return: tuple of bar, rgb values, and hsv values
    """
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    hsv_bar = cv2.cvtColor(bar, cv2.COLOR_BGR2HSV)
    hue, sat, val = hsv_bar[0][0]
    return bar, (red, green, blue), (hue, sat, val)


def sort_hsvs(hsv_list):
    """
    Sort the list of HSV values
    :param hsv_list: List of HSV tuples
    :return: List of indexes, sorted by hue, then saturation, then value
    """
    bars_with_indexes = []
    for index, hsv_val in enumerate(hsv_list):
        bars_with_indexes.append((index, hsv_val[0], hsv_val[1], hsv_val[2]))
    bars_with_indexes.sort(key=lambda elem: (elem[1], elem[2], elem[3]))
    return [item[0] for item in bars_with_indexes]



def load_images_from_folder(folder):
	"""
	Load images by OpenCV. 
	:param folder: String, path of the source folder.
	:return: List of OpenCV images, List of filenames corresponding to the images.
	"""
    images = []
    filenames = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
            filenames.append(filename)
    return images, filenames


def kmeans_seg(img, filename, outputpath):
	"""
	Run K-means for color reduction based segmentation.
	:param: OpenCV images
	:param: Filenames
	:param: Output folder path
	:return: None
	"""
	Z = img.reshape((-1,3))

	# convert to np.float32
	Z = np.float32(Z)

	# define criteria, number of clusters(K) and apply kmeans()
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	K = 2
	ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_PP_CENTERS)
	# Now convert back into uint8, and make original image
	center = np.uint8(center)
	# pdb.set_trace()
	center0 = center[0:1]
	center1 = center[1:]
	res = center[label.flatten()].reshape((img.shape))
	cv2.imwrite(os.path.join(outputpath, filename), res)

# K-means color reduction

# 	input_path = "/Users/yiyi/vsr-api-2/vsr-api/data/image/sample"
# 	outputpath = "./output1"
# 	images, filenames = load_images_from_folder(input_path)
# 	for image, filename in zip(images, filenames):
# 		kmeans_seg(image, filename, outputpath)

# HSV based dominant color extraction
img = cv2.imread('/Users/yiyi/vsr-api-2/vsr-api/data/image/sample/10362354_10362354.jpg')
height, width, _ = np.shape(img)

# reshape the image to be a simple list of RGB pixels
image = img.reshape((height * width, 3))

# we'll pick the 5 most common colors
num_clusters = 10
clusters = KMeans(n_clusters=num_clusters)
clusters.fit(image)

# count the dominant colors and put them in "buckets"
histogram = make_histogram(clusters)
# then sort them, most-common first
combined = zip(histogram, clusters.cluster_centers_)
combined = sorted(combined, key=lambda x: x[0], reverse=True)

# finally, we'll output a graphic showing the colors in order
bars = []
hsv_values = []
for index, rows in enumerate(combined):
    bar, rgb, hsv = make_bar(100, 100, rows[1])
    print(f'Bar {index + 1}')
    print(f'  RGB values: {rgb}')
    print(f'  HSV values: {hsv}')
    hsv_values.append(hsv)
    bars.append(bar)

# sort the bars[] list so that we can show the colored boxes sorted
# by their HSV values -- sort by hue, then saturation
# sorted_bar_indexes = sort_hsvs(hsv_values)
# sorted_bars = [bars[idx] for idx in sorted_bar_indexes]

# cv2.imshow('Sorted by HSV values', np.hstack(sorted_bars))
cv2.imshow(f'{num_clusters} Most Common Colors', np.hstack(bars))
# cv2.waitKey(0)

for mc_hsv in hsv_values:
	upper = tuple((mc_hsv[0]+12., 225., 225.))
	lower = tuple((mc_hsv[0]-12., 30., 30.))
	# pdb.set_trace()
	hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv_img, lower, upper)
	result = cv2.bitwise_and(img, img, mask=mask)
	result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
	plt.subplot(1, 2, 1)
	plt.imshow(mask, cmap="gray")
	plt.subplot(1, 2, 2)
	plt.imshow(result)
	plt.show()