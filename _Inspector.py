import cv2
import numpy as np
from matplotlib import pyplot as plt

def paddedsize(img_1 , img_2=None):
    # calculate padding size
    if img_2 is None:
        P = 2 * img_1.shape[1]
        Q = 2 * img_1.shape[0]
    else:
        P = 2 * np.max(img_1.shape[1], img_2.shape[1])
        Q = 2 * np.max(img_1.shape[0], img_2.shape[0])
    return P, Q


def notch(ftype, M, N, points, D0, n=1, w=1):
    # create empty filter mask
    fmask = np.zeros((M, N, 2), np.float32)
    for idx in range(0,len(points)):
        tmpmask = np.zeros((M, N, 2), np.float32)
        crow, ccol = points[idx]
        center = [crow, ccol]
        x, y = np.ogrid[:M, :N]
        D = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
        # check filter type: ideal, gaussian, butterworth
        if ftype == "gaussian":
            tmpmask[:, :, 0] = 1 - np.exp(-D ** 2 / (2 * D0 ** 2))
            tmpmask[:, :, 1] = 1 - np.exp(-D ** 2 / (2 * D0 ** 2))
        elif ftype == "ideal":
            tmpmask[D > D0, 0] = 1
            tmpmask[D > D0, 1] = 1
        elif ftype == "btw":
            # add const value to avoid division by zero
            tmpmask[:, :, 0] = (1 / (1 + (((w * D0) / (D+0.0001)) ** (2 * n))))
            tmpmask[:, :, 1] = (1 / (1 + (((w * D0) / (D+0.0001)) ** (2 * n))))
        else:
            print("Wrong filter type given: try 'gaussian', 'btw', or 'ideal'!")
            return None

        # merge filter masks for given points in frequency domain
        if idx != 0:
            fmask = fmask * tmpmask
        else:
            fmask += tmpmask

    return fmask


img_back = cv2.imread("./img/Other/image_100.jpg") # , cv2.COLOR_RGB2BGR
img_gray = cv2.imread("./img/1-NoHat/image_041.jpg", cv2.IMREAD_GRAYSCALE) # , cv2.COLOR_RGB2BGR



P,Q = paddedsize(img_gray)
D0 = 52
points = []
# D0 = 2      # radius of filter
mask = notch('gaussian', Q, P, points, D0)


img_padded = cv2.copyMakeBorder(img_gray, Q//4, Q//4, P//4, P//4, cv2.BORDER_CONSTANT)

# calculate spectrum and visualize result
dft = cv2.dft(np.float32(img_padded), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)
mag_spec = 20 * np.log(1+cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))


# apply filter
fshift_mask = cv2.mulSpectrums(dft_shift, mask, 0)

fshift_mask_mag = 20 * np.log(1+cv2.magnitude(fshift_mask[:, :, 0],
                                              fshift_mask[:, :, 1]))
# apply inverse transformation
f_ishift = np.fft.ifftshift(fshift_mask)
img_back_padded = cv2.idft(f_ishift, flags=cv2.DFT_SCALE)
img_back_padded = cv2.magnitude(img_back_padded[:,:,0],
                                img_back_padded[:,:,1])
# remove padded area
img_back = img_back_padded[P//4:P//4+img_gray.shape[1], Q//4:Q//4+img_gray.shape[0]]


# div = img/img_back
# plt.imshow(img_back)
plt.imshow(img_back, cmap='gray')
print(img_padded.shape )
print(mask.shape )
print(img_back.max())
print(img_back.min())
print(img_back.mean())
# print(max(img_back), min(img_back), mean(img_back))
# print(img.shape)
# plt.imshow(div)
plt.show()
