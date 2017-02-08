import numpy as np
import cv2 as cv

def trigulationMatting(compA, compB, backA, backB):
    # r -> 0; g -> 1; b -> 2
    cAr, cAg, cAb, cBr, cBg, cBb = compA[:, :, 0], compA[:, :, 1], compA[:, :, 2],\
                                   compB[:, :, 0], compB[:, :, 1], compB[:, :, 2]
    bAr, bAg, bAb, bBr, bBg, bBb = backA[:, :, 0], backA[:, :, 1], backA[:, :, 2],\
                                   backB[:, :, 0], backB[:, :, 1], backB[:, :, 2]
    # color = np.zeros(compA.shape)  # size and color
    alpha = np.zeros(compA.shape[:2])  # only the size
    alpha = 1 - (((cAr- cBr) * (bAr - bBr) + (cAg - cBg) * (bAg - bBg) + (cAb - cBb) * (bAb - bBb)) /
                 +((bAr - bBr) ** 2 + (bAg - bBg) ** 2 + (bAb - bBb) ** 2))
    newAlpha = np.zeros(backA.shape)
    newAlpha[:, :, 0] = alpha
    newAlpha[:, :, 1] = alpha
    newAlpha[:, :, 2] = alpha
    color = compA - (1-newAlpha)*backA
    return color, alpha


def createComposite(realBack, alpha):
    # deal with background
    back = np.zeros(compA.shape)
    print 'in composite:'
    print alpha.shape
    print 1- alpha[0][0]
    for h in range(realBack.shape[0]):
        for w in range(realBack.shape[1]):
            back[h][w] = realBack[h][w] * (1.0 - alpha[h][w])
    return back


if __name__ == '__main__':
    compA = cv.imread('../MoreImages/flowers-compA.jpg')/255.0
    compB = cv.imread('flowers-compB.jpg')/255.0
    backA = cv.imread('flowers-backA.jpg')/255.0
    backB = cv.imread('flowers-backB.jpg')/255.0
    realBack = cv.imread('window.jpg')/255.0
    color, alpha = trigulationMatting(compA, compB, backA, backB)
    color = color * 255.0
    cv.imwrite('flower-alpha4.jpg', alpha*255.0)
    cv.imwrite('flower-foreground4.jpg',color)

    back = np.zeros(compA.shape)
    newAlpha = np.zeros(backA.shape)
    newAlpha[:, :, 0] = alpha
    newAlpha[:, :, 1] = alpha
    newAlpha[:, :, 2] = alpha
    back = realBack * (1.0 - newAlpha)
    back = back * 255.0
    cv.imwrite('flower-back4.jpg',back)
    composite = color + back
    cv.imwrite('flower-composite4.jpg', composite)