import cv2 as cv
import numpy as np
from matplotlib import *
import matplotlib.pyplot as plt
import matplotlib.image as image

import math as m
import glob
import os

from scipy import linalg


def showImg(img, windowName):
    # resize img
    width = 400
    height = m.floor(width*1.2)
    img = cv.resize(img, (width, height))

    # display img
    cv.imshow(windowName, img)
    # wait until user presses key to terminate window
    cv.waitKey(0)
    cv.destroyAllWindows()


def discretizeImg(A, numColors, type="left"):
    endpoints = numColors+1
    minPix = np.min(A)
    maxPix = np.max(A)
    sections = np.linspace(minPix, maxPix, num=endpoints)

    newImg = A
    # TYPES: left, right, mid, weighted_mean
    if (type == "left"):
        for color in range(numColors):
            if (color == numColors-1):
                newImg[(newImg >= sections[color]) & (
                    newImg <= sections[color+1])] = sections[color]
            else:
                newImg[(newImg >= sections[color]) & (
                    newImg < sections[color+1])] = sections[color]

    # FIXME doesn't work: all single color
    # elif (type == "right"):
    #     for color in range(numColors):
    #         if (color == numColors-1):
    #             newImg[(newImg >= sections[color]) & (
    #                 newImg <= sections[color+1])] = sections[color+1]
    #         else:
    #             newImg[(newImg >= sections[color]) & (
    #                 newImg < sections[color+1])] = sections[color+1]

    return newImg


def rankApproximateImage(U, S, Vt, k):
    return (U[:, :k] @ np.diag(S[:k]) @ Vt[:k])


def compressImage(A, relative_rank):
    # extract R,G,B channels
    # normalize rgb by dividing by 0xff
    R = A[:, :, 0] / 0xff
    G = A[:, :, 1] / 0xff
    B = A[:, :, 2] / 0xff

    # svd of channels
    U_R, S_R, VT_R = np.linalg.svd(R, full_matrices=False)
    U_G, S_G, VT_G = np.linalg.svd(G, full_matrices=False)
    U_B, S_B, VT_B = np.linalg.svd(B, full_matrices=False)

    # find k
    k = int(relative_rank * min(R.shape[0], R.shape[1]))

    # use principle components to approximate channels
    R_approx = rankApproximateImage(U_R, S_R, VT_R, k)
    G_approx = rankApproximateImage(U_G, S_G, VT_G, k)
    B_approx = rankApproximateImage(U_B, S_B, VT_B, k)
    layers = (R_approx, G_approx, B_approx)

    # convert to single channel
    compressed_float = np.dstack(layers)

    return (np.minimum(compressed_float, 1.0)*0xff).astype(np.uint8)


"""
def svdOfImg(img, threshold):
    # take economy SVD of data
    U, S, Vt = linalg.svd(img, full_matrices=False)
    S = np.diag(S)

    # extract percentages of energy from ranks
    percentages = np.cumsum(np.diag(S)) / np.sum(np.diag(S))

    # find first index that surpasses threshold
    r = np.searchsorted(percentages, threshold)
    # r = 40

    # approximate original data with r-rank SVD
    imgSvd = U[:, :r] @ S[0:r, :r] @ Vt[:r, :]

    return r, imgSvd
"""


# def discretizeImg(path, numColors=4, type="left",):
def transform_discretize(path, colors=4, type="left",):
    def to_raw(string):
        return fr"{string}"

    print("\n\nPath argument: {}".format(path))
    # path = r"C:\Users\justi\OneDrive\Pictures\Backgrounds\glory.png"
    path = path.get()
    # path = path.encode('unicode_escape')
    # path = r'{}'.format(path)
    print("{} \n\n".format(path))
    A = cv.imread(to_raw(path))
    print("I am past defining A")
    # A = image.fromArray(path)

    r = A[:, :, 0]
    g = A[:, :, 1]
    b = A[:, :, 2]

    bNorm = cv.normalize(
        b, None, alpha=0, beta=1,
        norm_type=cv.NORM_MINMAX,
        dtype=cv.CV_32F
    )

    gNorm = cv.normalize(
        g, None, alpha=0, beta=1,
        norm_type=cv.NORM_MINMAX,
        dtype=cv.CV_32F
    )

    rNorm = cv.normalize(
        r, None, alpha=0, beta=1,
        norm_type=cv.NORM_MINMAX,
        dtype=cv.CV_32F
    )

    newB = discretizeImg(bNorm, colors)
    newG = discretizeImg(gNorm, colors)
    newR = discretizeImg(rNorm, colors)

    layers = (newR, newG, newB)
    discLayers = cv.merge(layers)

    return discLayers
