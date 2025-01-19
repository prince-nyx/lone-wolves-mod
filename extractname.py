from PIL import Image
import math

def colorDistance(firstColor, secondColor):
    rDiff = firstColor[0] - secondColor[0]
    gDiff = firstColor[1] - secondColor[1]
    bDiff = firstColor[2] - secondColor[2]

    return math.sqrt(rDiff * rDiff + gDiff * gDiff + bDiff * bDiff)

def extractText(path):
    img = Image.open(path)
    pixels = list(img.getdata())

    thresh = 90

    newPixels = []
    for pixel in pixels:
        if colorDistance(pixel, (8,185,21)) < thresh or colorDistance(pixel, (2, 1, 177)) < thresh:
            newPixel = (0,0,0)
        else:
            newPixel = (255,255,255)
        newPixels.append(newPixel)

    im = Image.new(img.mode, img.size)
    im.putdata(newPixels)
    im.save(path)